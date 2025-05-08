from core.deck import Deck
from core.player import Player
from core.board import Board
from core.card import Card

class Round:
    def __init__(self, round_number: int):        
        self._deck : Deck = Deck()
        self._discard_pile: Card = None
        self._boards: list[Board] = [None, None, None]
        self._round_number = round_number
        self._current_player_order: int = ((round_number - 1 ) % 3) + 1

    def start_round(self, players: list[Player]) -> None:
        self._deck.load_default_deck()
        self._discard_pile = self._deck.draw_card()
        self.create_boards(players)

    def create_boards(self, players: list[Player]) -> None:
        for i in range(3):
            initial_cards = self._deck.get_six_cards()
            self._boards[i] = Board(players[i], initial_cards)
            self._boards[i].reveal_two_random_cards()
            
    def get_round_number(self) -> int:
        return self._round_number
    
    def get_discard_pile(self) -> Card:
        return self._discard_pile
    
    def get_board_by_player_id(self, player_id: str) -> Board:
        for board in self._boards:
            if board.get_player().get_id() == player_id:
                return board
        
        raise ValueError("Player not found in this round")