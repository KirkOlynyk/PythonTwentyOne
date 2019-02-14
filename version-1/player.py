'''
player.py

Defines the interface for a blackjack player.
'''

import abc
from general import CARD, HAND, SHOE

class Player(abc.ABC):
  'Player interface definition'

  @abc.abstractclassmethod
  def set_get_shoe_len(cls, get_shoe_len) -> None:
    '''
    Give the player a function to get the number of
    undealt cards in the shoe
    '''

  @abc.abstractclassmethod
  def requests_insurance(cls, hand: HAND, upcard: CARD) -> bool:
    '''
    The dealer is asking the player if the hand should be insured
    '''

  @abc.abstractclassmethod
  def requests_surrender(cls, hand: HAND, upcard: CARD) -> bool:
    '''
    The dealer is asking the player if the hand should be surrendered
    '''

  @abc.abstractclassmethod
  def requests_split(cls, hand: HAND, upcard: CARD) -> bool:
    '''
    The dealer is asking the player if the hand should be split
    '''

  @abc.abstractclassmethod
  def requests_double(cls, hand: HAND, upcard: CARD) -> bool:
    '''
    The dealer is asking the player if the bet on the hand should be doubled
    '''

  @abc.abstractclassmethod
  def requests_stand(cls, hand: HAND, upcard: CARD) -> bool:
    '''
    The dealer is asking the player if the hand should stand
    i.e. no more cards are to be added
    '''

  @abc.abstractclassmethod
  def observe_card(cls, card: CARD) -> None:
    '''
    The newly dealt card is shown to the player
    '''

  @abc.abstractclassmethod
  def observe_number_of_decks_in_shoe(cls, n_decks: int) -> None:
    '''
    The player is shown the number of decks in the shoe.
    This happens at the start of each shoe
    '''

  @abc.abstractclassmethod
  def get_bet_amount(cls) -> float:
    '''
    The player announces the bet amount for this round
    '''

  @abc.abstractclassmethod
  def receive_payoff(cls, amount: float) -> None:
    '''
    The player receive the payoff for bet
    '''

  @abc.abstractclassmethod
  def set_minimum_bet(cls, amount: float) -> None:
    '''
    The player is informed of the minimum bet size for this table.
    This happens once the player sits down at the table.
    '''

  @abc.abstractclassmethod
  def set_maximum_bet(cls, amount: float) -> None:
    '''
    The player is informed of he maximum bet size for this table.
    This happens once the player sits down at he table.
    '''

  @abc.abstractclassmethod
  def make_bet(cls, amount: float) -> None:
    '''
    Money is taken from the Player and placed on a hand at the table.
    The system determines the bet amount and removes it from
    the player's bankrole.
    '''
