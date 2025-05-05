class Player:
    def __init__(self, nickname: str, id: int):
        self._nickname = nickname
        self._id = id
        self._score = 0
        self._is_winner = False
        self._is_turn = False