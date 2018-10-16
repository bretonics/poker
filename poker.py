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

    # Call implementation function #1 using pre-defined hand
    print("\nUsing hand: {}".format(hand))
    one(hand)

    # Call implementation function #1 using hand entered from user
    hand = json.loads( input("\nEnter you poker hand in [JSON format]: ") )
    one(hand)

    # # Call implementation function #2
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    # print("Let's play another round.\n")
    # print("Who will the winner be? Enter your hands...\n")
    # # Aks user for poker hand input -> convert JSON , add to list
    # hand = json.loads( input("\nEnter poker hand in [JSON format]: ") )
    # hands.append(hand)
    # hand = json.loads( input("\nEnter poker hand in [JSON format]: ") )
    # hands.append(hand)
    # two()
    #
    # # Call implementation function #3
    # hand = json.loads( input("Enter poker hand in [JSON format]: ") )
    # three(hand)

#--------------------------------------------------------------------------------
# implementation Functions
def one(hand):
    """First implementation where category of 5-card is determined"""
    cards = []  # list of card objects
    ranks = defaultdict(int)  # dictionary of rank counts
    suits = defaultdict(int)  # dictionary of suit counts
    result = {}

    # Create list of Card objects
    for card in hand:
        c = Card(card)
        cards.append(c)
        # Keep track of counts for each rank/suit observed, increment in dictionary
        ranks[c.rank] += 1
        suits[c.suit] += 1

    #--------------------------------------------------
    # Hands deailing with suits

    # Royal Flush
    if isRoyal(ranks) and isFlush(suits):
        print("\nWinner! Winner! Chicken Dinner!")
        result = {"name": "Royal Flush", "hand": hand, "kicker": None}
        message(result)
        return result

    # Straight flush
    if isStraight(ranks) and isFlush(suits):
        result =  {"name": "Straight Flush", "hand": hand, "kicker": None}
        message(result)
        return result

    # Flush
    if isFlush(suits):
        result = {"name": "Flush", "hand": hand, "kicker": None}
        message(result)
        return result

    #--------------------------------------------------
    # Hands dealing with ranks

    # Straight
    if isStraight(ranks):
        result = {"name": "Straight", "hand": hand, "kicker": None}
        message(result)
        return result

    # Four of a kind
    if isXOK(ranks, 4):
        result = {"name": "Four of a Kind", "hand": hand, "kicker": None}
        message(result)
        return result

    # Pairs
    if hasPair(ranks):
        pairs = hasPair(ranks)
        if len(pairs) == 1:

            # Full house
            if isXOK(ranks, 3):
                result = {"name": "Full House", "hand": hand, "kicker": None}
                message(result)
                return result

            # One pair
            else:
                # Get other cards not in pair to get kicker
                remaining = [x for x in ranks.keys() if not x.startswith(pairs[0])]
                result = {"name": "One Pair", "hand": hand, "kicker": None, "kicker": kicker(remaining)}
                message(result)
                return result

        # Two pair
        if len(pairs) == 2:
            # Get other cards not in pair to get kicker
            remaining = [x for x in ranks.keys() if not x.startswith(pairs[0]) and not x.startswith(pairs[1])]
            result = {"name": "Two Pair", "hand": hand, "kicker": None, "kicker": remaining}
            message(result)
            return result

    # Three of a kind
    if isXOK(ranks, 3):
        n = isXOK(ranks, 3)
        # Get other cards not in pair to get kicker
        remaining = [x for x in ranks.keys() if not x.startswith(n[0])]
        print(remaining)

        result = {"name": "Three of a Kind", "hand": hand, "kicker": kicker(remaining)}
        message(result)
        return result

    # High Card
    if not bool(result):
        result = highCard(ranks)
        result["hand"] = hand
        message(result)
        return result


def two():
    """Determine winner between 2 5-card hands"""
    # Track hands dealt
    results = {}
    # Check each hand dealt (passed)
    for hand in hands:
        # Returned result is dictionary of name:hand (key:value) pair
        result = one(hand)
        results[result["name"]] = hand

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
    """Return best 5-card hand"""
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

    return {"name": "High Card", "value": highest}

def kicker(remaining):
    """Get kicker card rank"""
    highest = ""
    try:  # Check if ranks are numbers
        r = [eval(i) for i in remaining]
        highest = max(r)
    except:
        # Get highes non-numeric card rank
        if "A" in remaining:
            highest = "A"
        if "K" in remaining:
            highest = "K"
        if "Q" in remaining:
            highest = "Q"
        if "J" in remaining:
            highest = "J"

    return highest

def hasPair(ranks):
    """Check if pairs of cards present"""
    # Get list of ranks that have value of 2 (a pair)
    pairs = [k for k,v in ranks.items() if v == 2]
    # returns pairs list, lenght will determine number of pairs
    return pairs

def isXOK(ranks, n):
    """Check for n number of cards in hand"""
    if n in ranks.values():
        # Return card rank that is present "n" times
        return [k for k,v in ranks.items() if v == n]
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

def message(result):
    name = result["name"]
    hand = result["hand"]
    kicker = result["kicker"]

    # Print hand
    print("\nYou have a {}!\n".format(name), end="")

    # Append kicker if present
    if kicker is not None:
        print("Kicker: {}".format(kicker) )
    else:
        print("")  # append new line return carriage

main() # Call the main function
