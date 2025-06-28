from core.suit import Suit

class Card:
    def __init__(self, value: str, suit: Suit):
        self._value = value
        self._suit = suit
        self._id = f"{self._value}_{self._suit.name}"
        self._face_up = False

    def get_score(self) -> int:
        if self._value == "A":
            return 1
        elif self._value == "2":
            return -2
        elif self._value == "K":
            return 0
        elif self._value == "Q" or self._value == "J":
            return 10
        else:
            return int(self._value)

    def get_id(self) -> str:
        return self._id
    
    def get_value(self) -> str:
        return self._value
    
    def is_face_up(self) -> bool:
        return self._face_up

    def reveal(self):
        self._face_up = True
    