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

    def calculate_score(self, player_id: str) -> None:
        pass

    def create_boards(self, players: list[Player]) -> None:
        for i in range(3):
            initial_cards = self._deck.get_six_cards()
            self._boards[i] = Board(players[i], initial_cards)
            self._boards[i].reveal_two_random_cards()

    def draw_card_from_deck(self, player_id: str) -> None:
        card = self._deck.draw_card()
        board = self.get_board_by_player_id(player_id)
        board.add_card_to_hand(card)

    def draw_card_from_discard_pile(self, player_id: str) -> None:
        card = self.get_discard_pile()
        board = self.get_board_by_player_id(player_id)
        self._clear_discard_pile()
        board.add_card_to_hand(card)

    def discard_hand(self, local_player_id: str) -> None:
        board = self.get_board_by_player_id(local_player_id)
        board.clear_hand()

    def swap_card_by_hand(self, local_player_id: str, row: int, col: int) -> None:
        board = self.get_board_by_player_id(local_player_id)
        board.swap_cards(row, col)
        self._discard_pile = board.get_hand()
        board.clear_hand()

    def reveal_player_board(self, player_id: str) -> None:
        board = self.get_board_by_player_id()
        board.reveal_board()

    def reveal_card(self, local_player_id: str, row: int, col: int) -> None:
        board = self.get_board_by_player_id(local_player_id)
        board.swap_cards(row, col)

    def set_next_player(self) -> None:
        self._current_player_order = (self._current_player_order % 3) + 1

    def is_round_finished(self) -> bool:
        for board in self._boards:
            if not board.is_all_cards_revealed():
                return False
            
        return True

    def _clear_discard_pile(self) -> None:
        self._discard_pile = None

    def get_round_number(self) -> int:
        return self._round_number
    
    def get_current_player_order(self) -> int:
        return self._current_player_order
    
    def get_discard_pile(self) -> Card:
        return self._discard_pile
    
    def get_board_by_player_id(self, player_id: str) -> Board:
        for board in self._boards:
            if board.get_player().get_id() == player_id:
                return board
    
    def _get_boards_state(self) -> list[dict]:
        boards_state: list[dict] = []
        for board in self._boards:
            boards_state.append(board.get_board_state_dict())

        return boards_state
    
    def get_state_dict(self) -> dict:
        state_dict = {}
        state_dict["deck"] = self._deck.get_current_deck_state()
        state_dict["discard_pile"] = self._discard_pile.get_id()
        state_dict["boards"] = self._get_boards_state()
        state_dict["current_player_order"] = self._current_player_order

        return state_dict