# Simulating Blackjack


## cards



A card is represented by a byte. The face index,
which can take the values 0 to 12 is contained in
the lowest four bits of the byte. The suit index
which can take the values 0 to 3 is contained in
the highest byte. The game of Blackjack is indifferent
to the value of a card's suit so the highest byte
will be ignored. Associated with each face is a symbol,
a value for Blackjack and a value for counting cards.
These associated values can be seen in the following
tables.

### faces

| face index | face symbol | face value | count value |
| :--------: | :---------: | :--------: | :---------: |
|     0      |     '2'     |     2      |   +1        |
|     1      |     '3'     |     3      |   +1        |
|     2      |     '4'     |     4      |   +1        |
|     3      |     '5'     |     5      |   +1        |
|     4      |     '6'     |     6      |   +1        |
|     5      |     '7'     |     7      |    0        |
|     6      |     '8'     |     8      |    0        |
|     7      |     '9'     |     9      |    0        |
|     8      |     'X'     |    10      |   -1        |
|     9      |     'J'     |    10      |   -1        |
|    10      |     'Q'     |    10      |   -1        |
|    11      |     'K'     |    10      |   -1        |
|    12      |     'A'     |    11*     |   -1        |

```python
face_symbols = ['2', '3', '4', '5', ... 'A']
face_values  = [ 2, 3, ... 11]
count_values = [ +1, +1, ... -1]
face_count = 13
suit_count = 4
assert(0 <= face_index < face_count)
assert(0 <= suit_index < suit_count)
card_value = face_index + 16 * suit_index
```

### suits

| suit index | suit symbol |
| :--------: | :---------: |
|     0      |   'H'       |
|     1      |   'D'       |
|     2      |   'C'       |
|     3      |   'S'       |
