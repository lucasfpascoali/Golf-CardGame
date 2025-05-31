from core.deck import Deck
from core.player import Player
from core.board import Board
from core.card import Card
from core.suit import Suit
from dog.dog_actor import DogActor

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

    def load_round(self, round_state_dict: dict, players: list[Player]) -> None:
        self._current_player_order = round_state_dict["current_player_order"]
        self._deck.load_deck(round_state_dict["deck"])
        self._load_discard_pile(round_state_dict["discard_pile"])
        self._boards = [Board(players[0], [None, None, None, None, None, None]), Board(players[1], [None, None, None, None, None, None]), Board(players[2], [None, None, None, None, None, None])]
        self._load_boards(round_state_dict["boards"])

    def _load_discard_pile(self, card_id: str) -> None:
        value, suit_name = card_id.split('_', 1)
        suit = Suit[suit_name]
        card = Card(value, suit)
        card.reveal()
        self._discard_pile = card
    
    def _load_boards(self, boards_dict: dict[str, list[list[dict]]]) -> None:
        for player_id, matrix in boards_dict.items():
            board = self.get_board_by_player_id(player_id)
            cards = self._build_card_list(matrix)
            board.load_matrix(cards)

    def _build_card_list(self, matrix: list[list[dict]]) -> list[Card]:
        cards: list[Card] = []
        for row in range(2):
            for col in range(3):
                card_id: str = matrix[row][col]["card_id"]
                value, suit_name = card_id.split("_", 1)
                suit = Suit(suit_name)
                card = Card(value, suit)
                is_face_up = matrix[row][col]["face_up"]
                if is_face_up:
                    card.reveal()
                
                cards.append(card)

        return cards

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

    def swap_card_by_hand(self, local_player_id: str, row: int, column: int) -> None:
        board = self.get_board_by_player_id(local_player_id)
        board.swap_cards(row, column)
        self._discard_pile = board.get_hand()
        board.clear_hand()

    def reveal_player_board(self, player_id: str) -> None:
        board = self.get_board_by_player_id(player_id)
        board.reveal_board()

    def reveal_card(self, local_player_id: str, row: int, column: int) -> None:
        board = self.get_board_by_player_id(local_player_id)
        board.swap_cards(row, column)

    def set_next_player(self) -> None:
        self._current_player_order = (self._current_player_order % 3) + 1

    def is_round_finished(self, current_player_id: str) -> bool:
        board = self.get_board_by_player_id(current_player_id)
        return board.is_all_cards_revealed()

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
    
    def _get_boards_state(self) -> dict:
        boards_state: dict = {}
        for board in self._boards:
            boards_state[board.get_player().get_id()] = board.get_board_state_dict()

        return boards_state
    
    def get_state_dict(self) -> dict:
        state_dict = {}
        state_dict["deck"] = self._deck.get_current_deck_state()
        state_dict["discard_pile"] = self._discard_pile.get_id()
        state_dict["boards"] = self._get_boards_state()
        state_dict["current_player_order"] = self._current_player_order
        state_dict["round_number"] = self._round_number

        return state_dict