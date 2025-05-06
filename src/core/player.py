class Player:
    def __init__(self, nickname: str, id: str, order: int):
        self._nickname = nickname
        self._id = id
        self._score = 0
        self._is_winner = False
        self._order = order

    def get_nickname(self) -> str:
        return self._nickname

    def get_id(self) -> str:
        return self._id
    
    def get_order(self) -> int:
        return self._order
    
    def get_score(self) -> int:
        return self._score