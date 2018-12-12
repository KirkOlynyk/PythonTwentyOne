'''
bj.py

Controls the blackjack program
'''

class InvalidFace(Exception):
  pass

class Hand:
  'A hand in blackjack does not care about the suits of the cards'

  chars = '23456789XJQKA'
  values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 1]

  def __init__(self):
    self.has_aces = False
    self.faces = []
    self.total = 0

  def is_bj(self):
    'return True if this hand is a blackjack'
    return self.has_aces and len(self.faces) == 2 and self.total == 11

  def add(self, i): 
    'add a card using it\'s face index'
    if i < 0 or i >= len(Hand.values):
      raise InvalidFace
    if i == 12:
      self.has_aces = True
    self.total += Hand.values[i]
    self.faces.append(i)

  def value(self):
    'return the value of the hand'
    if self.has_aces and self.total <= 11:
      return self.total + 10
    else:
      return self.total

  def __repr__(self):
    temp = self.faces[:]
    temp.sort()
    ans = ''
    for i in temp:
      ans += Hand.chars[i]
    return ans + " " + str(self.value())

  def addFace(self, face):
    self.add(Hand.chars.index(face))

def test(arg):
  '''
  development testing routine
  '''
  hand = Hand()
  for face in arg:
    hand.addFace(face)
  if (hand.is_bj()):
    print(hand, 'blackjack!')
  else:
    print(hand)
