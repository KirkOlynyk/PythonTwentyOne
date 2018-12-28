'''
hand.py
'''

class Hand:
  '''
Each hand contains a set of cards and a wager.
  '''
  def __init__(self):
    self.reset()

  def reset(self):
    self.__cards = ''
    self.__bet = 0.0
    self.__insurance_bet = 0.0

  @property
  def cards(self):
    return self.__cards

  @cards.setter
  def cards(self, x):
    self.__cards = x

  @property
  def bet(self):
    return self.__bet

  @bet.setter
  def bet(self, x):
    self.__bet = x

  @property
  def insurance_bet(self):
    return self.__insurance_bet

  @insurance_bet.setter
  def insurance_bet(self, x):
    self.__insurance_bet = x

