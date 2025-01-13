import pytest
from unittest.mock import patch
from src.player.rl_player import RLPlayer
from src.game.game import Game
from src.card import Card, Suit


def test_get_player_name():
    """Test get_player_name generates a valid name."""
    player = RLPlayer()
    assert isinstance(player.name, str)
    assert len(player.name) > 0


def test_turn_initial_cards():
    """Test turn_initial_cards generates valid initial card turns."""
    initial_table_cards = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]

    player = RLPlayer()

    with patch("src.player.computer_player.randint", side_effect=[2, 1, 3]):
        result = player.turn_initial_cards(initial_table_cards)
        assert len(result) == len(initial_table_cards)
        for r, c in result:
            assert 1 <= r <= len(initial_table_cards)
            assert 1 <= c <= len(initial_table_cards[0])
