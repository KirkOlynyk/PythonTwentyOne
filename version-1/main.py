'main.py'

from typing import Iterable
import matplotlib.pyplot as plt
from general import General, SHOE

def get_counts(shoe: SHOE) -> Iterable[int]:
  'returns a sequence of observed card counter counts for a shoe'
  count = 0
  for card in shoe:
    count += General.get_count_value(card)
    yield count

def plot_shoe_trues(seed: int = None) -> None:
  'display a plot of the true count for a random shoe'
  n_decks = 6
  shoe = General.get_shoe(n_decks=n_decks, seed=seed)
  card_counts = list(get_counts(shoe))
  observed_counts = card_counts[:int(52 * (float(n_decks) - 1.5))]
  scale = 1.0/52.0
  trues = []
  for i_card, count in enumerate(observed_counts):
    decks_remaining = float(n_decks) - scale * (i_card + 1)
    true = count / decks_remaining
    trues.append(true)
  _, axes = plt.subplots()
  axes.plot(list(range(len(observed_counts))), trues)
  axes.set(xlabel='card number', ylabel='true', title='observed true values')
  # _, _, _ = plt.hist(observed_counts, bins=[x + 0.5 for x in list(range(-20, 21))])
  plt.grid(True)
  plt.show()

def main() -> None:
  'main entry point'
  plot_shoe_trues()

if __name__ == '__main__':
  main()
