'''
table.py
'''

from rules import CARDS_PER_DECK, is_blackjack
from shoe import Shoe
from counter import Counter
from place import Place
from hand import Hand

class Table:
  '''
  Each table is a list of Places
  '''
  def __init__(self, n_places, n_decks, seed, decks_cut):
    '''
    This initializes the table. The number of decks
    in the shoe, the numbe of places at the table and
    the cut depth are esablished. No players are
    seated yet.
    '''
    cards_cut = int(CARDS_PER_DECK * decks_cut + 0.5)
    n_cards_per_shoe = n_decks * CARDS_PER_DECK
    self.n_decks = n_decks
    self.cut_number = n_cards_per_shoe - cards_cut
    self.places = [Place() for i in range(n_places)]
    self.shoe = Shoe(n_decks=n_decks, seed = seed)
    self.n_cards_dealt = 0
    self.players = []

  def burn_card(self):
    '''
    This is the first card that comes off a shuffled shoe.
    It is dicarded without showing it to the players
    '''
    _ = self.shoe.get_card()

  def sit_down(self, i_place, player):
    self.players.append(player)
    self.places[i_place].occupy(player)

  def show_decks(self):
    for place in self.places:
      if place.player != None:
        place.player.show_decks_in_shoe(self.n_decks)

  def make_bets(self):
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

  def deal_places(self):
    for place in self.places:
      player = place.player
      if player != None:
        assert len(place.hands) == 1
        card = self.shoe.get_card()
        hand = place.hands[0]
        hand.cards += card
        self.show_card_to_all_players(card)
    
  def deal_down_card(self):
    self.downcard = self.shoe.get_card()
    self.hand = self.downcard

  def deal_up_card(self):
    self.upcard = self.shoe.get_card()
    self.hand += self.upcard
    self.show_card_to_all_players(self.upcard)

  def play_hand(self, player, place, hand):
    '''
    If the hand is a blackjack then it is
    immediately payed off and taken from the 
    place
    '''
    print('hand.bet', hand.bet)
    print('hand.cards', hand.cards)
    if self.upcard == 'A':
      if player.accepts_insurance(hand.cards, self.upcard):
        self.process_insurance(player, place, hand)
    if player.accepts_surrender(hand.cards, self.upcard):
      self.process_surrrender(player, place, hand)
      return
    if player.accepts_split(hand.cards, self.upcard):
      self.process_split(player, place, hand)
    if player.accepts_double(hand.cards, self.upcard):
      self.process_double(player, place, hand)
    if player.accepts_stand(hand.cards, self.upcard):
      self.process_stand(player, place, hand)
    else:
      self.process_hit(player, place, hand)

  def process_insurance(self, player, place, hand):
    print('insurance')

  def process_surrrender(self, player, place, hand):
    print('surrender')

  def process_split(self, player, place, hand):
    print('split')

  def process_stand(self, player, place, hand):
    print('stand')

  def process_hit(self, player, place, hand):
    print('hit')

  def process_double(self, player, place, hand):
    print('double')

  def play_place(self, place):
    player = place.player
    if player != None:
      for hand in place.hands:
        self.play_hand(player, place, hand)

  def play_each_place(self):
    for place in self.occupied_places():
      self.play_place(place)

  def occupied_places(self):
    for place in self.places:
      if place.player != None:
        yield place

  def players_take_insurance(self):
    for place in self.occupied_places():
      assert len(place.hands) == 1
      player = place.player
      hand = place.hands[0]
      cards = hand.cards
      if player.accepts_insurance(cards, self.upcard):
        hand.insurance_bet = 0.5 * hand.bet
        player.make_bet(hand.insurance_bet)

  def dealer_blackjack_ace_up(self):
    assert self.upcard == 'A'
    print('dealer has a blackjack ace up')
    for place in self.occupied_places():
      assert len(place.hands) == 1
      hand = place.hands[0]
      player = place.player
      if hand.insurance_bet != 0.0:
        player.receive_payoff(2 * hand.insurance_bet)
      if hand.is_blackjack():
        player.receive_payoff(hand.bet) # push

  def dealer_blackjack_ten_up(self):
    assert self.upcard == 'X'
    print('dealer has a blackjack ten up')
    for place in self.occupied_places():
      assert len(place.hands) == 1
      player = place.player
      hand = place.hands[0]
      assert hand.insurance_bet == 0.0
      if hand.is_blackjack():
        player.receive_payoff(hand.bet) # push

  def reset_places(self):
    for place in self.occupied_places():
      place.hands = [Hand()]

  def play_round(self):
    self.hand = ''
    self.make_bets()
    self.burn_card()
    self.deal_places()
    self.deal_down_card()
    self.deal_places()
    self.deal_up_card()
    if self.upcard == 'A':
      self.players_take_insurance()
      if self.downcard == 'X':
        self.dealer_blackjack_ace_up()
        self.reset_places()
        return
    elif self.upcard == 'X':
      if self.downcard == 'A':
        self.dealer_blackjack_ten_up()
        self.reset_places()
        return
    self.play_each_place()

def test():
  n_places = 1
  seed = 1
  n_decks = 6
  decks_cut = 1.5

  table = \
    Table(
      n_places=n_places,
      n_decks=n_decks,
      seed = seed, 
      decks_cut = decks_cut
    )
  counter = Counter(json_file_path="strategy1.json")
  table.sit_down(i_place=0, player=counter)
  table.show_decks()
  table.play_round()

if __name__ == '__main__':
  test()
