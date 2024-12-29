'''Test card.py '''

# Debugging for not able to import
# import sys
# import os

# print("sys.path:", sys.path)
# print("Current working directory:", os.getcwd())

import pytest
from src.card import Card, Suit


def test_card_creation():
    '''Test creating a card'''
    card = Card(Suit.SPADES, 10)
    assert card.suit == Suit.SPADES
    assert card.value == 10

def test_card_string_representation():
    '''Test string representation of a card'''
    card = Card(Suit.HEARTS, 5)
    assert str(card) == "5 of HEARTS"
    assert repr(card) == "5 of HEARTS"

def test_card_equality():
    '''Test card equality'''
    card1 = Card(Suit.CLUBS, 8)
    card2 = Card(Suit.DIAMONDS, 8)
    assert card1 == card2
    assert card1 != Card(Suit.HEARTS, 7)

def test_card_comparison():
    '''Test card comparison'''
    card1 = Card(Suit.CLUBS, 6)
    card2 = Card(Suit.SPADES, 9)
    assert card1 < card2
    assert card2 > card1
    assert card1 <= Card(Suit.DIAMONDS, 6)
    assert card2 >= Card(Suit.HEARTS, 9)

def test_card_addition():
    '''Test card addition'''
    card1 = Card(Suit.CLUBS, 4)
    card2 = Card(Suit.DIAMONDS, 5)
    assert card1 + card2 == 9
    assert card1 + 3 == 7

def test_card_subtraction():
    '''Test card subtraction'''
    card1 = Card(Suit.HEARTS, 7)
    card2 = Card(Suit.CLUBS, 2)
    assert card1 - card2 == 5
    assert card1 - 3 == 4

def test_invalid_addition():
    '''Test invalid addition'''
    card = Card(Suit.SPADES, 5)
    with pytest.raises(ValueError):
        result = card + "not_a_card"
