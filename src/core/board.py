from core.player import Player
from core.card import Card
import random

class Board:
    def __init__(self, player: Player, initial_cards: list[Card]):
        self._player = player
        self._hand : Card = None
        self._matrix : list[list[Card]] = [[None for _ in range(3)] for _ in range(2)] # 2 rows and 3 columns
        self.load_matrix(initial_cards)
    
    def get_player(self) -> Player:
        return self._player

    def get_card_in_position(self, row: int, column: int) -> Card:
        return self._matrix[row][column]

    def add_card_to_hand(self, card: Card) -> None:
        if self._hand is not None:
            raise ValueError("Hand already has a card")
        
        self._hand = card

    def reveal_two_random_cards(self):
        random_positions = self._get_two_random_cards_pos()
        for row, column in random_positions:
            self.reveal_card(row, column)

    def reveal_card(self, row: int, column: int) -> None:        
        self._matrix[row][column].reveal()

    def swap_cards(self, row: int, column: int) -> None:
        if self._hand is None:
            raise ValueError("Hand is empty")
        
        if self._matrix[row][column] is None:
            raise ValueError("Position is empty")
        
        self._matrix[row][column], self._hand = self._hand, self._matrix[row][column]
        self._hand.reveal()

    def load_matrix(self, cards: list[Card]) -> None:
        if len(cards) != 6:
            raise ValueError("There must be 6 cards")
        
        for row in range(2):
            for column in range(3):
                self._set_card_in_position(cards[row * 3 + column], row, column)

    def _get_two_random_cards_pos(self) -> list[tuple[int, int]]:
        positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
        return random.sample(positions, 2)

    def _set_card_in_position(self, card: Card, row: int, column: int) -> None:
        if self._matrix[row][column] is not None:
            self._hand = self._matrix[row][column]
        
        self._matrix[row][column] = card

    
        