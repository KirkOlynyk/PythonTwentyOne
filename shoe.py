'''
table.py

This file implements the rules of the casino and runs
the blackjack game
'''
import random
import rules

class Shoe:
  def __init__(self, n_decks, seed=0):
    random.seed(seed)
    self.shoe = list(rules.CARD_FACES * (n_decks * rules.SUITS_PER_DECK))
    random.shuffle(self.shoe)

  def get_card(self):
    return self.shoe.pop(0)

if __name__ == '__main__':
  n_decks = 6
  seed = 23
  shoe = Shoe(n_decks=n_decks, seed=seed)
  ans = ''
  for i in range(10):
    ans += shoe.get_card()
  print(ans)
