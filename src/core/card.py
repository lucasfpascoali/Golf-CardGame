from suit import Suit

class Card:
    def __init__(self, value: str, suit: Suit):
        self._value = value
        self._suit = suit
        self._id = f"{self._value}_{self._suit.name}"
        self._from_deck = True
        self._face_up = False

    def reveal(self):
        self._face_up = True
    