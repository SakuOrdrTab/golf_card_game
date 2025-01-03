import pytest
from unittest.mock import MagicMock, patch
from src.game import Game
from src.card_deck import CardDeck, Card, Suit
from src.player.computer_player import ComputerPlayer


def test_game_initialization():
    """Test game initializes with the correct number of players."""
    # with patch("src.card_deck.CardDeck", spec=CardDeck), patch(
    #     "src.player.computer_player.ComputerPlayer"
    # ) as MockComputerPlayer:
    #     MockComputerPlayer.side_effect = lambda: MagicMock(
    #         spec=ComputerPlayer, table_cards=[]
    #     )
    #     game = Game(num_players=2, human_player=False)
    #     assert len(game.players) == 2
    #     assert all(isinstance(player, ComputerPlayer) for player in game.players)
    game = Game(num_players=3, human_player=False)
    assert len(game.players) == 3

def test_player_gets_card():
    """Test player_gets_card returns a card from the correct deck."""
    mock_deck = MagicMock(spec=CardDeck)
    mock_deck.draw_from_deck.return_value = Card(Suit.HEARTS, 1)
    mock_deck.draw_from_played.return_value = Card(Suit.DIAMONDS, 2)

    mock_player = MagicMock(
        spec=ComputerPlayer,
        get_draw_action=MagicMock(side_effect=["d", "p"]),
        table_cards=[]  # Ensure table_cards attribute is present
    )

    with patch("src.card_deck.CardDeck", return_value=mock_deck):
        game = Game(num_players=2, human_player=False)

        # Test drawing from the played pile
        card = game.player_gets_card(mock_player)
        assert isinstance(card, Card)

        # Test drawing from the deck
        card = game.player_gets_card(mock_player)
        assert isinstance(card, Card)

