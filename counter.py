'''
counter.py

Defines the Counter class for a blackjack counter
'''

import json
import shoe
from math import floor
from player import Player
from rules import CARDS_PER_DECK, \
                  CARD_VALUES,    \
                  hand_value,     \
                  CARD_INDEXES

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
    Implements the Player interface function.

    The player has won the wager. This is the
    return of the win along with the original wager
    '''
    self._bankrole += amount

  def get_bet_amount(self) -> float:
    '''
    Implements the Player interface function.
    Get the desire bet amount. Do not take
    any money from the bankrole, that is
    done with make_bet
    '''
    scale = self._true_count + self._true_adjust
    wager = self._unit * floor(scale + 0.5)
    if wager < self._minimum_bet:
      wager = self._minimum_bet
    elif wager > self._maximum_bet:
      wager = self._maximum_bet
    if wager < self._unit:
      wager = self._unit
    return wager

  def make_bet(self, wager:float) -> None:
    '''
    Required by the Player interface
    '''
    self._bankrole -= wager
    return wager

  def _accepts(self, cards:str, upcard:str, table) -> bool:
    assert len(cards) == 2
    try:
      hand = self._handsort(cards)
      updex = self._upcard_index[upcard]
      decision = table[hand][updex]
      return self._true_count >= decision
    except KeyError:
      return False

  def accepts_insurance(self, cards : str, upcard : str) -> bool:
    '''
    Implements the Player interface function.
    
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
    'Required by the Player interface'
    return self._accepts(cards, upcard, self._surrender)

  def accepts_split(self, cards:str, upcard:str) -> bool:
    'Required by the Player interface'
    return self._accepts(cards, upcard, self._split)

  def accepts_double(self, cards:str, upcard:str) -> bool:
    'Required by the Player interface'
    return self._accepts(cards, upcard, self._double)

  def accepts_stand(self, cards:str, upcard:str) -> bool:
    'Required by the Player interface'
    value, soft = hand_value(cards)
    if soft:
      table = self._soft_stand
    else:
      table = self._hard_stand
    try:
      updex = self._upcard_index[upcard]
      decision = table[str(value)][updex]
      return self._true_count >= decision
    except KeyError:
      return False

  def show_card(self, card : str) -> None:
    'The player sees a card that has been dealt to the table'
    print('counter sees', card)
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

def test0() -> None:
  'Just at test'
  # Set everything done
  counter = Counter('strategy1.json')
  counter.show_decks_in_shoe(6)
  counter.set_minimum_bet(100.0)
  counter.set_maximum_bet(3000.0)

  print('counter-bankrole:', counter._bankrole)

  #play a round
  # deal the cards
  counter.show_card('A')                    # up-card
  counter.show_card('X')                    # player card
  counter.show_card('X')                    # player card
  
  # what is the true?
  print("true-count: {0:.1f}".format(counter._true_count))
  bet = counter.get_bet_amount()
  counter.make_bet(bet)
  print("counter-bet:", bet)
  print("couter-bankrole:", counter._bankrole)

  # the player gets two tens
  cards = 'XX'
  # the dealer has an up-card
  up_card = 'A'
  # a hand is a values sorted string of cards
  hand = counter._handsort(cards)
  # print the original string of cards and then the sorted cards of the hand
  print('counter-hand:', hand)
  print('up-card:', up_card)

  if counter.accepts_insurance(cards, up_card):
    print("counter accepts insurance")
  else:
    print("counter declines insurance")

  if counter.accepts_split(cards, up_card):
    print("counter accepts split")
  else:
    print("counter declines split")

  if counter.accepts_double(cards, up_card):
    print("player accepts double")
  else:
    print("player declines double")

  if counter.accepts_stand(cards, up_card):
    print("player accepts stand")
  else:
    print("player declines stand")

class Table:
  '''
  Each table is a list of Places
  '''
  def __init__(self, n_places, n_decks, seed, decks_cut):
    cards_cut = int(CARDS_PER_DECK * decks_cut + 0.5)
    n_cards_per_shoe = n_decks * CARDS_PER_DECK
    self.n_decks = n_decks
    self.cut_number = n_cards_per_shoe - cards_cut
    self.places = [Place() for i in range(n_places)]
    self.shoe = shoe.Shoe(n_decks=n_decks, seed = seed)
    self.n_cards_dealt = 0
    self.players = []

  def burn_card(self):
    _ = self.shoe.get_card()

  def sit_down(self, i_place, player):
    self.players.append(player)
    self.places[i_place].occupy(player)

  def show_number_of_decks_in_shoe_to_all_players(self):
    for place in self.places:
      if place.player != None:
        place.player.show_decks_in_shoe(self.n_decks)

  def make_players_bet(self):
    for place in self.places:
      player = place.player
      if player != None:
        assert len(place.hands) == 1
        hand = place.hands[0]
        hand.bet = player.get_bet_amount()
        player.make_bet(hand.bet)

  def show_card_to_all_players(self, card):
    for player in self.players:
      player.show_card(card)

  def deal_one_card_to_each_place(self):
    for place in self.places:
      player = place.player
      if player != None:
        assert len(place.hands) == 1
        card = self.shoe.get_card()
        hand = place.hands[0]
        hand.cards += card
        self.show_card_to_all_players(card)
    
  def deal_down_card(self):
    self.hand = self.shoe.get_card()

  def deal_up_card(self):
    self.upcard = self.shoe.get_card()
    self.hand += self.upcard
    self.show_card_to_all_players(self.upcard)

  def play_hand(self, player, hand):
    print('hand.bet', hand.bet)
    print('hand.cards', hand.cards)
    if self.upcard == 'A':
      if player.accepts_insurance(hand.cards, self.upcard):
        print('insurcance accepted')
    if player.accepts_surrender(hand.cards, self.upcard):
      print('surrender accepted')
    else:
      print('surrender declined')
    if player.accepts_split(hand.cards, self.upcard):
      print('split accepted')
    else:
      print('split declined')
    if player.accepts_double(hand.cards, self.upcard):
      print('double accepted')
    else:
      print('double declined')
    if player.accepts_stand(hand.cards, self.upcard):
      print('stand accepted')
    else:
      print('stand declined')

  def play_each_place(self):
    for index, place in enumerate(self.places):
      player = place.player
      if player != None:
        print("{0}:".format(index))
        for hand in place.hands:
          self.play_hand(player, hand)

  def play_round(self):
    self.hand = ''
    self.show_number_of_decks_in_shoe_to_all_players()
    self.make_players_bet()
    self.burn_card()
    self.deal_one_card_to_each_place()
    self.deal_down_card()
    self.deal_one_card_to_each_place()
    self.deal_up_card()
    self.play_each_place()

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

class Hand:
  '''
Each hand contains a set of cards and a wager.
  '''
  def __init__(self):
    self.cards = ''
    self.bet = 0.0

def test1():
  n_places = 1
  seed = 1
  n_decks = 6
  decks_cut = 1.5

  table = Table(n_places=n_places, n_decks=n_decks, seed = seed, decks_cut = decks_cut)
  counter = Counter(json_file_path="strategy1.json")
  table.sit_down(i_place=0, player=counter)
  table.play_round()

  print(table)
  print(counter)

if __name__ == '__main__':
  test1()
