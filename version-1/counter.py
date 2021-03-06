'''
counter.py

Implments the Player inteface
'''

from math import floor, ceil
import json
from general import CARD, HAND, General
from player import Player

# pylint: disable=R0902
class Counter(Player):
  '''
  Card counter class
  '''

  _cards_to_decks = 0.0192307692307692 # = 1 / 52
  _key_alphabet = '23456789XXXXA'
  #                 2  3  4  5  6  7  8  9  X  J  Q  K  A
  _face_to_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8, 9]

  def __init__(self, file_path: str) -> None:
    '''
    Constructor for the Counter class
    '''
    self.n_cards_dealt = 0
    self.n_decks = 0
    self.count = 0
    self.minimum_bet = 0.0
    self.maximum_bet = 0.0
    self.bankrole = 0.0
    self.ddict = Counter._get_json_dict(file_path)  # decision numbers
    self.unit = self.ddict['unit']                  # bet quantizer
    self.true_adjust = self.ddict['true_adjust']    # true adjustor for betting
    self.get_shoe_len = lambda: 0                   # function for shoe length

  @staticmethod
  def _card_to_index(card: CARD) -> int:
    '''
    returns index into decision tables. The the
    return value must be in the range 0 .. 9
    '''
    face = General.face_index(card)
    return Counter._face_to_index[face]

  @staticmethod
  def _card_to_character(card: CARD) -> str:
    '''
    Convert a card to a key character to be used by
    _hand_to_key
    '''
    return Counter._key_alphabet[card]

  @staticmethod
  def _hand_to_key(hand: HAND) -> str:
    '''
    Converts a hand into a sorted string key the mappings in self.ddict.
    The key is a two character string from the alphabet '23456789XA'.
    The key must be sorted in alphabetical order, that is 'A'
    always comes last, etc. For example the hand [12, 10]
    corresponds to 'AQ' will result in the key 'XA'
    '''
    a_list = hand[:]  # make a local copy so the sort does not affect the original
    a_list.sort()     # sort from low to high
    b_list = [Counter._card_to_character(x) for x in a_list]
    return "".join(b_list)

  @staticmethod
  def _get_json_dict(file_path: str) -> dict:
    '''
    Loads a JSON file and parse it into a dictionary which is the
    return value
    '''
    with open(file_path, 'r') as file_object:
      answer = json.load(file_object)
    return answer

  @staticmethod
  def _permit(hand: HAND, upcard: CARD, true_value: float, table: dict) -> bool:
    '''
    The counter has been asked if an action (surrender, split, etc.)
    is wanted or not. The decision table is provided.
    '''
    assert len(hand) == 2
    key = Counter._hand_to_key(hand)
    try:
      alist = table[key]
    except KeyError:
      return False
    index = Counter._card_to_index(upcard)
    crit = alist[index]
    return true_value >= crit

  def _request_action(self, hand: HAND, upcard: CARD, table: dict) -> bool:
    '''
    Determine if the counter wants the request action
    '''
    true_count = self.get_true()
    return Counter._permit(hand, upcard, true_count, table)

  def set_get_shoe_len(self, get_shoe_len) -> None:
    '''
    Set function to get the number of undealt cards
    remaining in the shoe
    '''
    self.get_shoe_len = get_shoe_len

  def requests_insurance(self, hand: HAND, upcard: CARD) -> bool:
    '''
    The dealer is asking the player if the hand should be insured
    '''
    try:
      index = Counter._card_to_index(upcard)
      return self.get_true() >= self.ddict['insurance'][index]
    except KeyError:
      return False

  def _requests_any(self, hand: HAND, upcard: CARD, table_key: str) -> bool:
    '''
    Answers whether the counter wants the specfied action
    '''
    table = self.ddict[table_key]
    return self._request_action(hand, upcard, table)

  def requests_surrender(self, hand: HAND, upcard: CARD) -> bool:
    '''
    The dealer is asking the player if the hand should be surrendered
    '''
    return self._requests_any(hand, upcard, 'surrender')

  def requests_split(self, hand: HAND, upcard: CARD) -> bool:
    '''
    The dealer is asking the player if the hand should be split
    '''
    return self._requests_any(hand, upcard, 'split')

  def requests_double(self, hand: HAND, upcard: CARD) -> bool:
    '''
    The dealer is asking the player if the bet on the hand should be doubled
    '''
    return self._requests_any(hand, upcard, 'double')

  def requests_stand(self, hand: HAND, upcard: CARD) -> bool:
    '''
    The dealer is asking the player if the hand should stand
    i.e. no more cards are to be added
    '''
    hand_value, is_soft = General.bj_value(hand)
    if is_soft:
      table_key = 'soft_stand'
    else:
      table_key = 'hard_stand'
    table = self.ddict[table_key]
    key = str(hand_value)
    true_count = self.get_true()
    index = self._card_to_index(upcard)
    try:
      alist = table[key]
      critical_true = alist[index]
      return true_count >= critical_true
    except KeyError:
      return False

  def observe_card(self, card: CARD) -> None:
    '''
    The newly dealt card is shown to the player
    '''
    self.count += General.get_count_value(card)

  def observe_number_of_decks_in_shoe(self, n_decks: int) -> None:
    '''
    The player is shown the number of decks in the shoe.
    This happens at the start of each shoe
    '''
    self.n_decks = n_decks

  def get_bet_amount(self) -> float:
    '''
    The player announces the bet amount for this round
    '''
    scale = self.get_true() + self.true_adjust
    bet = self.unit * floor(scale * self.unit + 0.5)
    if bet < self.minimum_bet:
      return self.minimum_bet
    if bet > self.maximum_bet:
      return self.maximum_bet
    return bet

  def receive_payoff(self, amount: float) -> None:
    '''
    The player receive the payoff for bet
    '''
    assert amount > 0.0
    self.bankrole += amount

  def set_minimum_bet(self, amount: float) -> None:
    '''
    The player is informed of the minimum bet size for this table.
    This happens once the player sits down at the table.
    '''
    self.minimum_bet = self.unit * ceil(amount / self.unit)

  def set_maximum_bet(self, amount: float) -> None:
    '''
    The player is informed of he maximum bet size for this table.
    This happens once the player sits down at he table.
    '''
    self.maximum_bet = self.unit * ceil(amount / self.unit)

  def get_true(self) -> float:
    '''
    Get the current value of the 'true' count
    '''
    decks_remaining = self.get_shoe_len() * self._cards_to_decks
    return self.count / decks_remaining

  def make_bet(self, amount: float) -> None:
    '''
    Money is taken from the Player and placed on a hand at the table.
    The system determines the bet amount and removes it from
    the player's bankrole.
    '''
    self.bankrole -= amount

  @staticmethod
  def test1(strategy_file_path) -> None:
    '''
    For testing purposes
    '''
    n_decks = 6

    shoe = General.get_shoe(n_decks)

    def get_shoe_len() -> int:
      'returns the length of the shoe'
      return len(shoe)

    counter = Counter(strategy_file_path)
    counter.set_get_shoe_len(get_shoe_len)

    # burn a card
    _ = shoe.pop()


    for _ in range(20):
      # player is dealt the first card
      card = shoe.pop()
      counter.observe_card(card)
      player_hand = [card]

      # dealer gets the second card face down
      dealer_hand = [shoe.pop()]

      # player gets the third card
      card = shoe.pop()
      counter.observe_card(card)
      player_hand.append(card)

      # dealer gets the last card face up
      upcard = shoe.pop()
      counter.observe_card(upcard)
      dealer_hand.append(upcard)

      print()
      print('dealer hand: "{0}"'.format(General.hand_to_face_string(dealer_hand)))
      print('upcard: "{0}"'.format(General.get_face_symbol(upcard)))
      print('player hand:', General.hand_to_face_string(player_hand))
      print('true: {0:.1f}'.format(counter.get_true()))

      # if the up-card is an ace then see if the player requests
      # insurance
      if counter.requests_insurance(player_hand, upcard):
        print('player requests insurance')
      else:
        print('player declines insurance')



# pylint: enable=R0902

if __name__ == '__main__':
  Counter.test1("strategy1.json")
