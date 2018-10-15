from Card import Card
from collections import defaultdict
import json

rankings = { "RoFl": 1, "StrFl": 2, "FoK": 3, "FHouse": 4, "Fl": 5, "Str":6, "ToK": 7, "TPair": 8, "OPair": 9, "HC": 10}
hands = []
results = []

def main():
    # hand = json.loads( "[\"JH\", \"4C\", \"4S\", \"JC\", \"9H\"]" )
    # Aks user for poker hand input -> convert JSON to list
    hand = json.loads( input("Enter poker hand in JSON format: ") )
    hands.append(hand)
    hand = json.loads( input("Enter poker hand in JSON format: ") )
    hands.append(hand)

    # Call implementation functions
    one(hand)
    two()

def one(hand):
    cards = []  # list of card objects
    ranks = defaultdict(int)  # dictionary of rank counts
    suits = defaultdict(int)  # dictionary of suit counts

    # Create list of Card objects
    for card in hand:
        c = Card(card)
        cards.append(c)
        # Keep track of counts for each rank/suit observed, increment in dictionary
        ranks[c.rank] += 1
        suits[c.suit] += 1

    #--------------------------------------------------
    # Hands deailing with suits
    if isRoyal(ranks) and isFlush(suits):
        print("Winner! Winner! Chicken Dinner!")
        return "RoFl"

    if isStraight(ranks) and isFlush(suits):
        print("Straight Flush!")
        return "StrFl"

    if isFlush(suits):
        print("Flush!")
        return "Fl"

    #--------------------------------------------------
    # Hands dealing with ranks
    if isStraight(ranks):
        print("Straight!")
        return "Str"

    if isXOK(ranks, 4):
        print("Four of a kind!")
        return "FoK"

    if hasPair(ranks):
        pairs = hasPair(ranks)
        if len(pairs) == 1:
            if isXOK(ranks, 3):
                print("Full house!")
                return "FHouse"
            else:
                print("One pair!")
                return "OPair"
        if len(pairs) == 2:
            print("Two pair!")
            return "TPair"

    if isXOK(ranks, 3):
        print("Three of a kind!")
        return "ToK"

    highCard(ranks)

def two():
    """Determine winner between 2 5-card hands"""
    # track hands dealt
    results = []
    # Check each hand dealt (passed)
    for hand in hands:
        result = one(hand)
        results.append(result)

    rank = 11
    winner = ""
    for h in results:
        if rankings[h] < rank:
            rank = rankings[h]
            winner = h
    print("Winning hand is {}".format(winner))
    return winner

#--------------------------------------------------------------------------------
# Helper functions

def highCard(ranks):
    """Get highest card rank"""
    highest = ""
    if numeric(ranks):  # Check if ranks are numbers
        r = [eval(i) for i in ranks.keys()]
        highest = max(r)
        print("High card! Rank {}".format(highest))
        return "HC"
    else:
        # Get highes non-numeric card rank
        if "A" in ranks:
            highest = "A"
        if "K" in ranks:
            highest = "K"
        if "Q" in ranks:
            highest = "Q"
        if "J" in ranks:
            highest = "J"

        print("Highest card! Rank {}".format(highest))
        return "HC"


def hasPair(ranks):
    """Check if pairs of cards present"""
    # Get list of ranks that have value of 2 (a pair)
    pairs = [k for k,v in ranks.items() if v == 2]
    # returns pairs list, lenght will determine number of pairs
    return pairs

def isXOK(ranks, n):
    """Check for n number of cards in hand"""
    if n in ranks.values():
        return True
    else:
        return False

def isStraight(ranks):
    """Check if sequence of ranks is a straight"""

    if numeric(ranks):  # Check if ranks are numbers
        r = [eval(i) for i in ranks.keys()]

        # Iterate through sorted list +1 each step.
        # Increment initial and compare current count to each subsequent rank
        # as this should be a sequence
        r.sort()
        m = r[0]
        for n in r:
            if n == m:
                m += 1
            else:
                return False
        return True
    else:  # Rank is non-numeric cards (J, Q, K, A) or contains mix numeric/non-numeric
    # TODO: check edge cases of numeric and non-numeric straights
        if isRoyal(ranks):  # Straight is royal
            return True
        else:  # Check if straight has both numeric and non-numeric

            if "10" in ranks:
                if "J" in ranks:  # going up
                    pass
                if "9" in ranks:  # goind down
                    pass
            return False

def isFlush(suits):
    """Check if all cards are same suit"""
    if 5 in suits.values():
        return True
    else:
        return False

def isRoyal(ranks):
    """Check if royal suit of cards"""
    if "A" in ranks:
        if "K" in ranks:
            if "Q" in ranks:
                if "J" in ranks:
                    if "10" in ranks:
                        return True

def numeric(ranks):
    """Check if ranks are numbers"""
    try:
        r = [eval(i) for i in ranks.keys()]
        return True
    except:
        return False


main() # Call the main function
