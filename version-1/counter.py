'''
counter.py

Implments the Player inteface
'''

from general import CARD, HAND, General
from player import Player

class Counter(Player):
  '''
  Card counter class
  '''
  _cards_to_decks = 1.0 / 52.0

  def __init__(self, strategy_file_path: str, unit: float) -> None:
    '''
    Constructor for the Counter class
    '''
    self.strategy_file_path = strategy_file_path
    self.n_cards_dealt = 0
    self.n_decks = 0
    self.count = 0
    self.unit = unit
    self.minimum_bet = 0.0
    self.maximum_bet = 0.0
    self.bankrole = 0.0

  def requests_insurance(self, hand: HAND, upcard: CARD) -> bool:
    '''
    The dealer is asking the player if the hand should be insured
    '''
    return False

  def requests_surrender(self, hand: HAND, upcard: CARD) -> bool:
    '''
    The dealer is asking the player if the hand should be surrendered
    '''
    return False

  def requests_split(self, hand: HAND, upcard: CARD) -> bool:
    '''
    The dealer is asking the player if the hand should be split
    '''
    return False

  def requests_double(self, hand: HAND, upcard: CARD) -> bool:
    '''
    The dealer is asking the player if the bet on the hand should be doubled
    '''
    return False

  def requests_stand(self, hand: HAND, upcard: CARD) -> bool:
    '''
    The dealer is asking the player if the hand should stand
    i.e. no more cards are to be added
    '''
    return False

  def observe_card(self, card: CARD) -> None:
    '''
    The newly dealt card is shown to the player
    '''
    self.n_cards_dealt += 1
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
    return 0.0

  def receive_payoff(self, amount: float) -> None:
    '''
    The player receive the payoff for bet
    '''

  def set_minimum_bet(self, amount: float) -> None:
    '''
    The player is informed of the minimum bet size for this table.
    This happens once the player sits down at the table.
    '''
    self.minimum_bet = amount

  def set_maximum_bet(self, amount: float) -> None:
    '''
    The player is informed of he maximum bet size for this table.
    This happens once the player sits down at he table.
    '''
    self.maximum_bet = amount

  def _get_true(self) -> float:
    '''
    Get the current value of the 'true' count
    '''
    decks_remaining = float(self.n_decks) \
                             - self._cards_to_decks * self.n_cards_dealt
    true = self.count / decks_remaining
    return true

  def make_bet(self, amount: float) -> None:
    '''
    Money is taken from the Player and placed on a hand at the table.
    The system determines the bet amount and removes it from
    the player's bankrole.
    '''

  def unobservable_card_dealt(self) -> None:
    '''
    Inform the player that a card as been dealt and will not
    be made visible
    '''
    self.n_cards_dealt += 1


  @staticmethod
  def test1(strategy_file_path) -> None:
    '''
    For testing purposes
    '''
    counter = Counter(strategy_file_path, unit=100.0)
    print(counter)

if __name__ == '__main__':
  Counter.test1("strategy1.json")
