'''
Insurance.py

I have my doubts about when making an insurance bet is justified.
This file contains the programs to settle the issue. This is
a partial implementation of blackjack. I will represent the set
of all cards by the integers 0..12 representing '2','3',..'A'.
I am not concerned with suit. In addition I shall assume the
traditional count values of the cards which are +1 for '2'..'6'
0 for '7'..'9' and -1 for 'X'..'A'. (I use 'X' as a single character
representation of a '10' card.)

I shall play a large number of shoes consisting of 6 decks each
with a one and a half deck cut. I have one player and one
dealer. When the dealer has an ace I shall record the 'true'
and whether the second dealer card is a 10.
'''

import sys
import math
import random
import numpy                      # pylint: disable=import-error
import matplotlib.pyplot as plt   # pylint: disable=import-error

class Card:
  '''
  A class that implemets the duties of a card. The duties include
  giving its count value, determining if the card is an ace or
  it has a blackjack value of ten
  '''
  # index    0    1    2    3    4    5    6    7    8    9    A    B    C
  #SUITS = ['2', '3', '4', '5', '6', '7', '8', '9', 'X', 'J', 'Q', 'K', 'A']
  COUNTS = [+1, +1, +1, +1, +1, 0, 0, 0, -1, -1, -1, -1, -1]
  def __init__(self, _index):
    self.index = _index
    self.count = Card.COUNTS[_index]
  def is_ace(self):
    'returns true if the card is an ace'
    return self.index == 12
  def is_value_equal_10(self):
    'returns true if the card is a ten, jack, queen or king'
    return 8 <= self.index < 12

class Shoe:
  '''
  A class implementing the duties of a shoe which in this case is dealing
  cards randomly until the cut card comes out and calculating the true
  given a player's belief of the count.
  '''
  def __init__(self, n_decks, fCut=1.5):
    assert n_decks > 0
    self.n_decks = n_decks
    self.indices = list(range(0, 13)) * (4 * n_decks)
    random.shuffle(self.indices)
    self.cut = int(52*fCut + .05)
  def more(self):
    '''
    Return true if the cut card has not come out
    '''
    return len(self.indices) > self.cut
  def deal(self):
    '''
    Remove one card number from the list, create a card, return it
    '''
    return Card(self.indices.pop())
  def get_true(self, count):
    '''
    The 'true' is equal to the count divided the the number of undealt decks
    '''
    return (52*count) / len(self.indices)

def insurance(shoe, count, recorder):
  '''
  Deals four cards from the shoe which corresponds to two to the player
  and two to the dealer. The count is initially adjusted for three of
  the cards. The fourth card corresponds to the dealer's down card
  so the player does not see it and thus does not initally affect the
  count. The true count is calcualted after the three cards has
  been seen. If if the dealer's upcard, which is part of the visible
  three, is an ace then we have the possibility of a dealer blackjack.
  In this case, the true count is recorded. The the uncounted card
  , the downcard, is revealed to see if it has a blackjack value
  of 10 and thus the dealer has a blackjack. If the dealer has
  a blackjack then a loss of 1 is recorded otherwise a win of 2
  is recorded simulating the result of an insurance bet being made.
  Finally, the count is adjusted for the downcard. The true count and
  insurance bet result are recorded by calling the recorder function.
  The updated count is returned to the caller.
  '''
  cards = [shoe.deal(), shoe.deal(), shoe.deal(), shoe.deal()]
  counts = [card.count for card in  cards]
  count += sum(counts[:3])
  if cards[2].is_ace():
    etrue = shoe.get_true(count)
    if cards[3].is_value_equal_10():
      win = 2 # dealer blackjack, insurance bet pays off 2:1
    else:
      win = -1 # no dealer blackjack, insurace bet is lost
    recorder((etrue, win))
  count += counts[3]
  return count

def play_shoe(recorder, n_decks=6):
  '''
  Simulate a single shoe for the purpose of observing insurance opportunities.
  If such an opportunity is observed it is recored with a recorder function.
  '''
  shoe = Shoe(n_decks)
  count = 0
  while shoe.more():
    count = insurance(shoe, count, recorder)

def analyze_true(results, tmin, recorder):
  '''
  Iterate over the insurance results looking for insurance opportunities
  where the observed true is greater than equal to the minimum value
  of true for which making the insurance bet is justified. Calculate
  the average and standard deviation of the results per unit
  insurance bet and report it by calling recorder function.
  '''
  ntotal = 0
  win1 = 0
  win2 = 0
  for (etrue, win) in results:
    if etrue >= tmin:
      ntotal += 1
      win1 += win
      win2 += win*win
  if ntotal <= 0:
    return
  e_win1 = win1 / ntotal
  e_win2 = win2 / ntotal
  var = e_win2 - e_win1 * e_win1    # variance
  std = math.sqrt(var)  # standard deviation
  recorder((tmin, e_win1, std))

def analyze_results(results, start, stop):
  '''
  Analyze the results of the insurance data for set of minimum critical
  values of true. Plot the results where the x-axis is the critical
  true and the y-axis is the expected return on an accepted unit
  insurance bet.
  '''
  step = +0.5
  tmin_s = []
  win_s = []
  def my_recorder(result):
    tmin, avg, _ = result
    tmin_s.append(tmin)
    win_s.append(avg)
  tmins = numpy.arange(start, stop, step)
  for tmin in tmins:
    analyze_true(results, tmin, my_recorder)

  plt.scatter(tmin_s, win_s)
  plt.grid(True)
  plt.xlabel("minimum true")
  plt.ylabel("expected win")
  plt.axes().set_xticks(numpy.arange(start, stop, 2*step))
  plt.title("expected insurance result vs minimum true")
  plt.show()

def run(n_shoes, start, stop):
  '''
  Simulates n_shoes of 6 deck blackjack looking for insurance opportunities.
  The start and stop are the ranges of critical true values.
  '''
  results = []
  def a_recorder(result):
    results.append(result)
  for _ in range(n_shoes):
    play_shoe(a_recorder)
  analyze_results(results, start, stop)

def main():
  'main entry point: args = n_shoes start stop'
  try:
    n_shoes = int(sys.argv[1])
    start = float(sys.argv[2])
    stop = float(sys.argv[3]) + .1
    run(n_shoes, start, stop)
  except Exception: # pylint: disable=broad-except
    print()
    print("Analyze insurance bets")
    print()
    print("  Syntax:")
    print()
    print("    > python insurance.py n_shoes start stop")
    print()
    print("    eg.")
    print()
    print("    > python insurance.py 10000 -5.0 +5.1")
    print()

if __name__ == '__main__':
  main()
