'''Card deck class for the golf game'''

from card import Card, Suit

from random import shuffle

class CardDeck:
    '''Class for a deck of cards'''
    def __init__(self) -> None:
        self.drawing_deck = []
        self.played_cards = []
        for suit in Suit:
            for value in range(13):
                self.drawing_deck.append(Card(suit, value))
        shuffle(self.drawing_deck)

    def draw_from_deck(self) -> Card:
        '''Draw a card from the deck. If the deck is empty, shuffle the played cards and use them as the deck.
        The card is the first item in the drawing deck list'''
        # If deck is empty, shuffle the played cards and use them as the deck
        if len(self.drawing_deck) == 0:
            self.drawing_deck = self.played_cards
            self.played_cards = []
            shuffle(self.drawing_deck)
        card = self.drawing_deck.pop(0)
        return card

    def deal_first_card(self) -> None:
        '''Deal the first card from the deck to the played deck'''
        self.played_cards.append(self.draw_from_deck())

    def draw_from_played(self) -> Card:
        '''Draw a card from the played cards. The drawn card is the last card in the played cards list'''
        if len(self.played_cards) == 0:
            raise ValueError('No cards in the played deck')
        card = self.played_cards.pop()
        return card
    
    def add_to_played(self, card: Card) -> None:
        '''Add a card to the played cards'''
        self.played_cards.append(card)

    def get_last_played_card(self) -> Card:
        '''Get the last played card'''
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