'''Card class for the Gulf card game'''

from enum import Enum

class Suit(Enum):
    '''Enumeration for the suits of a card'''
    SPADES = '\U00002664'
    HEARTS = '\U00002661'
    DIAMONDS = '\U00002662'
    CLUBS = '\U00002667'

class Card:
    '''Class for a card in the Gulf card game'''



    def __init__(self, suit: Suit, value: int):
        self.suit = suit
        if value < 0 or value > 12:
            raise ValueError('Value must be between 0 and 12')
        self.value = value

    def __str__(self):
        return f'{self.suit.value}{self.value}'

    def __repr__(self):
        return f'{self.suit.value}{self.value}'

    def __eq__(self, value):
        return self.value == value

    def __lt__(self, value):
        return self.value < value

    def __gt__(self, value):
        return self.value > value

    def __le__(self, value):
        return self.value <= value

    def __ge__(self, value):
        return self.value >= value

    def __ne__(self, value):
        return self.value != value

    def __add__(self, value):
        if isinstance(value, Card):
            return self.value + value.value
        elif isinstance(value, int):
            return self.value + value
        else:
            raise ValueError('Unsupported operand type')

    def __sub__(self, value):
        if isinstance(value, Card):
            return self.value - value.value
        elif isinstance(value, int):
            return self.value - value
        else:
            raise ValueError('Unsupported operand type')

if __name__ == '__main__':
    card1 = Card(Suit.SPADES, 10)
    card2 = Card(Suit.HEARTS, 5)
    card3 = Card(Suit.DIAMONDS, 10)

    print(card1 + card2)
    print(card1 > card2)
    print(card1 == card3)
