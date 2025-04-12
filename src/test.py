import tkinter as tk

class PlayerInterface:
    def __init__(self):
        # Colors
        self._bg_color = "#0F3F27"
        self._primary_color = "#5CA35F"
        self._side_color = "#B7C3AD"
        self._secondary_color = "#DBE0D2"

        self.main_window = tk.Tk()
        self._fill_main_window()
        self.main_window.mainloop()


    def _fill_main_window(self):
        # Config da janela
        self.main_window.title("Golf")
        self.main_window.geometry("1440x1024")
        self.main_window.resizable(False, False)
        self.main_window.config(bg=self._bg_color)
        # self.main_window.iconbitmap("../resources/logo-jogo.ico")

        # Criado frame lateral
        self._create_side_frame()

        game_frame = tk.Frame(self.main_window, bg=self._bg_color)
        game_frame.pack(side="right", fill="both")

    def _create_side_frame(self):
        self._side_frame = tk.Frame(self.main_window, width=295, bg=self._side_color)
        self._side_frame.pack(side="left", fill="y")
        self._create_logo()
        self._create_round_label(0)
        self._create_players_label(3)



    def _create_logo(self):
        self._logo_img = tk.PhotoImage(file="assets/others/logo.png")
        label_logo = tk.Label(self._side_frame, image=self._logo_img, bg=self._side_color)
        label_logo.pack(padx=10, pady=40)

    def _create_round_label(self, round_number: int):
        round_label = tk.Label(
            self._side_frame,
            text=f"Rodada {round_number}/9",
            bg=self._primary_color,
            fg="white",
            font=("Inter", 14, "bold"),
            padx=20,
            pady=10,
            width=20
        )
        round_label.pack(pady=10)
    
    def _create_players_label(self, n_players: int):
        players_label: list[tk.Label] = []
        for player in range(n_players):
            players_label.append(tk.Label(
                self._side_frame,
                text=f"Jogador {player}",
                bg=self._secondary_color,
                fg="black",
                font=("Inter", 14, "bold"),
                padx=20,
                pady=5,
                width=20
            ))
            players_label[player].pack(pady=5)
    
    def _create_player_turn_label(self, player_number: int):
        player_turn_label = tk.Label(
            self._side_frame,
            text=f"Vez do Jogador {player_number}",
            bg=self._primary_color,
            fg="white",
            font=("Inter", 14, "bold"),
            padx=20,
            pady=10,
            width=20
        )
        player_turn_label.pack(pady=20)

if __name__ == "__main__":
    PlayerInterface()