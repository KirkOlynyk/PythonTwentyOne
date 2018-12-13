'''
bj.py

Controls the blackjack program
'''
import sys
import abc

NEVER = sys.float_info.max
ALWYS = sys.float_info.min

class IPlayer(abc.ABC):
  @abc.abstractclassmethod
  def want_insurance(self, hand, dealer):
    pass
  @abc.abstractclassmethod
  def want_surrender(self, hand, dealer):
    pass
  @abc.abstractclassmethod
  def want_split(self, hand, dealer):
    pass
  @abc.abstractclassmethod
  def want_double(self, hand, dealer):
    pass
  @abc.abstractclassmethod
  def want_stand(self, hand, dealer):
    pass

class InvalidFace(Exception):
  pass

class Hand:
  'A hand in blackjack does not care about the suits of the cards'

  chars = '23456789XJQKA'
  # faces   0   1   2   3   4   5   6   7   8   9  10  11  12
  # chars   2   3   4   5   6   7   8   9   X   J   Q   K   A
  values = [2,  3,  4,  5,  6,  7,  8,  9, 10, 10, 10, 10,  1]

  def __init__(self):
    self.has_aces = False
    self.faces = []
    self.total = 0

  def is_blackjack(self):
    'return True if this hand is a blackjack'
    return self.has_aces and len(self.faces) == 2 and self.total == 11

  def is_pair_of_8s(self):
    return len(self.faces) == 2 and self.faces[0] == 6 and self.faces[1] == 6

  def add(self, i): 
    'add a card using it\'s face index'
    if i < 0 or i >= len(Hand.values):
      raise InvalidFace
    if i == 12:
      self.has_aces = True
    self.total += Hand.values[i]
    self.faces.append(i)
    self.repr = self.__repr__()

  def value(self):
    'return the value of the hand'
    if self.is_soft():
      return self.total + 10
    else:
      return self.total

  def __repr__(self):
    temp = self.faces[:]
    temp.sort()
    ans = ''
    for i in temp:
      ans += Hand.chars[i]
    return ans + ": " + str(self.value())

  def addFace(self, face):
    self.add(Hand.chars.index(face))

  def is_soft(self):
    return self.has_aces and self.total <= 11

  def has_ace(self):
    return self.total == 1

  @staticmethod
  def create(hand):
    ans = Hand()
    for card in hand:
      ans.addFace(card)
    return ans


class Counter(IPlayer):
  hard_stand_table = {
    #            2      3      4      5      6      7      8      9      X      A
      12 : [  +3.0,  +1.5,   0.0,  -1.5,  -1.0, NEVER, NEVER, NEVER, NEVER, NEVER],
      13 : [  -1.0,  -2.5,  -3.5,  -5.0,  -5.0, NEVER, NEVER, NEVER, NEVER, NEVER],
      14 : [  -4.0,  -5.0,  -6.0, ALWYS, ALWYS, NEVER, NEVER, NEVER, NEVER, NEVER],
      15 : [ ALWYS, ALWYS, ALWYS, ALWYS, ALWYS,  +9.5,  +9.0,  +7.5,  +4.5,  +9.0],
      16 : [ ALWYS, ALWYS, ALWYS, ALWYS, ALWYS,  +7.5,  +6.5,  +4.5,   0.0,  +8.5],
      17 : [ ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS],
      18 : [ ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS],
      19 : [ ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS],
      20 : [ ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS],
      21 : [ ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS],
  }

  soft_stand_table = {
    #            2      3      4      5      6      7      8      9      X      A
      18 : [ ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, NEVER, NEVER,  +1.5],
      19 : [ ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS],
      20 : [ ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS],
      21 : [ ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS],
  }

  double_table = {
    #            2      3      4      5      6      7      8      9      X      A
    '22' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '23' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '24' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '25' : [ NEVER, NEVER, NEVER,  +9.0,  +9.0, NEVER, NEVER, NEVER, NEVER, NEVER],
    '26' : [ NEVER,  +9.5,  +6.0,  +3.5,  +2.0, NEVER, NEVER, NEVER, NEVER, NEVER],
    '27' : [  +1.0,  -1.5,  -3.0,  -4.5,  -6.5,  +3.5,  +7.5, NEVER, NEVER, NEVER],
    '28' : [ ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS,  -4.5,  -1.5,  +4.0,  +4.0],
    '29' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER,  -5.0,  -5.0,  +1.5],
    '2X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '2A' : [ NEVER,  +8.0,  +4.0,   0.0,  -1.5, NEVER, NEVER, NEVER, NEVER, NEVER],
    '33' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '34' : [ NEVER, NEVER, NEVER,  +9.0,  +9.0, NEVER, NEVER, NEVER, NEVER, NEVER],
    '35' : [ NEVER,  +9.5,  +6.0,  +3.5,  +2.0, NEVER, NEVER, NEVER, NEVER, NEVER],
    '36' : [  +1.0,  -1.5,  -3.0,  -4.5,  -6.5,  +3.5,  +7.5, NEVER, NEVER, NEVER],
    '37' : [ ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS,  -4.5,  -1.5,  +4.0,  +4.0],
    '38' : [ ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS,  -5.0,  -5.0,  +1.5],
    '39' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '3X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '3A' : [ NEVER,  +8.0,  +2.5,  -1.0,  -4.5, NEVER, NEVER, NEVER, NEVER, NEVER],
    '44' : [ NEVER,  +9.5,  +6.0,  +3.5,  +2.0, NEVER, NEVER, NEVER, NEVER, NEVER],
    '45' : [  +1.0,  -1.5,  -3.0,  -4.5,  -6.5,  +3.5,  +7.5, NEVER, NEVER, NEVER],
    '46' : [ ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS,  -4.5,  -1.5,  +4.0,  +4.0],
    '47' : [ ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS,  -5.0,  -5.0,  +1.5],
    '48' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '49' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '4X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '4A' : [ NEVER,  +8.0,   0.0,  -4.5, ALWYS, NEVER, NEVER, NEVER, NEVER, NEVER],
    '55' : [ ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS,  -4.5,  -1.5,  +4.0,  +4.0],
    '56' : [ ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS,  -5.0,  -5.0,  +1.5],
    '57' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '58' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '59' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '5X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '5A' : [ NEVER,  +4.0,  -3.0, ALWYS, ALWYS, NEVER, NEVER, NEVER, NEVER, NEVER],
    '66' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '67' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '68' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '69' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '6X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '6A' : [  +1.0,  -4.0, ALWYS, ALWYS, ALWYS, NEVER, NEVER, NEVER, NEVER, NEVER],
    '77' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '78' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '79' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '7X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '7A' : [  +0.5,  -3.0,  -5.5, ALWYS, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '88' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '89' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '8X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '8A' : [  +8.0,  +5.5,  +3.5,  +1.5,  +1.0, NEVER, NEVER, NEVER, NEVER, NEVER],
    '99' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '9X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '9A' : [ +11.0,  +9.0,  +6.5,  +5.0,  +4.5, NEVER, NEVER, NEVER, NEVER, NEVER],
    'XX' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    'XA' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    'AA' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
  }

  split_table = {
    #            2      3      4      5      6      7      8      9      X      A
    '22' : [  -3.0, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS,  +5.0, NEVER, NEVER, NEVER],
    '23' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '24' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '25' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '26' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '27' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '28' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '29' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '2X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '2A' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '33' : [  -0.5,  -4.5,  -6.0, ALWYS, ALWYS, ALWYS,  +4.0, NEVER, NEVER, NEVER],
    '34' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '35' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '36' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '37' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '38' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '39' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '3X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '3A' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '44' : [ NEVER,  +8.5,  +3.0,  -0.5,  -2.0, NEVER, NEVER, NEVER, NEVER, NEVER],
    '45' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '46' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '47' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '48' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '49' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '4X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '4A' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '55' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '56' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '57' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '58' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '59' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '5X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '5A' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '66' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '67' : [  -2.0,  -4.5, ALWYS, ALWYS, ALWYS, NEVER, NEVER, NEVER, NEVER, NEVER],
    '68' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '69' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '6X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '6A' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '77' : [ ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, NEVER, NEVER, NEVER, NEVER],
    '78' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '79' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '7X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '7A' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '88' : [ ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS],
    '89' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '8X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '8A' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '99' : [  -3.5,  -5.0,  -6.0, ALWYS, ALWYS,  +3.0, ALWYS, ALWYS, NEVER,  +3.5],
    '9X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '9A' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    'XX' : [ NEVER, NEVER,  +6.5,  +5.0,  +4.5, +15.0, NEVER, NEVER, NEVER, NEVER],
    'XA' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    'AA' : [ ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS, ALWYS],
  }

  surrender_table = {
    #            2      3      4      5      6      7      8      9      X      A
    '22' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '23' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '24' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '25' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '26' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '27' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '28' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '29' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '2X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '2A' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '33' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '34' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '35' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '36' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '37' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '38' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '39' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '3X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '3A' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER,  +3.0, NEVER],
    '44' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '45' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '46' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '47' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '48' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '49' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '4X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER,  +3.0, NEVER],
    '4A' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER,  +3.0,  -1.0,  +2.0],
    '55' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '56' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '57' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '58' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '59' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER,  +3.0, NEVER],
    '5X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER,  +3.0,  -1.0,  +2.0],
    '5A' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER,  +4.0,   0.0,  -3.0,  -2.0],
    '66' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '67' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '68' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER,  +3.0, NEVER],
    '69' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER,  +3.0,  -1.0,  +2.0],
    '6X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER,  +4.0,   0.0,  -3.0,  -2.0],
    '6A' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '77' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER,  +3.0, NEVER],
    '78' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER,  +3.0,  -1.0,  +2.0],
    '79' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER,  -3.0,  -2.0],
    '7X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '7A' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '88' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER,  +7.0,   0.0, NEVER],
    '89' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '8X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '8A' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '99' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '9X' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    '9A' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    'XX' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    'XA' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
    'AA' : [ NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER, NEVER],
  }

  insurance_table = {
    '22' : +3.0,    '23' : +3.0,    '24' : +3.0,    '25' : +3.0,
    '26' : +3.0,    '27' : +3.0,    '28' : +3.0,    '29' : +3.0,
    '2X' : +3.0,    '2A' : +3.0,    '33' : +3.0,    '34' : +3.0,
    '35' : +3.0,    '36' : +3.0,    '37' : +3.0,    '38' : +3.0,
    '39' : +3.0,    '3X' : +3.0,    '3A' : +3.0,    '44' : +3.0,
    '45' : +3.0,    '46' : +3.0,    '47' : +3.0,    '48' : +3.0,
    '49' : +3.0,    '4X' : +3.0,    '4A' : +3.0,    '55' : +3.0,
    '56' : +3.0,    '57' : +3.0,    '58' : +3.0,    '59' : +3.0,
    '5X' : +3.0,    '5A' : +3.0,    '66' : +3.0,    '67' : +3.0,
    '68' : +3.0,    '69' : +3.0,    '6X' : +3.0,    '6A' : +3.0,
    '77' : +3.0,    '78' : +3.0,    '79' : +3.0,    '7X' : +3.0,
    '7A' : +3.0,    '88' : +3.0,    '89' : +3.0,    '8X' : +3.0,
    '8A' : +3.0,    '99' : +3.0,    '9X' : +3.0,    '9A' : +3.0,
    'XX' : +3.0,    'XA' : +3.0,    'AA' : +3.0,
  }

  def __init__(self):
    self.true_count = 0.0

  upcard_index = {
    '2' : 0, '3' : 1, '4' : 2, '5' : 3, '6' : 4, '7' : 5, '8' : 6, '9' : 7,
    'X' : 8, 'A' : 9
  }

  value_dict = {
    '2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9,
    'X' : 10, 'A' : 1 
  }

  @staticmethod
  def get_value(hand:str):
    total = 0
    has_aces = False
    for face in hand:
      card_value = Counter.value_dict[face]
      if card_value == 1:
        has_aces = True
      total += card_value
    if total <= 11 and has_aces:
      return total + 10, True
    else:
      return total, False

  @staticmethod
  def is_blackjack(hand : str) -> bool:
    if len(hand) == 2:
      return Counter.get_value(hand) == (21, True)
    else:
      return False

  @staticmethod
  def get_index(face:str) -> int:
    return Counter.upcard_index[face]

  @staticmethod
  def handsort(hand:str) -> str:
    fs = list(hand)
    fs.sort(key=Counter.get_index)
    return ''.join(fs)
  
  @staticmethod
  def want_insurance(true_count, hand, upcard) -> bool:
    threshold = Counter.insurance_table[hand]
    return true_count >= threshold

  @staticmethod
  def want_surrender(true_count, hand, upcard):
    return Counter.want_something(Counter.surrender_table, true_count, hand, upcard)

  @staticmethod
  def want_split(true_count, hand, upcard):
    return Counter.want_something(Counter.split_table, true_count, hand, upcard)

  @staticmethod
  def want_double(true_count, hand, upcard):
    return Counter.want_something(Counter.double_table, true_count, hand, upcard)

  @staticmethod
  def want_stand(true_count, hand, upcard):
    value, soft = Counter.get_value(hand)
    if soft:
      table = Counter.soft_stand_table
    else:
      table = Counter.hard_stand_table
    try:
      index = Counter.upcard_index[upcard]
      threshold = table[value][index]
      return true_count >= threshold
    except KeyError:
        return False

  @staticmethod
  def want_something(table, true_count, hand, upcard):
    index = Counter.upcard_index[upcard]
    threshold = table[hand][index]
    return true_count >= threshold

if __name__ == '__main__':
  def test(hand, upcard, true_count):
    print(Counter.want_stand(true_count, hand, upcard))
  test('X6', 'X', -1.0)
