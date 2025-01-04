'''Advanced computer player class'''

from random import choice, randint, random
from collections import Counter
from .player import Player

class AdvancedComputerPlayer(Player):
    """
    An improved computer player.
    Incorporates slightly better heuristics and randomization.
    """

    def get_player_name(self) -> str:
        prefix = choice(["TPU-", "CPU-", "GPU-", "Azure", "Docker", "Cloud", "Hivemind"])
        postfix = choice([
            "cruncher", "grinder", "calculator", "mainframe", "brain", "totalizer",
            "calcinator", "abacus", "tron", "unit", "machina", "automaton", "system"
        ])
        return f"Advanced {prefix}{postfix} version {str(randint(1,4))}.{str(randint(1,20))}"

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

        # See if there are own pairs already and if so, draw from played
        if self._pair_in_own_tablecards(game_status['player']):
            own_pair_values = self._pairs_in_own_tablecards(game_status['player'])
            flat_pair_values = [value for sublist in own_pair_values for value in sublist]  # Flatten the list
            if str(played_top_value) in flat_pair_values:
                # print("HOPING TO SEE A TRIPLE!")
                return "p"

        # Get worst card value from the table (i.e. the largest or unknown).
        worst_card_value = self._get_worst_table_card_value(game_status['player'])

        # If the played top card is significantly better than the worst card on the table,
        # we are more likely to pick it.
        # Example: if worst_card_value = 8, and played_top_value = 5, that might be good.
        # But we also add a small random factor so it doesn't always pick from 'p'.
        if played_top_value < worst_card_value:
            # Weighted chance to pick from played pile if it's better
            if random() < 0.95:  # 80% chance if it's strictly better
                deck_choice = "p"
            else:
                deck_choice = "d"
        else:
            # Weighted chance to pick from the deck if it's not obviously better
            # We add a small chance to pick from played anyway
            if random() < 0.05:
                deck_choice = "p"
            else:
                deck_choice = "d"

        print(
            f"{self.name} draws a card from "
            f"{'deck' if deck_choice == 'd' else 'played cards'}."
        )
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

        # If there are pairs in own cards, place the card there
        if self._pair_in_own_tablecards:
            for row_index, row in enumerate(game_status['player']):
                # Extract card values (ignore suits)
                card_values = list(map(lambda x: self._parse_value(x), row))
                
                # Check if there are duplicates of the hand_value
                if Counter(card_values)[hand_value] > 1:
                    # Find the index where the card value is NOT equal to hand_value
                    non_matching_index = [col for col, card in enumerate(card_values) if card != hand_value]
                    
                    # If exactly one card does not match, process it
                    if len(non_matching_index) == 1:
                        non_matching_index = non_matching_index[0]  # Extract the single index
                        # print("PLACING A SMART ROW!")
                        # print(row_index, non_matching_index)
                        return (row_index + 1, non_matching_index + 1)
                    
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
                    if hand_value < 6 and random() < 0.9:
                        return (r + 1, c + 1)
                else:
                    # The card is known
                    # If our hand card is better (lower) by at least 2 or 3 points,
                    # we are fairly likely to replace it. (Add some randomness.)
                    if (table_value - hand_value) >= 2 and random() < 0.9:
                        return (r + 1, c + 1)

        # If we haven't found any good replacements, discard the card to the pile
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
        print(f"{self.name} turns the initial cards visible.")
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
        
    def _pair_in_own_tablecards(self, table_cards : list) -> bool:
        # discard suit:
        iterable = []
        for row in table_cards:
            new_row = []
            for column in row:
                new_row.append(column[1:])
            iterable.append(new_row)

        for row in iterable:
            strs = [item for item in row if item != "X"]
            counts = Counter(strs)
            if [item for item, count in counts.items() if count > 1] != []:
                return True
        return False
    
    def _pairs_in_others_tablecards(self, others : list) -> list:
        res = []
        for player in others:
            for row in player:
                strs = [item[1:] for item in row if item != "XX"]
                counts = Counter(strs)
                res.append([item for item, count in counts.items() if count > 1])
        return res

    def _pairs_in_own_tablecards(self, table_cards : list) -> list:
        res = []
        for row in table_cards:
            strs = [item[1:] for item in row if item != "XX"]
            counts = Counter(strs)
            res.append([item for item, count in counts.items() if count > 1])
        return res