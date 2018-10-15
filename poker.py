from Card import Card
from collections import defaultdict
import json


hands = []

def main():
    # hand = json.loads( "[\"JH\", \"4C\", \"4S\", \"JC\", \"9H\"]" )
    # Aks user for poker hand input -> convert JSON to list
    hand = json.loads( input("Enter poker hand in JSON format: ") )
    hands.append(hand)

    one()

def one():
    cards = []  # list of card objects
    ranks = defaultdict(int)  # dictionary of rank counts
    suits = defaultdict(int)  # dictionary of suit counts

    # Check each hand dealt
    for hand in hands:
        # Create list of Card objects
        for card in hand:
            c = Card(card)
            cards.append(c)
            ranks[c.rank] += 1
            suits[c.suit] += 1

        suitsVals = suits.values()
        print(ranks)
        print(suits)


        #--------------------------------------------------
        # Hands deailing with suits
        if isRoyal(ranks) and isFlush(suits):
            print("Winner! Winner! Chicken Dinner!")
            break

        if isStraight(ranks) and isFlush(suits):
            print("Straight Flush!")
            break

        if isFlush(suits):
            print("Flush!")
            break

        #--------------------------------------------------
        # Hands dealing with ranks
        if isStraight(ranks):
            print("Straight!")

        if hasPair(ranks):
            pairs = hasPair(ranks)
            if len(pairs) == 1:
                print("One pair!")
            if len(pairs) == 2:
                print("Two pair!")

#--------------------------------------------------------------------------------
# Helper functions

def hasPair(ranks):
    pairs = [k for k,v in ranks.items() if v == 2]
    return pairs

def isStraight(ranks):
    # TODO: check edge cases of numeric and non-numeric straights

    try:  # Check if rank is number
        r = [int(i) for i in ranks.keys()]
        print("Straight check")
        print(r)
        # Iterate through sorted list
        # +1 each step. Increment initial and compare to each subsequent rank
        r.sort()
        m = r[0]
        for n in r:
            if n == m:
                m += 1
            else:
                return False
        return True
    except:
        print("Checking non-numeric")
        # Rank is non-numeric card (J, Q, K, A)
        if isRoyal(ranks):
            return True
        else:
            # Check if straight has both numeric and non-numeric
            print("Straight has BOTH")
            if "10" in ranks:
                if "J" in ranks:  # going up
                    pass
                if "9" in ranks:  # goind down
                    pass
            return False

def isFlush(suits):
    # Check if all cards are same suit
    if 5 in suits.values():
        return True
    else:
        return False

def isRoyal(ranks):
    if "A" in ranks:
        if "K" in ranks:
            if "Q" in ranks:
                if "J" in ranks:
                    if "10" in ranks:
                        return True



main() # Call the main function
