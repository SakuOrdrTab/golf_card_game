import pytest
from unittest.mock import patch
from src.player.stupid_computer_player import StupidComputerPlayer
from src.card import Card, Suit


def test_get_player_name():
    """Test get_player_name generates a valid name."""
    player = StupidComputerPlayer()
    assert isinstance(player.name, str)
    assert len(player.name) > 0


def test_get_draw_action():
    """Test get_draw_action returns a valid choice ('d' or 'p')."""
    game_status = {
        "other_players": [],
        "player": [],
        "played_top_card": Card(Suit.SPADES, 4),
    }

    with patch("src.player.computer_player.choice", return_value="d"):
        player = StupidComputerPlayer()
        draw_action = player.get_draw_action(game_status)
        assert draw_action in ["p", "d"]


def test_get_play_action():
    """Test get_play_action returns a valid play action."""
    game_status = {
        "other_players": [],
        "player": [],
        "played_top_card": None,
        "hand_card": type("Card", (object,), {"value": 5})(),  # Mock hand card with value 5
    }

    # Mock computer's table cards
    table_cards = [
        [Card(Suit.CLUBS, x) for x in [2,5,4]],
        [Card(Suit.DIAMONDS, x) for x in [1,3,4]],
        [Card(Suit.HEARTS, x) for x in [1,5,2]],
    ]
    player = StupidComputerPlayer()
    player.table_cards = table_cards

    # Mock parse_value behavior for testing
    with patch("src.player.computer_player.randint", return_value=4):
        play_action = player.get_play_action(game_status)
        if play_action == ("p", None):
            assert play_action == ("p", None)
        else:
            row, col = play_action
            assert 1 <= row <= 3
            assert 1 <= col <= 3


def test_turn_initial_cards():
    """Test turn_initial_cards generates valid initial card turns."""
    initial_table_cards = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]

    player = StupidComputerPlayer()

    with patch("src.player.computer_player.randint", side_effect=[2, 1, 3]):
        result = player.turn_initial_cards(initial_table_cards)
        assert len(result) == len(initial_table_cards)
        for r, c in result:
            assert 1 <= r <= len(initial_table_cards)
            assert 1 <= c <= len(initial_table_cards[0])
