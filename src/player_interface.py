import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class PlayerInterface:
    def __init__(self):
        # Colors
        self._bg_color = "#0F3F27"          # dark green
        self._primary_color = "#5CA35F"     # bright green
        self._side_color = "#B7C3AD"        # very light grayish green
        self._secondary_color = "#DBE0D2"   # ice white

        self._window = tk.Tk()
        self._window.title("Golf")
        self._window.geometry("1440x1024")
        self._window.resizable(False, False)
        self._window.configure(bg=self._bg_color)

        self._login_frame = None
        self._game_frame = None

        self._init__login_frame()
        self._window.mainloop()

    def _init__login_frame(self):
        self._login_frame = tk.Frame(self._window, bg=self._primary_color)
        self._login_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._window.update()

        # Logo
        img = Image.open("assets/others/logo.png") 
        img = img.resize((500, 633))
        self.logo_img = ImageTk.PhotoImage(img)
        logo_label = tk.Label(self._login_frame, image=self.logo_img, bg=self._primary_color)
        logo_label.place(x=220, y=195)

        # Input field and button
        right_frame = tk.Frame(self._login_frame, bg=self._primary_color)
        right_frame.place(x=868, y=412)

        self.nickname_entry = tk.Entry(
            right_frame,
            font=("Helvetica", 16),
            width=20,
            justify="center",
            bd=0,
            bg=self._secondary_color,
            fg=self._side_color
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

    def _init__game_frame(self, nickname):
        # Destroy login
        if self._login_frame:
            self._login_frame.destroy()

        self._game_frame = tk.Frame(self._window, bg=self._bg_color)
        self._game_frame.place(x=0, y=0, width=1440, height=1024)

        self._create_side_frame(self._game_frame)

        self._create_game_main_frame(self._game_frame)

        self._create_local_player_board(self._game_frame)

    def _create_side_frame(self, _game_frame):
        _side_frame = tk.Frame(_game_frame, height=1024, width=295, bg=self._side_color)
        _side_frame.place(x=0, y=0)
        self._create_logo(_side_frame)
        self._create_round_label(0, _side_frame)
        self._create_players_label(3, _side_frame)
        self._create_player_turn_label(1, _side_frame)

    def _create_logo(self, _side_frame):
        self._logo_img = tk.PhotoImage(file="assets/others/logo.png")
        label_logo = tk.Label(_side_frame, image=self._logo_img, bg=self._side_color)
        label_logo.place(x=26, y=54)

    def _create_round_label(self, round_number: int, _side_frame):
        round_label = tk.Label(
            _side_frame,
            text=f"Round {round_number}/9",
            bg=self._primary_color,
            fg="white",
            font=("Inter", 14, "bold"),
            padx=20,
            pady=10,
            width=20
        )
        round_label.place(x=0, y=439, width=295, height=33)
    
    def _create_players_label(self, n_players: int, _side_frame):
        for i in range(n_players):
            player_label = tk.Label(
                _side_frame,
                text=f"Player {i + 1}: 0 pts",
                bg=self._secondary_color,
                fg=self._bg_color,
                font=("Inter", 12, "bold"),
                padx=20,
                pady=5,
                width=20
            )
            # Each label 50px below the previous one, starting at y=200 (example)
            player_label.place(x=0, y=486 + i * 40, width=295, height=33)
    
    def _create_player_turn_label(self, player_number: int, _side_frame):
        text = tk.Label(
            _side_frame, 
            text="It's the turn of:", 
            font=("Inter", 12), 
            fg="white", 
            bg=self._side_color
        )
        text.place(x=58, y=828)
        player_turn_label = tk.Label(
            _side_frame,
            text=f"Player {player_number}",
            bg=self._primary_color,
            fg=self._bg_color,
            font=("Inter", 14, "bold"),
            padx=20,
            pady=10,
            width=20
        )
        player_turn_label.place(x=0, y=853, width=295, height=33)

    def _create_game_main_frame(self, _game_frame):
        self._create_player_icons(_game_frame)   # Missing Nicknames
        self._create_deck_of_cards(_game_frame)
        self._create_discard_pile(_game_frame)
        self._create_remote_player_boards(_game_frame)

    def _create_player_icons(self, _game_frame):
        img = Image.open("assets/others/player.png") 
        img = img.resize((106, 139))
        self.player_icon = ImageTk.PhotoImage(img)
        
        # Remote players
        player_icon_label_1 = tk.Label(self._game_frame, image=self.player_icon, bg=self._bg_color)
        player_icon_label_1.place(x=323, y=70)

        player_icon_label_2 = tk.Label(self._game_frame, image=self.player_icon, bg=self._bg_color)
        player_icon_label_2.place(x=1276, y=70)

        # Local player
        img = img.resize((138, 181))
        self.player_icon_3 = ImageTk.PhotoImage(img)
        player_icon_label_3 = tk.Label(self._game_frame, image=self.player_icon_3, bg=self._bg_color)
        player_icon_label_3.place(x=1184, y=715)

    def _create_deck_of_cards(self, _game_frame):
        img = Image.open("assets/others/deck-of-cards.png") 
        img = img.resize((216, 234))
        self.deck = ImageTk.PhotoImage(img)
        deck_btn = tk.Button(
            _game_frame,
            image=self.deck,
            bd=0,
            bg=self._bg_color,
            activebackground=self._bg_color,
            highlightthickness=0,
            command=self._click_deck
        )
        deck_btn.place(x=436, y=391)

    def _create_discard_pile(self, _game_frame):
        img = Image.open("assets/others/discard-pile-default.png") 
        img = img.resize((135, 190))
        self.discard_pile = ImageTk.PhotoImage(img)
        discard_pile_btn = tk.Button(
            _game_frame,
            image=self.discard_pile,
            bd=0,
            bg=self._bg_color,
            activebackground=self._bg_color,
            highlightthickness=0,
            command=self._click_discard
        )
        discard_pile_btn.place(x=1092, y=422)

        img = Image.open("assets/others/trash-can.png") 
        img = img.resize((49, 51))
        self.trash_can = ImageTk.PhotoImage(img)
        trash_can_label = tk.Label(_game_frame, image=self.trash_can, bg=self._bg_color)
        trash_can_label.place(x=1230, y=480)

    def _create_remote_player_boards(self, _game_frame):
        # Frame for the first remote player (top left)
        remote_board_1 = tk.Frame(
            _game_frame,
            bg=self._bg_color,
            padx=0,
            pady=0,
            bd=0,
            highlightthickness=0
        )
        remote_board_1.place(x=450, y=50, width=310, height=310)
        
        # Frame for the second remote player (top right)
        remote_board_2 = tk.Frame(
            _game_frame,
            bg=self._bg_color,
            padx=0,
            pady=0,
            bd=0,
            highlightthickness=0
        )
        remote_board_2.place(x=950, y=50, width=310, height=310)
        
        # Add face-down cards for each remote board (images only)
        self._add_remote_player_cards(remote_board_1, 1)
        self._add_remote_player_cards(remote_board_2, 2)

    def _add_remote_player_cards(self, parent_frame, player_index, card_size=(90, 141)):
        img = Image.open("assets/cards/back.png")
        img = img.resize(card_size)
        # Use a different variable for each player
        setattr(self, f"remote_card_back_img_{player_index}", ImageTk.PhotoImage(img))
        
        # Create 2x3 grid of cards (images only)
        for row in range(2):
            for col in range(3):
                card_label = tk.Label(
                    parent_frame,
                    image=getattr(self, f"remote_card_back_img_{player_index}"),
                    bg=self._bg_color
                )
                card_label.grid(row=row, column=col, padx=5, pady=5)

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
            messagebox.showerror("Error", "Please enter a valid nickname.")
            return
        # Simulate server confirmation
        self._init__game_frame(nickname)

    def _create_local_player_board(self, _game_frame):
        # Main frame for local player board
        local_board = tk.Frame(
            _game_frame,
            bg=self._bg_color,
            padx=0,
            pady=0,
            bd=0,
            highlightthickness=0
        )
        local_board.place(x=600, y=550, width=470, height=450)
        
        # Frame for cards
        cards_frame = tk.Frame(
            local_board, 
            bg=self._bg_color,
            bd=0,
            highlightthickness=0
        )
        cards_frame.pack(expand=False)
        
        # Add face-down cards (back cards)
        self._add_back_cards(cards_frame)
        
    
    def _add_back_cards(self, parent_frame, card_size=(125, 196), clickable=True):
        img = Image.open("assets/cards/back.png")
        img = img.resize(card_size)
        self.card_back_img = ImageTk.PhotoImage(img)
        
        # Create 2x3 grid of cards
        for row in range(2):
            for col in range(3):
                card_label = tk.Label(
                    parent_frame,
                    image=self.card_back_img,
                    bg=self._bg_color
                )
                card_label.grid(row=row, column=col, padx=10, pady=5)
                
                # Add click event only if cards are clickable
                if clickable:
                    card_index = row * 3 + col  # Calculate index based on position
                    card_label.bind("<Button-1>", lambda e, idx=card_index: self._on_card_click(idx))
                
        
    def _on_card_click(self, card_index):
        print(f"Card {card_index+1} clicked")
        # Here you can implement the logic to flip the card

    def _on_discard_click(self):
        print("discard pile clicked")

    def _on_deck_click(self):
        print("draw pile clicked!")

if __name__ == "__main__":
    PlayerInterface()