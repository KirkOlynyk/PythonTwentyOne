'''
counter.py

Defines the Counter class for a blackjack counter
'''

import json
from math import floor
from player import Player
from rules import CARDS_PER_DECK

class Counter(Player):

  def __init__(self, json_file_path: str):
    with open(json_file_path, 'r') as fobj:
      self._tables = json.load(fobj)
    self._true_count = 0.0
    self._true_adjust = self._tables['true_adjust']
    self._count = 0.0
    self._decks_in_shoe = 0.0
    self._number_cards_seen = 0.0
    self._unit = self._tables['unit']
    self._bankrole = self._tables['bankrole']
    self._minimum_bet = self._tables['minimum_bet']
    self._maximum_bet = self._tables['maximum_bet']
    self._count_table = self._tables['counts']
    self._value_dict = self._tables['value_dict']

  def receive_payoff(self, amount : float) -> None:
    self._bankrole += amount
  def get_bet(self) -> float:
    scale = self._true_count + self._true_adjust
    wager = self._unit * floor(scale + 0.5)
    if wager < self._minimum_bet:
      wager = self._minimum_bet
    elif wager > self._maximum_bet:
      wager = self._maximum_bet
    self._bankrole -= wager
    return wager
  def accepts_insurance(self, cards : str, upcard : str) -> bool:
    return Counter._want_insurance(self._true_count, Counter.handsort(cards), upcard)
  def accepts_surrender(self, cards : str, upcard : str) -> bool:
    return Counter._want_surrender(self._true_count, Counter.handsort(cards), upcard)
  def accepts_split(self, cards : str, upcard : str) -> bool:
    return Counter._want_split(self._true_count, Counter.handsort(cards), upcard)
  def accepts_double(self, cards : str, upcard : str) -> bool:
    return Counter._want_double(self._true_count, Counter.handsort(cards), upcard)
  def accepts_stand(self, cards : str, upcard : str) -> bool:
    return Counter._want_stand(self._true_count, Counter.handsort(cards), upcard)
  def show_card(self, card : str) -> None:
    'The player sees a card that has been dealt to the table'
    self._number_cards_seen += 1.0
    self._count += self._count_table[card]
    self._set_true_count()
  def set_decks_in_shoe(self, decks_in_shoe : int) -> None:
    self._decks_in_shoe = float(decks_in_shoe)
  def _set_true_count(self) -> None:
    'set self.value to the current value'
    number_cards = CARDS_PER_DECK * self._decks_in_shoe
    number_cards_unseen = number_cards - self._number_cards_seen
    number_decks_unseen = number_cards_unseen / CARDS_PER_DECK
    self._true_count = self._count / number_decks_unseen

  def get_value(self, cards:str):
    total = 0
    has_aces = False
    for face in cards:
      card_value = self._value_dict[face]
      if card_value == 1:
        has_aces = True
      total += card_value
    if total <= 11 and has_aces:
      return total + 10, True
    else:
      return total, False

  @staticmethod
  def get_index(face:str) -> int:
    return Counter.upcard_index[face]

  @staticmethod
  def handsort(cards:str) -> str:
    'sort a hand so that the low cards come first'
    fs = list(cards)
    fs.sort(key=Counter.get_index)
    return ''.join(fs)
  
  @staticmethod
  def _want_insurance(true_count, cards, upcard) -> bool:
    threshold = Counter.insurance_table[cards]
    return true_count >= threshold

  @staticmethod
  def _want_surrender(true_count, cards, upcard):
    return Counter._want(Counter.surrender_table, true_count, cards, upcard)

  @staticmethod
  def _want_split(true_count, cards, upcard):
    return Counter._want(Counter.split_table, true_count, cards, upcard)

  @staticmethod
  def _want_double(true_count, cards, upcard):
    return Counter._want(Counter.double_table, true_count, cards, upcard)

  @staticmethod
  def _want_stand(true_count, cards, upcard):
    value, soft = Counter.get_value(cards)
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
  def _want(table, true_count, cards, upcard):
    index = Counter.upcard_index[upcard]
    threshold = table[cards][index]
    return true_count >= threshold
