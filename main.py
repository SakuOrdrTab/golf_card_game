from src import Card, CardDeck, Suit

if __name__ == '__main__':
    deck = CardDeck()
    print("Initial drawing deck", deck.drawing_deck)
    print("Length of drawing deck befpre operations: ", len(deck.drawing_deck))
    deck.deal_first_card()
    print("After dealing the first card to table:\n", deck.drawing_deck)
    print("..and the played cards:\n", deck.played_cards)
    print("Drawing a card from the deck: ", deck.draw_from_deck())
