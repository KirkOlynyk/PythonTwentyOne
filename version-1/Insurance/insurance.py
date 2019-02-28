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

import math
import random
import numpy
import matplotlib.pyplot as plt

class Card:
  # index   0    1    2    3    4    5    6    7    8    9    A    B    C
  SUITS = ['2', '3', '4', '5', '6', '7', '8', '9', 'X', 'J', 'Q', 'K', 'A']
  COUNTS = [+1, +1, +1, +1, +1, 0, 0, 0, -1, -1, -1, -1, -1]
  def __init__(self, _index):
    self.index = _index
    self.count = Card.COUNTS[_index]
  def __repr__(self):
    return Card.SUITS[self.index]

class Shoe:
  def __init__(self, n_decks, fCut=1.5):
    assert n_decks > 0
    self.n_decks = n_decks
    self.cards = list(range(0, 13)) * (4 * n_decks)
    random.shuffle(self.cards)
    self.cut = int(52*fCut + .05)
  def more(self):
    return len(self.cards) > self.cut
  def deal(self):
    return Card(self.cards.pop())
  def get_true(self, count):
    return (52*count) / len(self.cards)

def insurance(shoe, count, recorder):
  cards = [shoe.deal(), shoe.deal(), shoe.deal(), shoe.deal()]
  indexes = [card.index for card in cards]
  counts = [card.count for card in  cards]
  count += sum(counts[:3])
  if indexes[2] == 12: #does the dealer show an ace?
    etrue = shoe.get_true(count)
    if 8 <= indexes[3] <= 11: # does the dealer have a blackjack?
      win = 2 # dealer blackjack, insurance bet pays off 2:1
    else:
      win = -1 # no dealer blackjack, insurace bet is lost
    recorder((etrue, win))
  count += counts[3]
  return count

def play_shoe(recorder, n_decks=6):
  shoe = Shoe(n_decks)
  count = 0
  while shoe.more():
    count = insurance(shoe, count, recorder)

def analyze_true(results, tmin, recorder):
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

def analyze_results(results):
  tmin_s = []
  win_s = []
  def my_recorder(result):
    tmin, avg, _ = result
    tmin_s.append(tmin)
    win_s.append(avg)
  tmins = numpy.arange(-5.0, +15.2, +0.5)
  for tmin in tmins:
    analyze_true(results, tmin, my_recorder)
  plt.scatter(tmin_s, win_s)
  plt.grid(True)
  plt.xlabel("minimum true")
  plt.ylabel("expected win")
  plt.title("expected insurance result vs minimum true")
  plt.show()
  

if __name__ == '__main__':
  N_SHOES = 10 * 1000 * 1000
  RESULTS = []
  def a_recorder(result):
    RESULTS.append(result)
  for _ in range(N_SHOES):
    play_shoe(a_recorder)
  analyze_results(RESULTS)
