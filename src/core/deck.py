from card import Card
import random

class Deck:
    def __init__(self):
        self._cards: list[Card] = self._get_default_deck()
        self._shuffle()

    def draw_card(self) -> Card:
        if len(self._cards) == 0:
            raise ValueError("Deck is empty")
        
        card = self._cards.pop()
        card.reveal()

        return card

    def get_six_cards(self) -> list[Card]:
        if len(self._cards) < 6:
            raise ValueError("Not enough cards in the deck")
        
        cards = []
        for _ in range(6):
            card = self._cards.pop()
            cards.append(card)
        
        return cards

    def _get_default_deck(self) -> list[Card]:
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        for suit in suits:
            for value in values:
                card = Card(value, suit)
                self._cards.append(card)
        return self._cards
    
    def _shuffle(self):
        random.shuffle(self._cards)