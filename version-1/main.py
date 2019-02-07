'main.py'
from typing import List, Tuple
Card = int
FaceValue = int
Hand = List[Card]
Softness = bool
BjValue = Tuple[int, Softness]

# pylint: disable=R0903
class General:
  'general useful stuff'
  face_symbols = '23456789XJQKA'
  face_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
  count_values = [+1, +1, +1, +1, +1, 0, 0, 0, -1, -1, -1, -1, -1]
  suit_symbols = 'HDCS'

  @staticmethod
  def face_index(card) -> int:
    'returns the face index of a card'
    return card & 0xF

  @staticmethod
  def get_face_symbol(card) -> str:
    'return the symbol for the face of a card'
    return General.face_symbols[General.face_index(card)]

  @staticmethod
  def get_suit_symbol(card) -> str:
    'return the symbol of the card suit'
    return General.suit_symbols[General.suit_index(card)]

  @staticmethod
  def get_count_value(card) -> int:
    'return the count value of the card'
    return General.count_values[General.face_index(card)]

  @staticmethod
  def suit_index(card) -> int:
    'returns the suit index of a card'
    return (card >> 4) & 0xF

  @staticmethod
  def face_value(card: Card) -> int:
    'returns the face falue of a card'
    _face_index = General.face_index(card)
    return General.face_values[_face_index]

  @staticmethod
  def get_card(suit_index: int, face_index: int) -> Card:
    '''
    Returns an card number for the given suit and face
    '''
    assert 0 <= suit_index < 4
    assert 0 <= face_index < 13
    return (suit_index << 4) + face_index

  @staticmethod
  def get_deck() -> List[Card]:
    'returns a deck of 52 cards'
    return [General.get_card(suit, face) for suit in range(4) for face in range(13)]

  @staticmethod
  def get_bj_value(my_face_values: List[FaceValue]) -> BjValue:
    '''
    Returns the Blackjack value of the hand
    as represented by a list of face values
    in the range 0 .. 11. The return value consists
    of an integer-boolean pair where the integer
    is the blackjack value of the hand and the
    boolean indicates whether the hand is soft.
    '''
    is_soft = False
    hand_value = 0
    for face_value in my_face_values:
      hand_value += face_value
      if is_soft:
        if face_value == 11:
          if hand_value > 21:
            hand_value -= 10
          if hand_value > 21:
            hand_value -= 10
            is_soft = False
        else:
          if hand_value > 21:
            hand_value -= 10
            is_soft = False
      else:
        if face_value == 11:
          if hand_value > 21:
            hand_value -= 10
          else:
            is_soft = True
    return (hand_value, is_soft)

  @staticmethod
  def bj_value(hand: Hand) -> BjValue:
    '''
    Returns the Blackjack value of a hand which is an
    integer-boolean pair where the integer positive
    and the boolean indicates whether the integer
    value is 'soft'.
    '''
    return General.get_bj_value([General.face_value(card) for card in hand])

def main() -> None:
  'main entry point'
  import random
  shoe = []
  for _ in range(6):
    shoe.extend(General.get_deck())
  random.shuffle(shoe)
  count = 0
  low = 0
  high = 0
  for card in shoe:
    count_value = General.get_count_value(card)
    count += count_value
    if count < low:
      low = count
    if count > high:
      high = count
  print("low:", low)
  print("high:", high)

if __name__ == '__main__':
  main()
