from player import Player
from round import Round

class Match:
    def __init__(self, players: list[Player]):
        self._players = players
        self._current_round = Round(players, 1)
        self._local_player