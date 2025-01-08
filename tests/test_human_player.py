import pytest
from unittest.mock import patch
from src.player.human_player import HumanPlayer

def test_get_player_name():
    """Test get_player_name correctly sets the player's name."""
    with patch("builtins.input", return_value="Alice"):
        player = HumanPlayer()
        assert player.name == "Alice"


def test_get_draw_action_valid_inputs():
    """Test get_draw_action accepts valid inputs 'd' and 'p'."""
    game_status = {
        "other_players": [],
        "player": [],
        "played_top_card": None,
    }

    # Test 'd' input
    with patch("builtins.input", side_effect=["TestPlayer","1", "1", "1", "d"]):
        player = HumanPlayer()
        assert player.get_draw_action(game_status) == "d"

    # Test 'p' input
    with patch("builtins.input", side_effect=["TestPlayer","1", "1", "1", "p"]):
        player = HumanPlayer()
        assert player.get_draw_action(game_status) == "p"


def test_get_draw_action_invalid_then_valid():
    """Test get_draw_action rejects invalid inputs and accepts valid input."""
    game_status = {
        "other_players": [],
        "player": [],
        "played_top_card": None,
    }

    with patch("builtins.input", side_effect=["x", "invalid", "d"]), patch("builtins.print") as mock_print:
        player = HumanPlayer()
        assert player.get_draw_action(game_status) == "d"
        mock_print.assert_any_call("Invalid command, please input 'd' or 'p'")


def test_get_play_action_valid_inputs():
    """Test get_play_action accepts valid inputs ('p' or coordinates)."""
    game_status = {
        "other_players": [],
        "player": [1,2,3], # has to have len 3, like in table_cards
        "played_top_card": None,
        "hand_card": None,
    }

    # Test 'p' input
    with patch("builtins.input", side_effect=["test", "1", "1", "1", "d", "p"]):
        player = HumanPlayer()
        assert player.get_play_action(game_status) == ("p", None)

    # Test valid coordinates
    with patch("builtins.input", side_effect=["test", "1", "1", "1", "d", "1,2"]):
        player = HumanPlayer()
        assert player.get_play_action(game_status) == (1, 2)


def test_get_play_action_invalid_then_valid():
    """Test get_play_action rejects invalid inputs before accepting a valid one."""
    game_status = {
        "other_players": [],
        "player": [1,2,3], # has to have len 3, like in table_cards
        "played_top_card": None,
        "hand_card": None,
    }

    with patch("builtins.input", side_effect=["test", "1", "1", "1", "d", "3,x", "1,1"]), patch("builtins.print") as mock_print:
        player = HumanPlayer()
        assert player.get_play_action(game_status) == (1, 1)
        mock_print.assert_any_call("Invalid input")


def test_turn_initial_cards():
    """Test turn_initial_cards processes valid input correctly."""
    initial_table_cards = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
    inputs = ["TestPlayer", "2", "1", "3"]  # Provide name and valid inputs for all rows
    with patch("builtins.input", side_effect=inputs), patch("builtins.print") as mock_print:
        player = HumanPlayer()
        result = player.turn_initial_cards(initial_table_cards)
        assert result == [(1, 2), (2, 1), (3, 3)]
        # Verify the correct prompts were printed
        mock_print.assert_any_call("Which card do you want to turn for row ['A', 'B', 'C']")
        mock_print.assert_any_call("Which card do you want to turn for row ['D', 'E', 'F']")
        mock_print.assert_any_call("Which card do you want to turn for row ['G', 'H', 'I']")


