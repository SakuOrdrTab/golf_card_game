import pytest
from unittest.mock import MagicMock
from src.view import View
from src.card_deck import Card, Suit
from src.game import Game


def test_view_initialization():
    """Test that View initializes correctly."""
    mock_game = MagicMock(spec=Game)
    view = View(mock_game)
    assert view._game == mock_game, "View should hold a reference to the game instance"


def test_view_display_rows(capsys):
    """Test that _display_rows correctly displays a row."""
    mock_game = MagicMock(spec=Game)
    view = View(mock_game)
    cards = [Card(Suit.HEARTS, 1), Card(Suit.CLUBS, 2), Card(Suit.CLUBS, 3)]
    for card in cards:
        card.visible = True
    view._display_rows(cards)

    captured = capsys.readouterr()
    assert "♡1" in captured.out
    assert "♧2" in captured.out


def test_view_show_for_player_own_cards(capsys):
    """Test that show_for_player displays the player's own cards."""
    mock_game = MagicMock(spec=Game(2, human_player=False))
    view = View(mock_game)

    view.show_for_player(mock_game.players[0])

    captured = capsys.readouterr()

    assert "last played card" in captured.out

def test_default_is_not_silent():
    """Test that the default value for silent_mode is False."""
    mock_game = MagicMock(spec=Game(2, human_player=False))
    view = View(mock_game)
    assert view._silent_mode == False

def test_output(capsys):
    """Test that the silent_mode attribute is respected."""
    mock_game = MagicMock(spec=Game(2, human_player=False))

    view = View(mock_game, silent_mode=False)
    view.output("This should be printed")
    captured = capsys.readouterr()
    assert "This should be printed" in captured.out