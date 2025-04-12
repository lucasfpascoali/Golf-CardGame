import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class PlayerInterface:
    def __init__(self):
        # Colors
        self._bg_color = "#0F3F27"
        self._primary_color = "#5CA35F"
        self._side_color = "#B7C3AD"
        self._secondary_color = "#DBE0D2"

        self.window = tk.Tk()
        self.window.title("Golf")
        self.window.geometry("1440x1024")
        self.window.resizable(False, False)
        self.window.configure(bg=self._bg_color)

        self.login_frame = None
        self.game_frame = None

        self._init_login_frame()
        self.window.mainloop()

    def _init_login_frame(self):
        # Cria o frame de login ocupando a janela toda
        self.login_frame = tk.Frame(self.window, bg=self._primary_color)
        self.login_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Frame de layout horizontal (logo à esquerda, entrada à direita)
        layout_frame = tk.Frame(self.login_frame, bg=self._primary_color)
        layout_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Logo
        img = Image.open("assets/others/logo.png") 
        img = img.resize((470, 503))
        self.logo_img = ImageTk.PhotoImage(img)

        logo_label = tk.Label(layout_frame, image=self.logo_img, bg=self._primary_color)
        logo_label.grid(row=0, column=0, padx=50)

        # Campo de entrada e botão
        right_frame = tk.Frame(layout_frame, bg=self._primary_color)
        right_frame.grid(row=0, column=1, padx=20)

        self.nickname_entry = tk.Entry(
            right_frame,
            font=("Helvetica", 16),
            width=20,
            justify="center",
            bd=0,
            bg="#E6E9DD",
            fg="#A9A9A9"
        )
        self.nickname_entry.insert(0, "Nickname")
        self.nickname_entry.pack(pady=10, ipady=10)

        # Placeholder 
        self.nickname_entry.bind("<FocusIn>", self._clear_placeholder)
        self.nickname_entry.bind("<FocusOut>", self._restore_placeholder)

        # Load the rounded button image
        btn_img = Image.open("assets/buttons/start_btn.png")
        btn_img = btn_img.resize((240, 60), Image.Resampling.LANCZOS)
        self.start_btn_img = ImageTk.PhotoImage(btn_img)

        # Button with image and centered text
        start_btn = tk.Button(
            right_frame,
            image=self.start_btn_img,
            text="START",
            compound="center",
            font=("Helvetica", 24, "bold"),
            fg="white",
            bd=0,
            bg=self._primary_color,
            activebackground=self._primary_color,
            highlightthickness=0,
            command=self._validate_and_start_game
        )
        start_btn.pack(pady=10)

    def _init_game_frame(self, nickname):
        # Destroi o login
        if self.login_frame:
            self.login_frame.destroy()

        self.game_frame = tk.Frame(self.window, bg=self._bg_color)
        self.game_frame.pack(fill="both", expand=True)
        
        # frame esquerdo
        self._create_side_frame(nickname)

        # Parte central (temporária)
        content = tk.Frame(self.game_frame, bg=self._bg_color)
        content.pack(side="right", fill="both", expand=True)

        label = tk.Label(
            content,
            text=f"Bem-vindo, {nickname}!",
            fg="white",
            bg=self._bg_color,
            font=("Helvetica", 20)
        )
        label.pack(pady=40)

    def _create_side_frame(self):
        self._side_frame = tk.Frame(self.main_window, width=295, bg=self._side_color)
        self._side_frame.pack(side="left", fill="y")
        self._create_logo()
        self._create_round_label(0)
        self._create_players_label(3)

    def _create_logo(self):
        self._logo_img = tk.PhotoImage(file="src/assets/others/logo.png")
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


    def _clear_placeholder(self, event):
        if self.nickname_entry.get() == "Nickname":
            self.nickname_entry.delete(0, tk.END)
            self.nickname_entry.config(fg="black")

    def _restore_placeholder(self, event):
        if self.nickname_entry.get() == "":
            self.nickname_entry.insert(0, "Nickname")
            self.nickname_entry.config(fg="#A9A9A9")

    def _validate_and_start_game(self):
        nickname = self.nickname_entry.get().strip()
        if not nickname or nickname == "Nickname":
            messagebox.showerror("Erro", "Digite um nickname válido.")
            return
        # Simula confirmação do servidor
        self._init_game_frame(nickname)
