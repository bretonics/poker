# Poker Game

Just practical implementation. Must use Python 3.

Cards are  represented by their number or first letter for the non-numeric cards (J, Q, K, A) and the suits by their first letter (H, C, D, S), stored as a JSON array.


1. Determines your hand. (pre-defined)
2. Determines winner between 2 5-card hands (asks user)
3. Return best 5-card hand

Example
---
    $ python3 poker.py

    Using hand: ['JH', '4C', '4S', 'JC', '9H']

    You have a Two Pair!
    Kicker: J


    Enter your 5-card poker hand in [JSON format]: not JSON

    [X] Not a JSON input! Try again.

    Enter your 5-card poker hand in [JSON format]: ["9C", "7C", "5C", "6C", "10C"]

    You have a Flush!

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Let's play another round.

    Who will the winner be? Enter your hands...


    Enter first 5-card poker hand in [JSON format]: ["7H", "7C", "5S", "5C", "7H"]

    Enter second 5-card poker hand in [JSON format]: ["9C", "7C", "5C", "6C", "10C"]

    You have a Full House!


    You have a Flush!


    Winning hand is Full House: ['7H', '7C', '5S', '5C', '7H'].

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Let's see your best hand.


    Enter poker hand with more than 5 cards in [JSON format]: ["7H", "7C", "5S", "5C", "7H", "9C", "7C", "5C", "6C", "10C"]

    You have a Four of a Kind!
    Kicker: 10


Run Tests
---
    $ pip3 install -U pytest
    $ pytest
