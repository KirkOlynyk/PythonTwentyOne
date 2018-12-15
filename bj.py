'''
bj.py

Controls the blackjack program

This is not designed to be fast. If you want fast then
use a compiled language.
'''
import sys
import abc
from math import floor
import random

class IPlayer(abc.ABC):
  @abc.abstractclassmethod
  def accepts_insurance(self, hand : str, upcard : str) -> bool:
    pass
  @abc.abstractclassmethod
  def accepts_surrender(self, hand : str, upcard : str) -> bool:
    pass
  @abc.abstractclassmethod
  def accepts_split(self, hand : str, upcard : str) -> bool:
    pass
  @abc.abstractclassmethod
  def accepts_double(self, hand : str, upcard : str) -> bool:
    pass
  @abc.abstractclassmethod
  def accepts_stand(self, hand : str, upcard : str) -> bool:
    pass
  @abc.abstractclassmethod
  def show_card(self, card : str) -> None:
    pass
  @abc.abstractclassmethod
  def set_decks_in_shoe(self, decks_in_shoe : int) -> None:
    pass
  @abc.abstractclassmethod
  def get_wager(self) -> float:
    pass
  @abc.abstractclassmethod
  def receive_payoff(self, amount) -> None:
    pass
  @abc.abstractclassmethod
  def set_minimum_bet(self, amount:float) -> None:
    pass
  @abc.abstractclassmethod
  def set_maximum_bet(self, amount:float) -> None:
    pass

NEVER = sys.float_info.max
ALWYS = sys.float_info.min
CARDS_PER_DECK = 52.0

class Counter(IPlayer):

  def __init__(self):
    self._true_count = 0.0
    self._true_adjust = -0.5
    self._count = 0.0
    self._decks_in_shoe = 0.0
    self._number_cards_seen = 0.0
    self._unit = 0.0
    self._bankrole = 0.0
    self._minimum_bet = 0.0
    self._maximum_bet = 0.0

  def set_minimum_bet(self, amount:float) -> None:
    self._minimum_bet = amount
  def set_maximum_bet(self, amount:float) -> None:
    self._maximum_bet = amount
  def receive_payoff(self, amount : float) -> None:
    self._bankrole += amount
  def get_wager(self) -> float:
    scale = self._true_count + self._true_adjust
    wager = self._unit * floor(scale + 0.5)
    if wager < self._minimum_bet:
      wager = self._minimum_bet
    elif wager > self._maximum_bet:
      wager = self._maximum_bet
    self._bankrole -= wager
    return wager
  def accepts_insurance(self, hand : str, upcard : str) -> bool:
    return Counter._want_insurance(self._true_count, Counter.handsort(hand), upcard)
  def accepts_surrender(self, hand : str, upcard : str) -> bool:
    return Counter._want_surrender(self._true_count, Counter.handsort(hand), upcard)
  def accepts_split(self, hand : str, upcard : str) -> bool:
    return Counter._want_split(self._true_count, Counter.handsort(hand), upcard)
  def accepts_double(self, hand : str, upcard : str) -> bool:
    return Counter._want_double(self._true_count, Counter.handsort(hand), upcard)
  def accepts_stand(self, hand : str, upcard : str) -> bool:
    return Counter._want_stand(self._true_count, Counter.handsort(hand), upcard)
  def show_card(self, card : str) -> None:
    'The player sees a card that has been dealt to the table'
    self._number_cards_seen += 1.0
    self._count += Counter.count_table[card]
    self._set_true_count()
  def set_decks_in_shoe(self, decks_in_shoe : int) -> None:
    self._decks_in_shoe = float(decks_in_shoe)
  def _set_true_count(self) -> None:
    'set self.value to the current value'
    number_cards = CARDS_PER_DECK * self._decks_in_shoe
    number_cards_unseen = number_cards - self._number_cards_seen
    number_decks_unseen = number_cards_unseen / CARDS_PER_DECK
    self._true_count = self._count / number_decks_unseen

  count_table = {
    '2' : 1, '3' : 1, '4' : 1, '5' : 1, '6' : 1,
    '7' : 0, '8' : 0, '9' : 0,
    'X' : -1, 'A' : -1
  }

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
    'sort a hand so that the low cards come first'
    fs = list(hand)
    fs.sort(key=Counter.get_index)
    return ''.join(fs)
  
  @staticmethod
  def _want_insurance(true_count, hand, upcard) -> bool:
    threshold = Counter.insurance_table[hand]
    return true_count >= threshold

  @staticmethod
  def _want_surrender(true_count, hand, upcard):
    return Counter._want(Counter.surrender_table, true_count, hand, upcard)

  @staticmethod
  def _want_split(true_count, hand, upcard):
    return Counter._want(Counter.split_table, true_count, hand, upcard)

  @staticmethod
  def _want_double(true_count, hand, upcard):
    return Counter._want(Counter.double_table, true_count, hand, upcard)

  @staticmethod
  def _want_stand(true_count, hand, upcard):
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
  def _want(table, true_count, hand, upcard):
    index = Counter.upcard_index[upcard]
    threshold = table[hand][index]
    return true_count >= threshold

def test1():
  #       23456789XJQKA
  suit = '23456789XXXXA'
  deck = suit + suit + suit + suit
  decks = deck + deck + deck + deck + deck + deck
  shoe = list(decks)
  # show that the total count of the shoe is zero
  if sum([Counter.count_table[x] for x in shoe]) != 0:
    raise ValueError
  random.seed(a=23)     # set the seed for the random number generator
  random.shuffle(shoe)
  print(''.join(shoe[:32]))

def test0():
  player = Counter()
  player.set_decks_in_shoe(6)
  card1 = 'X'
  card2 = '6'
  upcard = 'A'
  player.show_card(card1)
  player.show_card(card2)
  hand = card1 + card2
  player.show_card(upcard)
  if player.accepts_insurance(hand, upcard):
    print("accept insurance")
  else:
    print("decline insurance")

if __name__ == '__main__':
  test1()
