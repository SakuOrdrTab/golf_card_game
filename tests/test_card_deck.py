'''Tests for the CardDeck class.'''

import pytest

from src.card_deck import CardDeck, Card, Suit


def test_deck_initialization():
    deck = CardDeck()
    assert len(deck.drawing_deck) == 52
    assert len(deck.played_cards) == 0


def test_draw_from_deck():
    deck = CardDeck()
    card = deck.draw_from_deck()
    assert isinstance(card, Card)
    assert len(deck.drawing_deck) == 51


def test_deal_first_card():
    deck = CardDeck()
    deck.deal_first_card()
    assert len(deck.drawing_deck) == 51
    assert len(deck.played_cards) == 1


def test_draw_from_played():
    deck = CardDeck()
    deck.deal_first_card()  # Adds one card to played_cards
    last_card = deck.draw_from_played()
    assert isinstance(last_card, Card)
    assert len(deck.played_cards) == 0


def test_add_to_played():
    deck = CardDeck()
    card = deck.draw_from_deck()
    deck.add_to_played(card)
    assert len(deck.played_cards) == 1
    assert deck.played_cards[-1] == card


def test_get_last_played_card():
    deck = CardDeck()
    deck.deal_first_card()
    last_card = deck.get_last_played_card()
    assert last_card == deck.played_cards[-1]


def test_reset_deck_when_empty():
    deck = CardDeck()
    # Draw all cards from the deck
    while len(deck.drawing_deck) > 0:
        deck.draw_from_deck()

    assert len(deck.drawing_deck) == 0

    # Add cards to the played pile
    deck.add_to_played(Card(Suit.HEARTS, 5))
    deck.add_to_played(Card(Suit.SPADES, 10))

    # Drawing now resets the deck
    card = deck.draw_from_deck()
    assert isinstance(card, Card)
    assert len(deck.drawing_deck) == 1

