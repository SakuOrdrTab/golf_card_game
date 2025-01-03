import pytest
from unittest.mock import MagicMock, patch
from src.game import Game
from src.player.computer_player import ComputerPlayer
from src.card_deck import CardDeck, Card, Suit


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
    """Test player_gets_card returns the correct card."""
    mock_deck = MagicMock(spec=CardDeck)
    mock_deck.draw_from_deck.return_value = Card(Suit.HEARTS, 1)
    mock_deck.draw_from_played.return_value = Card(Suit.DIAMONDS, 2)

    mock_player = MagicMock(
        spec=ComputerPlayer, get_draw_action=MagicMock(side_effect=["d", "p"])
    )

    with patch("src.card_deck.CardDeck", return_value=mock_deck):
        game = Game(num_players=2, human_player=False)
        card = game.player_gets_card(mock_player)
        assert card.suit == Suit.HEARTS

        card = game.player_gets_card(mock_player)
        assert card.suit == Suit.DIAMONDS


def test_player_plays_card():
    """Test player_plays_card updates the game state correctly."""
    mock_deck = MagicMock(spec=CardDeck)
    hand_card = Card(Suit.HEARTS, 5)
    mock_deck.add_to_played = MagicMock()

    mock_player = MagicMock(
        spec=ComputerPlayer,
        get_play_action=MagicMock(side_effect=[("p", None), (1, 2)]),
        table_cards=[[Card(Suit.CLUBS, 3), Card(Suit.DIAMONDS, 4)]],
    )

    with patch("src.card_deck.CardDeck", return_value=mock_deck):
        game = Game(num_players=2, human_player=False)
        game.player_plays_card(mock_player, hand_card)
        mock_deck.add_to_played.assert_called_with(hand_card)

        mock_player.get_play_action.return_value = (1, 2)
        game.player_plays_card(mock_player, hand_card)
        assert mock_player.table_cards[0][1]
