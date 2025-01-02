import pytest
from unittest.mock import patch
from src.player import HumanPlayer

def test_get_player_name():
    """Test the get_player_name method."""
    with patch("builtins.input", return_value="John Doe"):
        player = HumanPlayer()
        assert player.name == "John Doe"

def test_get_draw_action_deck():
    """Test get_draw_action with 'd' input for deck."""
    game_status = {
        "other_players": [],
        "player": [],
        "played_top_card": None,
    }
    with patch("builtins.input", side_effect=["d"]):
        player = HumanPlayer()
        action = player.get_draw_action(game_status)
        assert action == "d"

def test_get_draw_action_played():
    """Test get_draw_action with 'p' input for played cards."""
    game_status = {
        "other_players": [],
        "player": [],
        "played_top_card": None,
    }
    with patch("builtins.input", side_effect=["p"]):
        player = HumanPlayer()
        action = player.get_draw_action(game_status)
        assert action == "p"

def test_get_draw_action_invalid_then_valid():
    """Test get_draw_action with invalid input followed by valid input."""
    game_status = {
        "other_players": [],
        "player": [],
        "played_top_card": None,
    }
    with patch("builtins.input", side_effect=["x", "d"]), patch("builtins.print") as mock_print:
        player = HumanPlayer()
        action = player.get_draw_action(game_status)
        assert action == "d"
        mock_print.assert_any_call("Invalid command, please input 'd' or 'p'")

def test_get_play_action_played_deck():
    """Test get_play_action with 'p' input."""
    game_status = {
        "other_players": [],
        "player": [],
        "played_top_card": None,
        "hand_card": None,
    }
    with patch("builtins.input", side_effect=["p"]):
        player = HumanPlayer()
        action = player.get_play_action(game_status)
        assert action == ("p", None)

def test_get_play_action_table_coordinates():
    """Test get_play_action with table coordinates input."""
    game_status = {
        "other_players": [],
        "player": [],
        "played_top_card": None,
        "hand_card": None,
    }
    with patch("builtins.input", side_effect=["1,2"]):
        player = HumanPlayer()
        action = player.get_play_action(game_status)
        assert action == (1, 2)

def test_turn_initial_cards():
    """Test turn_initial_cards method."""
    initial_table_cards = [["A", "B", "C"], ["D", "E", "F"]]
    inputs = ["2", "1"]  # Choose card 2 for the first row and card 1 for the second row
    with patch("builtins.input", side_effect=inputs), patch("builtins.print") as mock_print:
        player = HumanPlayer()
        result = player.turn_initial_cards(initial_table_cards)
        assert result == [(1, 2), (2, 1)]
        mock_print.assert_any_call("Which card do you want to turn for row ['A', 'B', 'C']")
        mock_print.assert_any_call("Which card do you want to turn for row ['D', 'E', 'F']")
