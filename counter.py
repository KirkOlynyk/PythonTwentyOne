'''
counter.py

Defines the Counter class for a blackjack counter
'''

import json
from math import floor
from player import Player
from rules import CARDS_PER_DECK, CARD_VALUES, hand_value, CARD_INDEXES

class Counter(Player):
  '''
  The Player is a card counter
  '''

  def __init__(self, json_file_path: str):
    with open(json_file_path, 'r') as fobj:
      self._tables = json.load(fobj)
    self._true_count = 0.0
    self._count = 0.0
    self._decks_in_shoe = 0.0
    self._number_cards_seen = 0.0
    self._minimum_bet = 0.0   # table minimum
    self._maximum_bet = 0.0   # table maximum

    self._bankrole = self._tables['bankrole']
    self._unit = self._tables['unit']
    self._true_adjust = self._tables['true_adjust']
    self._counts = self._tables['counts']
    self._hard_stand = self._tables['hard_stand']
    self._soft_stand = self._tables['soft_stand']
    self._double = self._tables['double']
    self._split = self._tables['split']
    self._surrender = self._tables['surrender']
    self._insurance = self._tables['insurance']
    self._upcard_index = self._tables['upcard_index']

  def place_insurance_bet(self, bet:float) -> None:
    'remove the insurance bet from the player bankrole'
    self._bankrole -= bet

  def set_minimum_bet(self, bet:float) -> None:
    'sets the table minimum bet'
    self._minimum_bet = bet

  def set_maximum_bet(self, bet:float) -> None:
    'sets maximum table bet'
    self._maximum_bet = bet

  def receive_payoff(self, amount : float) -> None:
    '''
    The player has won the wager. This is the
    return of the win along with the original wager
    '''
    self._bankrole += amount

  def get_bet(self) -> float:
    '''
    The hand is started and a wager must be made. The player
    calculates the bet and removes it from his bankrole
    and places it on the table.
    '''
    scale = self._true_count + self._true_adjust
    wager = self._unit * floor(scale + 0.5)
    if wager < self._minimum_bet:
      wager = self._minimum_bet
    elif wager > self._maximum_bet:
      wager = self._maximum_bet
    self._bankrole -= wager
    return wager

  def _accepts(self, cards:str, upcard:str, table) -> bool:
    assert len(cards) == 2
    try:
      hand = self._handsort(cards)
      updex = self._upcard_index[upcard]
      critical_true = table[hand][updex]
      return self._true_count >= critical_true
    except KeyError:
      return False

  def accepts_insurance(self, cards : str, upcard : str) -> bool:
    '''
    The player is asked by the dealer if the hand should be
    insured. If then the dealer will place a side bet of 
    one half of the current bet on the hand
    '''
    assert upcard == 'A'
    assert len(cards) == 2
    try:
      hand = self._handsort(cards)
      return self._true_count >= self._insurance[hand]
    except KeyError:
      return False
    
  def accepts_surrender(self, cards:str, upcard:str) -> bool:
    return self._accepts(cards, upcard, self._insurance)

  def accepts_split(self, cards:str, upcard:str) -> bool:
    return self._accepts(cards, upcard, self._split)

  def accepts_double(self, cards:str, upcard:str) -> bool:
    return self._accepts(cards, upcard, self._double)

  def accepts_stand(self, cards:str, upcard:str) -> bool:
    value, soft = hand_value(cards)
    if soft:
      table = self._soft_stand
    else:
      table = self._hard_stand
    try:
      critical_true = table[str(value)]
      return self._true_count >= critical_true
    except KeyError:
      return False

  def show_card(self, card : str) -> None:
    'The player sees a card that has been dealt to the table'
    assert len(card) == 1
    self._number_cards_seen += 1.0
    self._count += self._counts[card]
    self._set_true_count()

  def show_decks_in_shoe(self, decks_in_shoe:int) -> None:
    '''
    Tells the counter the number of decks in the shoe.
    This is needed for calculating the true count.
    '''
    self._decks_in_shoe = float(decks_in_shoe)

  def _set_true_count(self) -> None:
    'set self.value to the current value'
    number_cards = CARDS_PER_DECK * self._decks_in_shoe
    number_cards_unseen = number_cards - self._number_cards_seen
    number_decks_unseen = number_cards_unseen / CARDS_PER_DECK
    self._true_count = self._count / number_decks_unseen

  def _handsort(self, cards:str) -> str:
    '''
    sort a hand so that the low cards come first
    Normally there are two cards.
    '''
    hand = list(cards)
    def keyfun(card):
      return CARD_INDEXES[card]
    hand.sort(key=keyfun)
    return ''.join(hand)

if __name__ == '__main__':
  counter = Counter('counter.json')
  counter.show_decks_in_shoe(6)
  counter.set_minimum_bet(100.0)
  counter.set_maximum_bet(3000.0)
  bet = counter.get_bet()
  print("counter bets", bet)
  print("bankrole", counter._bankrole)
  cards = 'A5'
  value, soft = hand_value(cards)
  print(value, soft)
  hand = counter._handsort(cards)
  print("cards", cards)
  print('hand', hand)
