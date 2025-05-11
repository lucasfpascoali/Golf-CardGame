from core.card import Card
from core.suit import Suit
import random

class Deck:
    def __init__(self):
        self._cards: list[Card] = []

    def load_default_deck(self) -> None:
        self._cards = self._get_default_deck()
        self._shuffle()

    def load_deck(self, card_ids: list[str]) -> None:
        for card_id in card_ids:
            value, suit_name = card_id.split("_", 1)
            suit = Suit[suit_name]
            card = Card(value, suit)
            self._cards.append(card)

    def get_current_deck_state(self) -> list[str]:
        deck_state: list[str] = []
        for card in self._cards:
            deck_state.append(card.get_id())
        
        return deck_state

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
        suits = [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]
        values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        for suit in suits:
            for value in values:
                card = Card(value, suit)
                self._cards.append(card)
        return self._cards
    
    def _shuffle(self):
        random.shuffle(self._cards)