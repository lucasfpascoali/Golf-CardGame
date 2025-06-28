from core.player import Player
from core.round import Round
from core.board import Board
from dog.dog_actor import DogActor

# Move Object Structure
# a_move = {
#   "match_status": "next" | "finished" (exigência do DOG, ainda existe um terceiro valor possível, mas não há uso neste programa),
#   "current_round": {
#       round_number : int,
#       deck: list[str], -> string vai ser o card id, a partir dele construímos as cartas (cartas do baralho são sempre face-up false)
#       discard_pile: str, -> string do card id, face up vai ser sempre true
#       boards: dict, -> um dict para cada board, o dict vai ter o player_id e um matrix (duas listas para o grid 2x3, cada posicao do grid possui um dict com card id e face up)
#       current_player_order: int
#   }
#   "scores": dict[str, int] -> mapeia o id do player para um inteiro representando a pontuação do jogador 
# }

class Match:
    def __init__(self, players_info: list[list[str]], local_id: str):
        self._players: list[Player] = self._build_players(players_info)
        self._current_round: Round = None
        self._local_player_id = local_id
        self._is_running: bool = False

    # TODO: changes to VPS
    def start_match(self) -> dict:        
        self.set_as_running()
        self.start_round(1)
        a_move = self.get_move_dict()
        return a_move

    def load_match(self, a_move: dict) -> None:
        self._current_round = Round(a_move["current_round"]["round_number"])
        self._current_round.load_round(a_move["current_round"], self._players)
        self._load_score(a_move["scores"])
        if a_move["match_status"] == "finished":
            self.set_as_finished()
    
    def _load_score(self, scores: dict[str, int]) -> None:
        for player_id, score in scores.items():
            player = self._get_player_by_id(player_id)
            player.set_score(score)
            
    def set_as_running(self) -> None:
        self._is_running = True

    def set_as_finished(self) -> None:
        self._is_running = False

    # TODO: changes to VPS
    def start_round(self, round_number: int) -> None:        
        self._current_round = Round(round_number)
        self._current_round.start_round(self._players) 
        # a_move = self.get_move_dict()
        # dog.send_move(a_move)

    def end_round(self) -> None:
        round_number = self._current_round.get_round_number()
        if round_number == 9:
            self.set_as_finished()

        self.show_round_results()

    def draw_card_from_deck(self) -> None:
        self._current_round.draw_card_from_deck(self._local_player_id)

    def draw_card_from_discard_pile(self) -> None:
        self._current_round.draw_card_from_discard_pile(self._local_player_id)

    def discard_hand(self) -> None:
        self._current_round.discard_hand(self._local_player_id)

    def swap_card_by_hand(self, row: int, column: int) -> None:
        self._current_round.swap_card_by_hand(self._local_player_id, row, column)

    def reveal_card(self, row: int, column: int) -> None:
        self._current_round.reveal_card(self._local_player_id, row, column)

    # TODO: changes to VPS
    def end_of_turn(self) -> None:
        self._current_round.set_next_player()

    def show_round_results(self) -> None:
        players = self.get_players()
        for i in range(3):
            player_id = players[i].get_id()
            self._current_round.calculate_score(player_id)
            self._current_round.reveal_player_board(player_id)

    def is_local_player_turn(self) -> bool:
        return self._current_round.get_current_player_order() == self.get_local_player().get_order()

    def is_running(self) -> bool:
        return self._is_running
    
    def is_round_finished(self) -> bool:
        return self._current_round.is_round_finished(self._local_player_id)
    
    def get_players(self) -> list[Player]:
        return self._players

    def get_local_player(self) -> Player:
        return self._get_player_by_id(self._local_player_id)
    
    def get_remote_players(self) -> list[Player]:
        remote_players = []
        for player in self._players:
            if player.get_id() != self._local_player_id:
                remote_players.append(player)
        
        return remote_players
        
    def get_current_player(self) -> Player:
        current_player_order = self._current_round.get_current_player_order()
        return self._get_player_by_order(current_player_order)

    def get_current_round(self) -> Round:
        return self._current_round
    
    def get_local_player_board(self) -> Board:
        return self._current_round.get_board_by_player_id(self._local_player_id)
    
    def get_remote_players_boards(self) -> list[Board]:
        remote_players_boards = []
        for player in self._players:
            if player.get_id() != self._local_player_id:
                remote_players_boards.append(self._current_round.get_board_by_player_id(player.get_id()))
        
        return remote_players_boards

    def get_discard_pile_card_id(self) -> str:
        card = self._current_round.get_discard_pile()
        if card == None:
            return "" # TODO: Change to be made to VPS

        return card.get_id()
    
    def get_round_number(self) -> int:
        return self._current_round.get_round_number()

    def get_players_scoreboard_string(self) -> str:
        scoreboard_dict = self._get_players_scores_dict()
        return self._format_scoreboard(scoreboard_dict)

    def _format_scoreboard(self, scoreboard_dict: dict[str, int]) -> str:
        # Ordena pelo score ascendente (menor primeiro)
        sorted_players = sorted(scoreboard_dict.items(), key=lambda kv: kv[1])
        # Monta as linhas e junta com “\n”
        return "\n".join(f"{player}: {score} pts" for player, score in sorted_players)

    def get_move_dict(self) -> dict:
        a_move: dict = {}
        a_move["match_status"] = "next" if self.is_running() else "finished"
        a_move["current_round"] = self._current_round.get_state_dict()
        a_move["scores"] = self._get_players_scores_dict()
        return a_move

    def _get_players_scores_dict(self) -> dict[str, int]:
        scores_dict = {}
        for player in self._players:
            scores_dict[player.get_id()] = player.get_score()

        return scores_dict

    def _get_player_by_order(self, order: int) -> Player:
        for player in self._players:
            if player.get_order() == order:
                return player
    
    def _get_player_by_id(self, player_id: str) -> Player:
        for player in self._players:
            if player.get_id() == player_id:
                return player

    def _build_players(self, players: list[list[str]]) -> list[Player]:
        player_list = []
        for player in players:
            player_list.append(Player(player[0], player[1], int(player[2])))
        
        return player_list
    
    