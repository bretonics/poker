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
    """Main function asking user for input and calling 3 different functions"""

    # Pre-define a JSON poker hand
    hand = json.loads( "[\"JH\", \"4C\", \"4S\", \"JC\", \"9H\"]" )

    # Call implementation function #1 using pre-defined hand
    print("\nUsing hand: {}".format(hand))
    one(hand)

    # Call implementation function #1 using hand entered from user
    # Make sure hand entered has 5 cards
    hand = []  # reset hand
    while len(hand) != 5:
        try:
            hand = json.loads( input("\nEnter your 5-card poker hand in [JSON format]: ") )
        except ValueError as e:
            print("\n[X] Not a JSON input! Try again.")

    # Use function #1
    one(hand)


    # Call implementation function #2
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    print("Let's play another round.\n")
    print("Who will the winner be? Enter your hands...\n")

    # Ask user for 2 poker hands
    for x in ["first", "second"]:
        hand = []  # reset hand
        # Make sure hand entered has 5 cards
        while len(hand) != 5:
            # Aks user for poker hand input -> convert JSON , add to list
            try:
                hand = json.loads( input("\nEnter {} 5-card poker hand in [JSON format]: ".format(x)) )
            except ValueError as e:
                print("\n[X] Not a JSON input! Try again.")
        hands.append(hand)

    # Use function #2
    two(hands)


    # Call implementation function #3
    # Make sure hand entered has more than 5 cards
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    print("Let's see your best hand.\n")
    hand = []  # reset hand
    while len(hand) <= 5:
        try:
            # Aks user for poker hand input -> convert JSON , add to list
            hand = json.loads( input("\nEnter poker hand with more than 5 cards in [JSON format]: ") )
        except ValueError as e:
            print("\n[X] Not a JSON input! Try again.")

    # Use function #3
    three(hand)

#--------------------------------------------------------------------------------
# Implementation Functions

def one(hand):
    """First implementation where category of 5-card is determined"""
    # Dictionary object for resulting hand
    result = {}

    # Get hand ranks and suits information from cards
    cards, ranks, suits = handInfo(hand)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Hands dealing with suits
    royal = isRoyal(hand)
    fok = isXOK(hand, 4)
    flush = isFlush(hand)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Hands dealing with ranks
    straight = isStraight(hand)
    tok = isXOK(hand, 3)
    pair = hasPair(hand)

    #--------------------------------------------------------------------------------
    # Check what kind of hand was passed

    # Royal Flush
    if royal and flush:
        print("\nWinner! Winner! Chicken Dinner!")
        # Construct royal flush result
        result = {**royal, **flush}
        result["name"] = "Royal Flush"
        result["hand"] = hand
        # Print message and return dictionary object of hand
        message(result)
        return result

    # Straight flush
    if straight and flush:
        # Construct straight flush result
        result = {**straight, **flush}
        result["name"] = "Straight Flush"
        result["hand"] = hand
        # Print message and return dictionary object of hand
        message(result)
        return result

    # Flush
    if flush:
        # Construct flush result
        result = flush
        result["name"] = "Flush"
        result["hand"] = hand
        # Print message and return dictionary object of hand
        message(result)
        return result

    # Straight
    if straight:
        # Construct straight result
        result = straight
        result["name"] = "Straight"
        result["hand"] = hand
        # Print message and return dictionary object of hand
        message(result)
        return result

    # Four of a kind
    if fok:
        # Construct four of a kind result
        result = fok[0]
        result["name"] = "Four of a Kind"
        result["hand"] = hand
        # Get other cards not in pair to get kicker
        remaining = remainingCards(ranks, fok[1][0])
        result["kicker"] = kicker(remaining)
        # Print message and return dictionary object of hand
        message(result)
        return result

    # Pairs
    if pair:
        pairs = pair[1]  # list of ranks that are pairs

        if len(pairs) == 1:

            # Full house (three of a kind + one pair)
            if tok:
                # Construct full house result
                result = {**tok[0], **pair[0]}
                result["name"] = "Full House"
                result["hand"] = hand
                # Print message and return dictionary object of hand
                message(result)
                return result

            # One pair
            else:
                # Construct one pair result
                result = pair[0]
                result["name"] = "One Pair"
                result["hand"] = hand
                # Get other cards not in pair to get kicker
                remaining = remainingCards(ranks, pairs[0])
                result["kicker"] = kicker(remaining)
                # Print message and return dictionary object of hand
                message(result)
                return result

        # Two pair
        if len(pairs) == 2:
            # Construct two pair result
            result = pair[0]
            result["name"] = "Two Pair"
            result["hand"] = hand

            # Get other cards not in pair to get kicker
            remaining = remainingCards(ranks, pairs[1])
            result["kicker"] = kicker(remaining)

            # Print message and return dictionary object of hand
            message(result)
            return result

    # Three of a kind
    if tok:
        # Construct three of a kind result
        result = tok[0]
        result["name"] = "Three of a Kind"
        result["hand"] = hand
        # Get other cards not in pair to get kicker
        remaining = remainingCards(ranks, tok[1][0])
        result["kicker"] = kicker(remaining)
        # Print message and return dictionary object of hand
        message(result)
        return result

    # High Card
    if not bool(result):
        # Construct high card result
        result = highCard(hand)
        result["hand"] = hand

        # Print message and return dictionary object of hand
        message(result)
        return result


def two(hands):
    """Determine winner between 2 5-card hands"""
    # Track hands dealt
    results = {}
    # Check each hand dealt (passed)
    for hand in hands:
        # Returned result is dictionary of name:hand (key:value) pair
        result = one(hand)
        # Handle hands that are both same type, e.g) a set of two "high card" hands
        if result["name"] in results.keys():
            hand = compareIdentHands(hands)
        results[result["name"]] = hand

    rank = 11
    winner = ""
    winningHand = ""
    # Loop through results and check rankings for value
    for name, hand in results.items():
        # If current hand's ranking value is less than current rank
        # set as new winner
        if rankings[name] < rank:
            rank = rankings[name]  # set new rank to compare against for next iter
            winner = name
            winningHand = hand

    print("\nWinning hand is {}: {}.\n".format(winner, winningHand))
    return winningHand


def three(hand):
    """Return best 5-card hand"""
    # Get hand ranks and suits information from cards
    cards, ranks, suits = handInfo(hand)

    # Keep track of all possible hands from cards passed
    hands = {}

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Hands deailing with suits
    royal = isRoyal(hand)
    fok = isXOK(hand, 4)
    flush = isFlush(hand)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Hands dealing with ranks
    straight = isStraight(hand)
    tok = isXOK(hand, 3)
    pair = hasPair(hand)

    #--------------------------------------------------------------------------------
    # Test each possible hand and save results to compare from all possibilities

    # Royal Flush
    if royal and flush:
        # Construct royal flush result
        result = {**royal, **flush}
        result["name"] = "Royal Flush"
        result["hand"] = hand
        # Add result to dictionary as a possible hand
        hands[result["name"]] = result

    # Straight flush
    if straight and flush:
        # Construct straight flush result
        result = {**straight, **flush}
        result["name"] = "Straight Flush"
        result["hand"] = hand
        # Add result to dictionary as a possible hand
        hands[result["name"]] = result

    # Four of a kind
    if fok:
        result = fok[0]
        result["name"] = "Four of a Kind"
        # Get other cards not in pair to get kicker
        remaining = remainingCards(ranks, fok[1][0])
        result["hand"] = hand
        result["kicker"] = kicker(remaining)
        # Add result to dictionary as a possible hand
        hands[result["name"]] = result

    # Pairs
    if pair:
        pairs = pair[1]  # list of ranks that are pairs

        if len(pairs) == 1:

            # Full house (three of a kind + one pair)
            if tok:
                # Construct full house result
                result = {**tok[0], **pair[0]}
                result["name"] = "Full House"
                result["hand"] = hand
                # Add result to dictionary as a possible hand
                hands[result["name"]] = result

            # One pair
            else:
                # Construct one pair result
                result = pair[0]
                result["name"] = "One Pair"
                result["hand"] = hand
                # Get other cards not in pair to get kicker
                remaining = remainingCards(ranks, pairs[0])
                result["kicker"] = kicker(remaining)
                # Add result to dictionary as a possible hand
                hands[result["name"]] = result

        # Two pair
        if len(pairs) == 2:
            # Construct two pair result
            result = pair[0]
            result["name"] = "Two Pair"
            result["hand"] = hand
            # Get other cards not in pair to get kicker
            remaining = remainingCards(ranks, pairs[1])
            result["kicker"] = kicker(remaining)
            # Add result to dictionary as a possible hand
            hands[result["name"]] = result

    # Flush
    if flush:
        # Construct flush result
        result = flush
        result["name"] = "Flush"
        result["hand"] = hand
        # Add result to dictionary as a possible hand
        hands[result["name"]] = result

    # Straight
    if straight:
        # Construct dictionary result
        result = straight
        result["name"] = "Straight"
        result["hand"] = hand
        # Add result to dictionary as a possible hand
        hands[result["name"]] = result

    # Three of a kind
    if tok:
        # Construct dictionary result
        result = tok[0]
        result["name"] = "Three of a Kind"
        result["hand"] = hand
        # Get other cards not in pair to get kicker
        remaining = remainingCards(ranks, tok[1][0])
        result["kicker"] = kicker(remaining)
        # Add result to dictionary as a possible hand
        hands[result["name"]] = result

    # High Card
    result = highCard(hand)
    result["hand"] = hand
    # Add result to dictionary as a possible hand
    hands[result["name"]] = result

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Return highest hand

    # Iterate through results of all possible hands in set of cards
    best = 11
    winner = ""
    value = ""
    for item, val in hands.items():
        score = rankings[item]
        # Store best set of cards according to ranking
        if score < best:
            best = score
            winner = item
            value = val

    print("Best possible hand ia a {}: {}".format(winner, value))
    return(winner)

#--------------------------------------------------------------------------------
# Helper functions

def highCard(hand):
    """Get highest card rank"""

    # Get hand ranks and suits information from cards
    cards, ranks, suits = handInfo(hand)

    highest = ""
    if numeric(ranks):  # Check if ranks are numbers
        r = [eval(i) for i in ranks.keys()]
        highest = max(r)
    else:
        # Get highest non-numeric card rank, order counts
        if "J" in ranks:
            highest = "J"
        if "Q" in ranks:
            highest = "Q"
        if "K" in ranks:
            highest = "K"
        if "A" in ranks:
            highest = "A"

    return {"name": "High Card", "value": highest, "kicker": None}

def hasPair(hand):
    """Check if pairs of cards present"""

    # Get hand ranks and suits information from cards
    cards, ranks, suits = handInfo(hand)

    # Get list of ranks that have value of 2 (a pair)
    pairs = [k for k,v in ranks.items() if v == 2]
    # returns pairs list, lenght will determine number of pairs

    return {"value": None, "kicker": None}, pairs

def isXOK(hand, n):
    """Check for n number of cards in hand"""

    # Get hand ranks and suits information from cards
    cards, ranks, suits = handInfo(hand)

    if n in ranks.values():
        # Return card rank that is present "n" times
        kind = [k for k,v in ranks.items() if v == n]
        return {"value": None}, kind
    else:
        return False

def isStraight(hand):
    """Check if sequence of ranks is a straight"""

    # Get hand ranks and suits information from cards
    cards, ranks, suits = handInfo(hand)

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
        return {"value": None, "kicker": None}
    else:  # Rank is non-numeric cards (J, Q, K, A) or contains mix numeric/non-numeric
    #### TODO: check edge cases of numeric and non-numeric straights
        if isRoyal(ranks):  # Straight contains non-numeric card(s)
            return True
        else:  # Check if straight has both numeric and non-numeric
            if "10" in ranks:
                if "J" in ranks:  # going up
                    pass
                if "9" in ranks:  # goind down
                    pass
            return False

def isFlush(hand):
    """Check if all cards are same suit"""

    # Get hand ranks and suits information from cards
    cards, ranks, suits = handInfo(hand)

    # Check if there are suit counts >= to 5
    if [x for x in suits.values() if x >= 5]:
        return {"name": "Flush", "value": None, "kicker": None}
    else:
        return False

def isRoyal(hand):
    """Check if royal suit of cards"""

    # Get hand ranks and suits information from cards
    cards, ranks, suits = handInfo(hand)

    if "A" in ranks:
        if "K" in ranks:
            if "Q" in ranks:
                if "J" in ranks:
                    if "10" in ranks:
                        return {"name": "Royal", "value": None, "kicker": None}


def kicker(remaining):
    """Get kicker card rank"""

    highest = ""
    try:  # Check if ranks are numbers
        r = [eval(i) for i in remaining]
        highest = max(r)
    except:
        # Get highest non-numeric card rank, order counts
        if "J" in remaining:
            highest = "J"
        if "Q" in remaining:
            highest = "Q"
        if "K" in remaining:
            highest = "K"
        if "A" in remaining:
            highest = "A"

    return highest

def handInfo(hand):
    """Takes hand passed and returns ranks and suits dictionaries as information data structures"""
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

    # Return a list of cards in hand, their ranks, and their suits
    return cards, ranks, suits

def compareIdentHands(hands):
    """Compare identically ranked hands and return one with highest card"""
    highest = 0
    hand = []

    # Loop every hand and card to determine which hands contains the highest rank value
    for h in hands:
        for card in h:
            rank = Card(card).rank
            # Rank value of this hand is higher than previous hand
            # set as winning hand to return
            try:
                r = eval(rank)
                if r > highest:
                    highest = r
                    hand = h
            except:
                # Get highest non-numeric card from hands
                if highest == 0:
                    highest = rank

                if rank == "J" and highest not in ["Q", "K", "A"]:
                    hand = h
                if rank == "Q" and highest not in ["K", "A"]:
                    hand = h
                if rank == "K" and highest != "A":
                    hand = h
                if rank == "A":
                    hand = h

    return hand

def numeric(ranks):
    """Check if ranks are numbers"""
    try:
        r = [eval(i) for i in ranks.keys()]
        return True
    except:
        return False

def remainingCards(ranks, n):
    return [x for x in ranks.keys() if not x.startswith(n)]

def message(result):
    """Prints user a message with poker hand"""
    name = result["name"]
    hand = result["hand"]
    kicker = result["kicker"]
    value = result["value"]

    # Print hand
    print("\nYou have a {}!\n".format(name), end="")

    # Append kicker if present
    if kicker is not None:
        print("Kicker: {}\n".format(kicker) )
    elif value is not None:
        print("Value: {}\n".format(value) )
    else:
        print("")  # append return carriage

if __name__ == "__main__":
    main() # Call the main function
