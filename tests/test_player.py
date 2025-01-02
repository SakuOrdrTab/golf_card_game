import pytest
from src.player import Player

# Dummy concrete implementation of Player to test the abstract class
class DummyPlayer(Player):
    def get_player_name(self) -> str:
        return "TestPlayer"

    def get_draw_action(self, game_status: dict) -> str:
        return "draw_pile"

    def get_play_action(self, game_status: dict) -> tuple:
        return ("card_to_play", "target_location")

    def turn_initial_cards(self, initial_table_cards: list) -> list:
        return initial_table_cards

def test_player_initialization():
    """Test that a concrete subclass of Player initializes correctly."""
    player = DummyPlayer()
    assert player.name == "TestPlayer"
    assert player.table_cards == []

def test_get_player_name():
    """Test the get_player_name method."""
    player = DummyPlayer()
    assert player.get_player_name() == "TestPlayer"

def test_get_draw_action():
    """Test the get_draw_action method."""
    player = DummyPlayer()
    game_status = {
        "other_players": [],
        "player": [],
        "played_top_card": None,
    }
    assert player.get_draw_action(game_status) == "draw_pile"

def test_get_play_action():
    """Test the get_play_action method."""
    player = DummyPlayer()
    game_status = {
        "other_players": [],
        "player": [],
        "played_top_card": None,
        "hand_card": None,
    }
    assert player.get_play_action(game_status) == ("card_to_play", "target_location")

def test_turn_initial_cards():
    """Test the turn_initial_cards method."""
    player = DummyPlayer()
    initial_table_cards = ["card1", "card2", "card3"]
    assert player.turn_initial_cards(initial_table_cards) == initial_table_cards

def test_abstract_class_enforcement():
    """Ensure Player cannot be instantiated directly."""
    with pytest.raises(TypeError):
        Player()
