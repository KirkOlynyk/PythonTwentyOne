'''
rules.py

A compendium of blackjack rules and numbers
'''

from typing import Tuple

CARDS_PER_SUIT = 13
SUITS_PER_DECK = 4
CARDS_PER_DECK = CARDS_PER_SUIT * SUITS_PER_DECK

CARD_VALUES = {
    "2" : 2, "3" : 3, "4" : 4, "5" : 5, "6" : 6, "7" : 7, "8" : 8, "9" : 9,
    "X" : 10, "A" : 1 
  }

CARD_INDEXES = {
  "2" : 0, "3" : 1, "4" : 2, "5" : 3, "6" : 4, "7" : 5, "8" : 6, "9" : 7,
  "X" : 8, "A" : 9 
}

CARD_FACES = "23456789XXXXA"

HAND_VALUE = Tuple[int, bool]

def hand_value(cards:str) -> HAND_VALUE:
  '''
  Returns the value of a hand

  cards is a string with the alphabet of '23456789XA'

  If the hand is soft the higher value is returned.
  The return value is a pair consisting of the
  value and the softness.
  '''
  total = 0
  has_aces = False
  for face in cards:
    card_value = CARD_VALUES[face]
    if card_value == 1:
      has_aces = True
    total += card_value
  if total <= 11 and has_aces:
    return total + 10, True
  else:
    return total, False
