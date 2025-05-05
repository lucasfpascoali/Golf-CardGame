from deck import Deck
from player import Player
from board import Board

class Round:
    def __init__(self, players: list[Player], round_number: int):        
        self._deck = Deck()
        self._discard_pile = self._deck.draw_card()
        self._boards = self._build_boards(players)
        self._round_number = round_number

    def get_round_number(self) -> int:
        return self._round_number
    
    def get_board_by_player_id(self, player: Player) -> Board:
        for board in self._boards:
            if board.get_player() == player:
                return board
        
        raise ValueError("Player not found in this round")

    def _build_boards(self, players: list[Player]) -> list[Player]:
        boards = []
        for player in players:
            initial_cards = self._deck.get_six_cards()
            board = Board(player, initial_cards)
            boards.append(board)
        
        return boards