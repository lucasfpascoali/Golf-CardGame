from core.player import Player
from core.round import Round
from core.board import Board

class Match:
    def __init__(self, players_info: list[list[str]], local_player_id: str):
        self._players: list[Player] = self._build_players(players_info)
        self._current_round: Round = None
        self._local_player = self._get_player_by_id(local_player_id)
        self._is_running: bool = False
        self._current_order: int = 0 

    def start_match(self) -> dict:
        if self._is_running:
            raise RuntimeError("Match is already running.")
        
        self._is_running = True
        self.start_round(1)

    def start_round(self, round_number: int):        
        self._current_round = Round(round_number)
        self._current_round.start_round(self._players)

    def get_local_player(self) -> Player:
        return self._local_player
        
    def get_current_player(self) -> Player:
        return self._get_player_by_order(self._current_order + 1)

    def get_current_round(self) -> Round:
        return self._current_round
    
    def get_local_player_board(self) -> Board:
        return self._current_round.get_board_by_player_id(self._local_player.get_id())
    
    def get_remote_players_boards(self) -> list[Board]:
        remote_players_boards = []
        for player in self._players:
            if player.get_id() != self._local_player.get_id():
                remote_players_boards.append(self._current_round.get_board_by_player_id(player.get_id()))
        
        return remote_players_boards

    def next_order(self) -> None:
        self._current_order = (self._current_order + 1) % 3 # Loop back to the first player (Always 3 players)

    def _get_player_by_order(self, order: int) -> Player:
        for player in self._players:
            if player.get_order() == order:
                return player
        
        raise ValueError("Player not found with the given order.")
    
    def _get_player_by_id(self, player_id: str) -> Player:
        for player in self._players:
            if player.get_id() == player_id:
                return player
        
        raise ValueError("Player not found with the given ID.")

    def _build_players(self, players: list[list[str]]) -> list[Player]:
        if len(players) < 3:
            raise ValueError("At least 3 players are required to start a match.")

        player_list = []
        for player in players:
            player_list.append(Player(player[0], player[1], int(player[2])))
        
        return player_list
    
    