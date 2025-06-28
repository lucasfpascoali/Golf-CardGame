from core.player import Player
from core.card import Card
import random

class Board:
    def __init__(self, player: Player, initial_cards: list[Card]):
        self._player = player
        self._hand : Card = None
        self._matrix : list[list[Card]] = [[None for _ in range(3)] for _ in range(2)] # 2 rows and 3 columns
        self.load_matrix(initial_cards)
    
    def get_board_state_dict(self) -> list[list[dict]]:
        matrix: list[list[dict]] = [[None, None, None], [None, None, None]]
        for row in range(2):
            for col in range(3):
                pos_dict = {}
                pos_dict["face_up"] = self._matrix[row][col].is_face_up()
                pos_dict["card_id"] = self._matrix[row][col].get_id()
                matrix[row][col] = pos_dict
            
        return matrix

    def get_player(self) -> Player:
        return self._player

    def get_card_in_position(self, row: int, column: int) -> Card:
        return self._matrix[row][column]
    
    def get_hand(self) -> Card:
        return self._hand

    def add_card_to_hand(self, card: Card) -> None:    
        self._hand = card # TODO: Possible change in VPS

    def clear_hand(self) -> None:
        self._hand = None

    def reveal_two_random_cards(self):
        random_positions = self._get_two_random_cards_pos()
        for row, column in random_positions:
            self.reveal_card(row, column)

    def reveal_card(self, row: int, column: int) -> None:        
        self._matrix[row][column].reveal()

    def reveal_board(self) -> None:
        for row in range(2):
            for col in range(3):
                self._matrix[row][col].reveal() 

    def swap_cards(self, row: int, column: int) -> None:
        self._matrix[row][column], self._hand = self._hand, self._matrix[row][column]
        self._hand.reveal()

    def is_all_cards_revealed(self) -> bool:
        for row in range(2):
            for col in range(3):
                if not self._matrix[row][col].is_face_up():
                    return False
                
        return True

    def load_matrix(self, cards: list[Card]) -> None:        
        for row in range(2):
            for column in range(3):
                self._matrix[row][column] = cards[row * 3 + column]

    def _get_two_random_cards_pos(self) -> list[tuple[int, int]]:
        positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
        return random.sample(positions, 2)

    
        