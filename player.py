'''
player.py 

Defines the interface for a blackjack player
'''

import abc

class Player(abc.ABC):
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
  def show_decks_in_shoe(self, decks_in_shoe : int) -> None:
    pass
  @abc.abstractclassmethod
  def get_bet(self) -> float:
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
  @abc.abstractclassmethod
  def place_insurance_bet(self, amount:float) -> None:
    pass
