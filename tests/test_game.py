import pytest
from unittest.mock import MagicMock, patch
from src.game import Game
from src.card_deck import CardDeck, Card, Suit
from src.player.computer_player import ComputerPlayer


def test_game_initialization():
    """Test game initializes with the correct number of players."""
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
    mock_player.name = "test"

    with patch("src.card_deck.CardDeck", return_value=mock_deck):
        game = Game(num_players=2, human_player=False)

        # Test drawing from the played pile
        card = game.player_gets_card(mock_player)
        assert isinstance(card, Card)

        # Test drawing from the deck
        card = game.player_gets_card(mock_player)
        assert isinstance(card, Card)

def test_game_status_player_own_cards():
    """Test that the player's own cards are correctly included."""
    # Create mock player
    player1 = MagicMock(spec=ComputerPlayer, table_cards=[
        [Card(Suit.HEARTS, 1), Card(Suit.CLUBS, 2)],
        [Card(Suit.DIAMONDS, 3), Card(Suit.SPADES, 4)],
    ])
    for row in player1.table_cards:
        for card in row:
            card.visible = True

    # Mock game
    game = Game(num_players=2, human_player=False)
    game.players = [player1]

    game_status = game.get_game_status_for_player(player1)
    assert game_status["player"] == [['♡1', '♧2'], ['♢3', '♤4']],\
          "Player's own visible cards should match"


def test_game_status_other_players_cards():
    """Test that other players' cards are correctly included."""
    # Create mock players
    player1 = MagicMock(spec=ComputerPlayer, table_cards=[])
    player2 = MagicMock(spec=ComputerPlayer, table_cards=[
        [Card(Suit.CLUBS, 5), Card(Suit.DIAMONDS, 6)],
        [Card(Suit.SPADES, 7), Card(Suit.HEARTS, 8)],
    ])
    for row in player2.table_cards:
        for card in row:
            card.visible = True

    game = Game(num_players=2, human_player=False)
    game.players = [player1, player2]

    game_status = game.get_game_status_for_player(player1)
    assert len(game_status["other_players"]) == 1
    assert game_status["other_players"][0] == [['♧5', '♢6'], ['♤7', '♡8']], \
    "Other players' visible cards should match"


def test_game_status_played_top_card():
    """Test that the top card of the played deck is included."""
    # Create mock player
    player1 = MagicMock(spec=ComputerPlayer, table_cards=[])

    # Mock game and deck
    with patch("src.card_deck.CardDeck") as mock_deck:
        mock_deck.get_last_played_card.return_value = Card(Suit.DIAMONDS, 9)
        game = Game(num_players=2, human_player=False)
        game.deck.played_cards = [Card(Suit.DIAMONDS, 9)]

        game_status = game.get_game_status_for_player(player1)
        assert game_status["played_top_card"].suit == Suit.DIAMONDS
        assert game_status["played_top_card"].value == 9


def test_game_status_hand_card():
    """Test that the hand card is included if provided."""
    # Create mock player
    player1 = MagicMock(spec=ComputerPlayer, table_cards=[])

    # Mock game
    game = Game(num_players=2, human_player=False)

    # Test with a hand card
    hand_card = Card(Suit.CLUBS, 10)
    game_status = game.get_game_status_for_player(player1, hand_card=hand_card)
    assert game_status["hand_card"] == hand_card, "Hand card should match the provided card"


def test_game_status_no_hand_card():
    """Test that hand card is excluded if not provided."""
    # Create mock player
    player1 = MagicMock(spec=ComputerPlayer, table_cards=[])

    # Mock game
    game = Game(num_players=2, human_player=False)

    # Test without a hand card
    game_status = game.get_game_status_for_player(player1)
    assert "hand_card" not in game_status, "Hand card should not be included if not provided"

def test_play_game_completes_properly():
    """Test that play_game completes once all conditions are met."""
    game = Game(num_players=2, human_player=False)
    for player in game.players:
        player.table_cards = [[Card(Suit.CLUBS, i) for i in range(1, 4)] for _ in range(3)]
        for row in player.table_cards:
            for card in row:
                card.visible = True  # All cards visible to simulate game-end condition

    result = game.play_game()
    assert result[0] > 0, "Game should play at least one turn"
    assert result[2] in result[1], "Winner's name should be in the scores"

def test_play_game_tied_scores():
    """Test play_game handles tied scores correctly."""
    game = Game(num_players=2, human_player=False)
    for player in game.players:
        player.table_cards = [[Card(Suit.SPADES, _) for _ in range(3)] for _ in range(3)]
        for row in player.table_cards:
            for card in row:
                card.visible = True  # All cards visible to simulate game-end condition

    assert game.player_score(game.players[0]) ==  game.player_score(game.players[1]), "Scores should be tied"

def test_play_game_max_players():
    """Test play_game works with the maximum number of players."""
    game = Game(num_players=3, human_player=False)
    for player in game.players:
        player.table_cards = [[Card(Suit.DIAMONDS, i) for i in range(1, 4)] for _ in range(3)]
        for row in player.table_cards:
            for card in row:
                card.visible = True  # All cards visible to simulate game-end condition

    result = game.play_game()
    assert result[0] > 0, "Game should play at least one turn"
    assert len(result[1]) == 3, "Scores should include all players"
    assert result[2] in result[1], "Winner's name should be in the scores"

def test_play_game_min_players():
    """Test play_game works with the minimum number of players."""
    game = Game(num_players=2, human_player=False)
    for player in game.players:
        player.table_cards = [[Card(Suit.HEARTS, i) for i in range(1, 4)] for _ in range(3)]
        for row in player.table_cards:
            for card in row:
                card.visible = True  # All cards visible to simulate game-end condition

    result = game.play_game()
    assert result[0] > 0, "Game should play at least one turn"
    assert len(result[1]) == 2, "Scores should include all players"
    assert result[2] in result[1], "Winner's name should be in the scores"

def test_play_game_returns_tuple():
    """Test that play_game returns a tuple."""
    game = Game(num_players=2, human_player=False)
    
    result = game.play_game()

    assert isinstance(result, tuple), "play_game should return a tuple"
