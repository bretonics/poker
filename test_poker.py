# ["AC", "KC", "QC", "JC", "10C"]     # royal flush
# ["8C", "7C", "6C", "5C", "4C"]      # straight flush
# ["7S", "5S", "6S", "8S", "4S"]      # straight flush
# ["7H", "7C", "7S", "5C", "7H"]      # FoK
# ["KH", "KC", "KS", "5C", "KH"]      # FoK
# ["7H", "7C", "5S", "5C", "7H"]      # full house
# ["9C", "7C", "5C", "6C", "10C"]     # flush
# ["AH", "KH", "QD", "JC", "10C"]     # straight
# ["KH", "QD", "JC", "10C", "9C"]     # straight **
# ["7H", "5H", "6C", "8C", "4C"]      # straight
# ["7H", "7C", "5S", "JC", "7H"]      # ToK
# ["JH", "4C", "4S", "JC", "9H"]      # 2 pair
# ["JH", "4C", "5S", "JC", "9H"]      # 1 pair
# ["JH", "4C", "5S", "KC", "9H"]      # highest
# ["9H", "4C", "5S", "8C", "3S"]      # highest

import pytest
import json
from poker import *
from Card import Card
from Color import Color


class TestCard:
    print("Testing Card class...")

    # Test multiple cards
    @pytest.fixture(scope="module", params=["4H", "KD", "10S", "AC"])

    # Initialize card for all Card tests
    def card(self,request):
        return request.param

    # Face card value test
    def test_card(self, card):
        c = Card(card)
        assert c.card == card

    # Card instance has "card" attribute
    def test_card_attr(self, card):
        c = Card(card)
        assert hasattr(c, "card")

    # Card instance has "rank" attribute
    def test_rank_attr(self, card):
        c = Card(card)
        assert hasattr(c, "rank")

    # Card instance has "suit" attribute
    def test_suit_attr(self, card):
        c = Card(card)
        assert hasattr(c, "suit")

    # Card instance has "color" attribute
    def test_color_attr(self, card):
        c = Card(card)
        assert hasattr(c, "color")

    # Card instance rank matches card value passed
    def test_rank(self, card):
        c = Card(card)
        if len(card) == 2:
            assert c.rank == card[0]
        else:
            assert c.rank == card[0:2]

    # Card instance suit matches card value passed
    def test_suit(self, card):
        c = Card(card)
        assert c.suit == card[-1]

    # Card instance color matches card value passed
    def test_color(self, card):
        c = Card(card)
        if c.suit == "H" or c.suit == "D":
            assert c.color == "red"
        else:
            assert c.color == "black"


class TestColor:
    print("Testing Color class...")

    # Initialize color for all Color tests
    @pytest.fixture
    def getColor(self):
        return Color()

    # Color instance has "color" attribute
    def test_color(self, getColor):
        c = getColor
        assert hasattr(c, "color")

    # Color object is an instance of Color class
    def test_isinstance(self, getColor):
        assert isinstance(getColor, Color)


class TestOne():
    print("\tTESTING function #1...")

    def test_royal_flush(self):
        print("\tTESTING royal flush...")

        hand = json.loads( '["AC", "KC", "QC", "JC", "10C"]' )
        assert one(hand) == {'name': 'Royal Flush', 'hand': ['AC', 'KC', 'QC', 'JC', '10C'], 'value': None, 'kicker': None}

    def test_straight_flush(self):
        print("\tTESTING straight flush...")

        hand = json.loads( '["8C", "7C", "6C", "5C", "4C"]' )
        assert one(hand) == {'name': 'Straight Flush', 'hand': ['8C', '7C', '6C', '5C', '4C'], 'value': None, 'kicker': None}

        hand = json.loads( '["7S", "5S", "6S", "8S", "4S"]' )
        assert one(hand) == {"name": "Straight Flush", "hand": ['7S', '5S', '6S', '8S', '4S'], "value": None, "kicker": None}

    def test_four_of_kind(self):
        print("\tTESTING four of a kind...")

        hand = json.loads( '["7H", "7C", "7S", "5C", "7H"]' )
        assert one(hand) == {'name': 'Four of a Kind', 'hand': ['7H', '7C', '7S', '5C', '7H'], 'value': None, 'kicker': 5}

        hand = json.loads( '["KH", "KC", "KS", "AC", "KH"]' )
        assert one(hand) == {'name': 'Four of a Kind', 'hand': ['KH', 'KC', 'KS', 'AC', 'KH'], 'value': None, 'kicker': 'A'}

    def test_full_house(self):
        print("\tTESTING full house...")

        hand = json.loads( '["7H", "7C", "5S", "5C", "7H"]' )
        assert one(hand) == {'name': 'Full House', 'hand': ['7H', '7C', '5S', '5C', '7H'], 'value': None, 'kicker': None}

    def test_flush(self):
        print("\tTESTING flush...")

        hand = json.loads( '["9C", "7C", "5C", "6C", "10C"]' )
        assert one(hand) == {'name': 'Flush', 'hand': ['9C', '7C', '5C', '6C', '10C'], 'value': None, 'kicker': None}

    def test_straight(self):
        print("\tTESTING straights...")

        hand = json.loads( '["AH", "KH", "QD", "JC", "10C"]' )
        assert one(hand) == {'name': 'Straight', 'hand': ['AH', 'KH', 'QD', 'JC', '10C'], 'value': None, 'kicker': None}

        hand = json.loads( '["7H", "5H", "6C", "8C", "4C"]' )
        assert one(hand) == {'name': 'Straight', 'hand': ['7H', '5H', '6C', '8C', '4C'], 'value': None, 'kicker': None}

    @pytest.mark.xfail(reason="known failure of numeric and non-numeric straights")
    def test_mixed_straight(self):
        print("\tTESTING mixed numeric and non-numeric straight...")

        hand = json.loads( '["KH", "QD", "JC", "10C", "9C"]' )
        assert one(hand) == {'name': 'Straight', 'hand': ['KH', 'QD', 'JC', '10C', '9C'], 'value': None, 'kicker': None}

    def test_three_of_kind(self):
        print("\tTESTING three fo a kind...")

        hand = json.loads( '["7H", "7C", "5S", "JC", "7H"]' )
        assert one(hand) == {'name': 'Three of a Kind', 'hand': ['7H', '7C', '5S', 'JC', '7H'], 'value': None, 'kicker': 'J'}

    def test_two_pair(self):
        print("\tTESTING two pair...")

        hand = json.loads( '["JH", "4C", "4S", "JC", "9H"]' )
        assert one(hand) == {'name': 'Two Pair', 'hand': ['JH', '4C', '4S', 'JC', '9H'], 'value': None, 'kicker': 'J'}

    def test_one_pair(self):
        print("\tTESTING one pair...")

        hand = json.loads( '["JH", "4C", "5S", "JC", "9H"]' )
        assert one(hand) == {'name': 'One Pair', 'hand': ['JH', '4C', '5S', 'JC', '9H'], 'value': None, 'kicker': 9}

    def test_highest(self):
        print("\tTESTING highest card...")

        hand = json.loads( '["JH", "4C", "5S", "KC", "9H"]' )
        assert one(hand) == {'name': 'High Card', 'hand': ['JH', '4C', '5S', 'KC', '9H'], 'value': 'K', 'kicker': None}

        hand = json.loads( '["9H", "4C", "5S", "8C", "3S"]' )
        assert one(hand) == {'name': 'High Card', 'hand': ['9H', '4C', '5S', '8C', '3S'], 'value': 9, 'kicker': None}


class TestTwo():
    print("\tTESTING function #2...")


    def test_royalflsuh_vs_straight(self):
        print("\tTESTING royal flush vs straight...")

        hands = [ ["AC", "KC", "QC", "JC", "10C"], ["AH", "KH", "QD", "JC", "10C"] ]
        assert two(hands) == ["AC", "KC", "QC", "JC", "10C"]

    def test_royalflush_vs_straightflush(self):
        print("\tTESTING royal flush vs straight flush...")

        hands = [ ["AC", "KC", "QC", "JC", "10C"], ["8C", "7C", "6C", "5C", "4C"] ]
        assert two(hands) == ["AC", "KC", "QC", "JC", "10C"]

    def test_straigh_vs_straighflush(self):
        print("\tTESTING straight vs straight flush...")

        hands = [ ["7H", "5H", "6C", "8C", "4C"] , ["7S", "5S", "6S", "8S", "4S"]  ]
        assert two(hands) == ["7S", "5S", "6S", "8S", "4S"]

    def test_fullhouse_vs_fok(self):
        print("\tTESTING full house vs four of a kind...")

        hands = [ ["7H", "7C", "5S", "5C", "7H"], ["KH", "KC", "KS", "5C", "KH"] ]
        assert two(hands) == ["KH", "KC", "KS", "5C", "KH"]

    def test_fof_vs_twopair(self):
        print("\tTESTING four of a kind vs two pair...")

        hands = [ ["KH", "KC", "KS", "5C", "KH"], ["JH", "4C", "4S", "JC", "9H"] ]
        assert two(hands) == ["KH", "KC", "KS", "5C", "KH"]

    def test_tof_vs_twopair(self):
        print("\tTESTING three of a kind vs one pair...")

        hands = [ ["7H", "7C", "5S", "JC", "7H"], ["JH", "4C", "7S", "JC", "9H"] ]
        assert two(hands) == ["7H", "7C", "5S", "JC", "7H"]

    def test_twopair_vs_onepair(self):
        print("\tTESTING two pair vs one pair...")

        hands = [ ["JH", "4C", "5S", "JC", "9H"], ["JH", "4C", "4S", "JC", "9H"] ]
        assert two(hands) == ["JH", "4C", "4S", "JC", "9H"]

    def test_onepair_vs_highest(self):
        print("\tTESTING one pair vs highest card...")

        hands = [ ["JH", "4C", "5S", "JC", "9H"], ["JH", "4C", "5S", "KC", "9H"] ]
        assert two(hands) == ["JH", "4C", "5S", "JC", "9H"]

    def test_high_vs_high_numeric(self):
        print("\tTESTING high vs high numeric...")

        hands = [ ["10H", "4C", "5S", "KC", "9H"], ["9H", "4C", "5S", "8C", "3S"] ]
        assert two(hands) == ["10H", "4C", "5S", "KC", "9H"]

    def test_high_vs_high_non_numeric(self):
        print("\tTESTING high vs high non-numeric...")

        hands = [ ["JH", "4C", "5S", "KC", "9H"] ,  ["AH", "4C", "5S", "8C", "9S"] ]
        assert two(hands) == ["AH", "4C", "5S", "8C", "9S"]

    def test_high_vs_high_mixed(self):
        print("\tTESTING high vs high mix...")

        hands = [ ["10H", "4C", "5S", "KC", "9H"] ,  ["AH", "4C", "5S", "8C", "10S"] ]
        assert two(hands) == ["AH", "4C", "5S", "8C", "10S"]

    def test_three_hands(self):
        print("\tTESTING three hands: three of a kind, one pair, high card...")

        hands = [ ["7H", "7C", "5S", "JC", "7H"], ["JH", "4C", "7S", "JC", "9H"], ["10H", "4C", "5S", "KC", "9H"] ]
        assert two(hands) == ["7H", "7C", "5S", "JC", "7H"]

    def test_fullhouse_vs_fok_vs_flush(self):
        print("\tTESTING full house vs four of a kind vs flush...")

        hands = [ ["7H", "7C", "5S", "5C", "7H"], ["KH", "KC", "KS", "5C", "KH"], ["9C", "7C", "5C", "6C", "10C"]  ]
        assert two(hands) == ["KH", "KC", "KS", "5C", "KH"]

    def test_other_three_hands(self):
        print("\tTESTING high vs two pair vs straight flush...")

        hands = [ ["10H", "4C", "5S", "KC", "9H"] ,  ["JH", "4C", "4S", "JC", "9H"], ["7S", "5S", "6S", "8S", "4S"] ]
        assert two(hands) == ["7S", "5S", "6S", "8S", "4S"]


class TestThree():
    print("\tTESTING function #2...")

    def test_fok(self):
        hand = ["7H", "7C", "5S", "5C", "7H", "9C", "7C", "5C", "6C", "10C"]
        assert three(hand) == "Four of a Kind"

    def test_royal_flush(self):
        #royal flush
        hand = ["AC", "KC", "QC", "JC", "10C", "7H", "7C", "5S", "5C", "7H"]
        assert three(hand) == "Royal Flush"

    def test_full_house(self):
        hand = ["JH", "4C", "4S", "JC", "9H", "7H", "7C", "5S", "JC", "7H"]
        assert three(hand) == "Full House"
