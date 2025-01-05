'''Very simple computer player class'''

# A Note: This computer player actually cheats. Unfortunately the algorithm 
# accesses self.table_cards, which of course holds also the hidden values
# not to be seen during the game.

from random import choice, randint, random
from .player import Player

class ComputerPlayer(Player):
    """
    An improved (but still relatively simple) computer player.
    Incorporates slightly better heuristics and randomization.
    """

    def get_player_name(self) -> str:
        prefix = choice(["TPU-", "CPU-", "GPU-", "Azure", "Docker", "Amiga", "Linux"])
        postfix = choice([
            "cruncher", "grinder", "calculator", "laptop",
            "calcinator", "abacus", "tron", "unit", "machina"
        ])
        return prefix + postfix

    def get_draw_action(self, game_status: dict) -> str:
        """
        Decide whether to draw from the (d)eck or from the (p)layed pile.
        The logic is:
          - Check the worst card on our table (highest or unknown).
          - If the played top card is strictly better (lower) than that worst
            card, we lean toward picking it (p).
          - Otherwise, we usually pick from the deck (d).
          - We also add some random factor to keep it from being fully predictable.
        """
        played_top_value = game_status['played_top_card'].value

        # Get worst card value from the table (i.e. the largest or unknown).
        worst_card_value = self._get_worst_table_card_value(game_status['player'])

        # If the played top card is significantly better than the worst card on the table,
        # we are more likely to pick it.
        # Example: if worst_card_value = 8, and played_top_value = 5, that might be good.
        # But we also add a small random factor so it doesn't always pick from 'p'.
        if played_top_value < worst_card_value:
            # Weighted chance to pick from played pile if it's better
            if random() < 0.9:  # 80% chance if it's strictly better
                deck_choice = "p"
            else:
                deck_choice = "d"
        else:
            # Weighted chance to pick from the deck if it's not obviously better
            # We add a small chance to pick from played anyway
            if random() < 0.1:
                deck_choice = "p"
            else:
                deck_choice = "d"

        # print(
        #     f"{self.name} draws a card from "
        #     f"{'deck' if deck_choice == 'd' else 'played cards'}."
        # )
        return deck_choice

    def get_play_action(self, game_status: dict) -> tuple:
        """
        Decide where to place the hand card:
          - We check each card on the table in ascending order, 
            looking for a "good" candidate to replace.
          - Prefer to replace unknown (hidden) cards, but only 
            if we think our hand card is decent.
          - If we find a known card that is worse than our hand card, 
            we replace it with some probability.
          - If we don't find any great replacement, we discard to the pile.
        """
        hand_card = game_status['hand_card']
        hand_value = hand_card.value

        # We'll loop over the table cards in row-major order
        # to find a suitable spot to play. 
        # The first "good enough" spot we find, we play.
        for r, row in enumerate(game_status['player']):
            for c, card_str in enumerate(row):
                table_value = self._parse_value(card_str)

                # If the card is hidden (unknown), we approximate 
                # it with some average or mid-range value.
                # parse_value above handles that, but let's keep it in a var
                # to do some logic around it.
                is_hidden = card_str.startswith("X")

                # A simple logic:
                #   - If hidden, we consider that it's "probably" around 6.
                #   - If our hand_value is significantly better (like 3 or less),
                #     we might want to replace it. 
                #   - If the card is known and the hand card is significantly better,
                #     we might also replace it.
                # We'll add some random chance to not be too predictable.
                if is_hidden:
                    # random factor & condition that our hand is decently small
                    if hand_value < 7 and random() < 0.9:
                        # print(
                        #     f"{self.name} plays the card {hand_card} "
                        #     f"on a hidden card at row={r+1}, col={c+1}."
                        # )
                        return (r + 1, c + 1)
                else:
                    # The card is known
                    # If our hand card is better (lower) by at least 2 or 3 points,
                    # we are fairly likely to replace it. (Add some randomness.)
                    if (table_value - hand_value) >= 2 and random() < 0.9:
                        # print(
                        #     f"{self.name} replaces a known card (val={table_value}) with "
                        #     f"{hand_card} at row={r+1}, col={c+1}."
                        # )
                        return (r + 1, c + 1)

        # If we haven't found any good replacements, discard the card to the pile
        # print(
        #     f"{self.name} discards the card {hand_card} to the played deck."
        # )
        return ("p", None)

    def turn_initial_cards(self, initial_table_cards):
        """
        Which cards to flip at the beginning?
        Simple logic: flip 2 random cards from each row, or just 1, 
        or something that helps start the game. This depends on your game rules.
        Below, we flip exactly 1 random card from each row as an example.
        """
        result = []
        for r, row in enumerate(initial_table_cards):
            # Flip exactly 1 card from each row
            flip_col = randint(1, len(row))
            result.append((r + 1, flip_col))
        # print(f"{self.name} turns the initial cards visible.")
        return result

    def _get_worst_table_card_value(self, table_cards) -> int:
        """
        Helper to find the worst card value (highest) on our table.
        For unknown (hidden) cards, assume a mid-range (e.g., 6).
        """
        worst_value = -1
        for row in table_cards:
            for card_str in row:
                val = self._parse_value(card_str)
                if val > worst_value:
                    worst_value = val
        return worst_value

    def _parse_value(self, card_str) -> int:
        """
        Safely parse card values.
        If the card is unknown (like 'XX'), we treat it as ~6.
        You could adjust that to a random guess in [4..7], or something else.
        """
        # If it's hidden or we can't parse it, approximate
        if card_str.startswith("XX"):
            return 6  # assume average card
        try:
            return int(card_str[1:])
        except ValueError:
            # If anything goes wrong, return ~6
            return 6
        
    def inform_game_result(self, win: bool, relative_score: int) -> None:
        """
        Inform the player about the game result.
        """
        return None