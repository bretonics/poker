from Card import Card
from collections import defaultdict
import json

# Overall Poker hand rankings. Min is better hand.
rankings = { "Royal Flush": 1, "Straight Flush": 2, "Four of a Kind": 3, "Full House": 4,
             "Flush": 5, "Straight":6, "Three of a Kind": 7, "Two Pair": 8, "One Pair": 9, "High Card": 10}

# Holds Poker hands passed
hands = []
# Holds results of Poker hands
results = []

def main():
    # Pre-define a JSON poker hand
    hand = json.loads( "[\"JH\", \"4C\", \"4S\", \"JC\", \"9H\"]" )

    # Call implementation function #1
    print("\nUsing hand: {}".format(hand))
    print( "\n...You have a {}.\n".format( one(hand) ) )

    # Aks user for poker hand input -> convert JSON , add to list
    hand = json.loads( input("Enter poker hand in [JSON format]: ") )
    hands.append(hand)
    hand = json.loads( input("Enter poker hand in [JSON format]: ") )
    hands.append(hand)

    # Call implementation function #2
    two()

    # Call implementation function #3
    hand = json.loads( input("Enter poker hand in [JSON format]: ") )
    three(hand)

def one(hand):
    """First implementation where category of 5-card is determined"""
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
        return "Royal Flush"

    if isStraight(ranks) and isFlush(suits):
        return "Straight Flush"

    if isFlush(suits):
        return "Flush"

    #--------------------------------------------------
    # Hands dealing with ranks
    if isStraight(ranks):
        return "Straight"

    if isXOK(ranks, 4):
        return "Four of a Kind"

    if hasPair(ranks):
        pairs = hasPair(ranks)
        if len(pairs) == 1:
            if isXOK(ranks, 3):
                return "Full House"
            else:
                return "One Pair"
        if len(pairs) == 2:
            return "Two Pair"

    if isXOK(ranks, 3):
        return "Three of a Kind"

    return( highCard(ranks) )

def two():
    """Determine winner between 2 5-card hands"""
    # Track hands dealt
    results = {}
    # Check each hand dealt (passed)
    for hand in hands:
        result = one(hand)
        results[result] = hand

    rank = 11
    winner = ""
    winningHand = ""
    # Loop through results and check rankings for value
    for res, hand in results.items():
        # If current hand's ranking value is less than current rank
        # set as new winner
        if rankings[res] < rank:
            rank = rankings[res]  # set new rank to compare against for next iter
            winner = res
            winningHand = hand
    print("\nWinning hand is {}: {}.\n".format(winner, winningHand))
    return winningHand

def three(hand):
    pass
#--------------------------------------------------------------------------------
# Helper functions

def highCard(ranks):
    """Get highest card rank"""
    highest = ""
    if numeric(ranks):  # Check if ranks are numbers
        r = [eval(i) for i in ranks.keys()]
        highest = max(r)
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


    return "High Card"



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
