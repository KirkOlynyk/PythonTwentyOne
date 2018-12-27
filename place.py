'''
place.py
'''
from hand import Hand

class Place:
  '''
Each place may or may not have a Player.

If a place has a player then the Place 
must start with a Hand with an associated bet.
  '''
  def __init__(self):
    self.player = None
    self.hand = None
  def occupy(self, player):
    self.player = player
    self.hands = [Hand()]


