'''Card deck class for the golf game'''

from random import shuffle
from .card import Card, Suit

class CardDeck:
    """A Card deck specific to Golf card game. Contains drawing deck and played
    card deck.
    """    
    def __init__(self) -> None:
        """Initializes the deck: builds drawing deck
        """        
        self.drawing_deck = []
        self.played_cards = []
        for suit in Suit:
            for value in range(13):
                self.drawing_deck.append(Card(suit, value))
        shuffle(self.drawing_deck)

    def draw_from_deck(self) -> Card:
        """Returns a Card from drawing deck. If deck is empty, the played cards
        are returned to the drawing deck and shuffled.

        Returns:
            Card: One card from the drawing deck
        """        
        # If deck is empty, shuffle the played cards and use them as the deck
        if len(self.drawing_deck) == 0:
            self.drawing_deck = self.played_cards
            self.played_cards = []
            shuffle(self.drawing_deck)
        card = self.drawing_deck.pop(0)
        return card

    def deal_first_card(self) -> None:
        """Called by Game() constructor, adds one card to the played deck
        """        
        self.played_cards.append(self.draw_from_deck())
        self.played_cards[-1].visible = True

    def draw_from_played(self) -> Card:
        """Returns the last Card from the played deck and removes from
        played deck.

        Raises:
            ValueError: No Cards in the played deck, this should not happen

        Returns:
            Card: Card from played deck
        """        
        if len(self.played_cards) == 0:
            raise ValueError('No cards in the played deck')
        card = self.played_cards.pop()
        return card

    def add_to_played(self, card: Card) -> None:
        """Adds a card to the played deck

        Args:
            card (Card) :
        """        
        card.visible = True # Ensure card is always visible in played deck
        self.played_cards.append(card)

    def get_last_played_card(self) -> Card:
        """Getter to get the last played card from the played deck, but NOT
        remove it. This is just to get the value of the card as it can be seen
        by players

        Raises:
            ValueError: Should not happen, no cards in played deck

        Returns:
            Card: top Card in played deck
        """        
        if len(self.played_cards) == 0:
            raise ValueError('No cards in the played deck')
        return self.played_cards[-1]


if __name__ == '__main__':
    deck = CardDeck()
    print("Initial drawing deck", deck.drawing_deck)
    print("Length of drawing deck befpre operations: ", len(deck.drawing_deck))
    deck.deal_first_card()
    print("After dealing the first card to table:\n", deck.drawing_deck)
    print("..and the played cards:\n", deck.played_cards)
