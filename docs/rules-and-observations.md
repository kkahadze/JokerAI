# Rules and environment contract

This package implements the repository's four-player, 36-card Joker variant. It
is a research environment, not a claim to implement every regional rule.

## Physical cards, deals and bidding

There are 7–ace of each suit, the sixes of diamonds/hearts, and two physical
Jokers. Physical Jokers use `Card(16, 0)` and `Card(16, 1)` internally; their suits
are identities, not actual suit obligations. Both encode as 34 in a hand. A
Joker declaration consumes exactly one of those physical cards.

The 24 deals are 1–8, four 9s, 8–1, then four 9s. `only_nines=True` instead uses
16 nine-card deals. Either schedule contains 144 tricks. Dealer rotates after
each deal. Bidding and the first trick begin at the seat after the dealer; each
later trick is led by its winner. The dealer calls last and cannot make the sum
of bids equal the number of tricks available. All bids, including seat zero's,
are chosen by baseline policies; the environment's action controls card play.

Trump is the first undealt card's suit, or no trump if that card is a Joker or
the deck is empty. Nine-card deals have no trump; player-selected trump and
section bonuses are not implemented.

## Card actions

Suits 0–3 are diamonds, clubs, hearts, spades. Suit 4 means no suit/trump.

| Action | Meaning |
| --- | --- |
| 0, 1 | Six of diamonds, six of hearts |
| 2–33 | 7–ace, ordered by rank then suit: `(rank - 7) * 4 + suit + 2` |
| 34 | Following Joker played high |
| 35 | Following Joker played low, with no suit |
| 36–39 | Leading Joker played low, requesting suit `action - 36` |
| 40–43 | Leading Joker played high, requesting suit `action - 40` |
| 44 | Observation padding only; never an action |

Follow the led/requested suit if possible, otherwise trump if possible,
otherwise any ordinary card. A Joker is always an alternative. After a high
Joker lead, a player with the requested suit must play their highest ordinary
card of that suit or a Joker. Legal Joker leads are 36–43; legal following Joker
plays are 34–35.

The last following high Joker wins. Without one, a leading high Joker wins.
Otherwise the highest trump wins, then the highest led/requested-suit card. A
leading low Joker has rank 5 in its requested suit; a following low Joker loses
to ordinary cards. The first equal-ranked ordinary card wins a tie (physical
ordinary cards are unique in actual games).

## Scores and reward

An exact bid earns `50 * taken + 50`, except calling and taking every trick earns
`100 * taken`. Missing a call earns `10 * taken`, unless a positive call takes
zero, which loses 200. An exact zero earns 50. Scores accumulate across deals.

Valid nonterminal steps receive 0. At termination, seat zero receives 1 for
highest score, including ties, and 0 otherwise. An unavailable but in-range
action receives −1 without advancing the game. These reward semantics are
separate from game scores, which are returned in the observation and info.

## Observations and info

Each reset and step returns fresh data. Array fields use NumPy int64.

| Field | Shape / values |
| --- | --- |
| `player0hand` | (9,), ordinary card codes or 34 for a physical Joker; padded with 44 |
| `in_play` | (3,), prior actions in play order; padded with 44 |
| `dealt` | 1–9 while active, 0 at termination |
| `round`, `play` | Section 1–4, deal 1–8; terminal section 5, deal 1 |
| `first_to_play`, `dealer` | Seat IDs 0–3 |
| `wild_suit`, `first_suit` | 0–3 or 4 for no suit |
| `jokers_remaining` | 0–2: physical Jokers still held by players, excluding undealt cards |
| `playerNdesired`, N=0–3 | Bid 0–9; −1 is used internally before a bid is made |
| `playerNtaken`, N=0–3 | Tricks won this deal, 0–9 |
| `scores` | (4,), cumulative scores; declared space bounds −100000 to 100000 |

`info['action_mask']` is an int8 array of length 44. Ones identify legal actions;
it is all zero at termination. `info['scores']` is a fresh list of four cumulative
scores. The observation excludes opponents' hands. `render_mode='ansi'` returns
a text view of the public state and seat zero's hand.
