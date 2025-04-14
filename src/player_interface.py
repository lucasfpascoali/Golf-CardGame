from tkinter import messagebox, Tk, PhotoImage, Label, Frame, Entry, Button, END
from PIL import Image, ImageTk

class PlayerInterface:
    def __init__(self):
        # Colors
        self._bg_color = "#0F3F27"          # dark green
        self._primary_color = "#5CA35F"     # bright green
        self._side_color = "#B7C3AD"        # very light grayish green
        self._secondary_color = "#DBE0D2"   # ice white

        self._window = Tk()
        self._window.title("Golf")
        self._window.geometry("1440x1024")
        self._window.resizable(False, False)
        self._window.configure(bg=self._bg_color)

        # Frames
        self._login_frame: Frame = None
        self._game_frame: Frame = None
        self._side_frame: Frame = None
        self._right_frame: Frame = None
        self._remote_players_boards : list[Frame] = []
        self._local_player_board: Frame = None
        self._local_player_cards_frame: Frame = None

        # Entry
        self._nickname_entry: Entry = None

        # PhotoImages
        self._login_logo_img: PhotoImage = None
        self._start_btn_img: PhotoImage = None
        self._game_logo_img: PhotoImage = None
        self._remote_player_icon: PhotoImage = None
        self._local_player_icon: PhotoImage = None
        self._deck: PhotoImage = None
        self._discard_pile_img: PhotoImage = None
        self._trash_can_img: PhotoImage = None
        self._card_back_img: PhotoImage = None

        # Labels
        self._login_logo_label: Label = None
        self._game_logo_label: Label = None
        self._round_label: Label = None
        self._players_label: list[Label] = []
        self._remote_player_icon_labels: list[Label] = []
        self._local_player_icon_label: Label = None
        self._turn_text_label: Label = None
        self._player_turn_label: Label = None
        self._trash_can_label: Label = None
        self._remote_player_card_labels: list[list[list[Label]]] = []
        # Button
        self._start_btn: Button = None
        self._deck_btn: Button = None
        self._discard_pile_btn: Button = None
        self._local_player_card_btn : list[list[Button]] = []

        self._init_login_frame()
        self._window.mainloop()

    def _init_login_frame(self):
        self._login_frame = Frame(self._window, bg=self._primary_color)
        self._login_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._window.update()

        # Logo
        img = Image.open("assets/others/logo.png") 
        img = img.resize((500, 633))
        self._login_logo_img = ImageTk.PhotoImage(img)
        self._login_logo_label = Label(self._login_frame, image=self._login_logo_img, bg=self._primary_color)
        self._login_logo_label.place(x=220, y=195)

        # Input field and button
        self._right_frame = Frame(self._login_frame, bg=self._primary_color)
        self._right_frame.place(x=868, y=412)

        self._nickname_entry = Entry(
            self._right_frame,
            font=("Helvetica", 16),
            width=20,
            justify="center",
            bd=0,
            bg=self._secondary_color,
            fg=self._side_color
        )
        self._nickname_entry.insert(0, "Nickname")
        self._nickname_entry.pack(pady=10, ipady=10)

        # Placeholder 
        self._nickname_entry.bind("<FocusIn>", lambda _ : self._clear_placeholder())
        self._nickname_entry.bind("<FocusOut>", lambda _ : self._restore_placeholder())

        # Load the rounded button image
        btn_img = Image.open("assets/buttons/start_btn.png").resize((240, 60), Image.Resampling.LANCZOS)
        self._start_btn_img = ImageTk.PhotoImage(btn_img)

        # Button with image and centered text
        self._start_btn = Button(
            self._right_frame,
            image=self._start_btn_img,
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
        self._start_btn.pack(pady=10)

    def _init_game_frame(self, _):
        # Destroy login
        if self._login_frame:
            self._login_frame.destroy()

        self._game_frame = Frame(self._window, bg=self._bg_color)
        self._game_frame.place(x=0, y=0, width=1440, height=1024)

        self._create_side_frame()

        self._create_game_main_frame()

        self._create_local_player_board()

    def _create_side_frame(self):
        self._side_frame = Frame(self._game_frame, height=1024, width=295, bg=self._side_color)
        self._side_frame.place(x=0, y=0)
        self._create_logo()
        self._create_round_label(0)
        self._create_players_label(3)
        self._create_player_turn_label(1)

    def _create_logo(self):
        self._game_logo_img = PhotoImage(file="assets/others/logo.png")
        self._game_logo_label = Label(self._side_frame, image=self._game_logo_img, bg=self._side_color)
        self._game_logo_label.place(x=26, y=54)

    def _create_round_label(self, round_number: int):
        self._round_label = Label(
            self._side_frame,
            text=f"Round {round_number}/9",
            bg=self._primary_color,
            fg="white",
            font=("Inter", 14, "bold"),
            padx=20,
            pady=10,
            width=20
        )
        self._round_label.place(x=0, y=439, width=295, height=33)
    
    def _create_players_label(self, n_players: int):
        for i in range(n_players):
            self._players_label.append(Label(
                self._side_frame,
                text=f"Player {i + 1}: 0 pts",
                bg=self._secondary_color,
                fg=self._bg_color,
                font=("Inter", 12, "bold"),
                padx=20,
                pady=5,
                width=20
            ))
            # Each label 50px below the previous one, starting at y=200 (example)
            self._players_label[i].place(x=0, y=486 + i * 40, width=295, height=33)
    
    def _create_player_turn_label(self, player_number: int):
        self._turn_text_label = Label(
            self._side_frame, 
            text="It's the turn of:", 
            font=("Inter", 12), 
            fg="white", 
            bg=self._side_color
        )
        self._turn_text_label.place(x=58, y=828)
        self._player_turn_label = Label(
            self._side_frame,
            text=f"Player {player_number}",
            bg=self._primary_color,
            fg=self._bg_color,
            font=("Inter", 14, "bold"),
            padx=20,
            pady=10,
            width=20
        )
        self._player_turn_label.place(x=0, y=853, width=295, height=33)

    def _create_game_main_frame(self):
        self._create_player_icons()   # Missing Nicknames
        self._create_deck_of_cards()
        self._create_discard_pile()
        self._create_remote_player_boards()

    def _create_player_icons(self):
        img = Image.open("assets/others/player.png") 
        img = img.resize((106, 139))
        self._remote_player_icon = ImageTk.PhotoImage(img)
        
        # Remote players
        self._remote_player_icon_labels.append(Label(self._game_frame, image=self._remote_player_icon, bg=self._bg_color))
        self._remote_player_icon_labels[0].place(x=323, y=70)

        self._remote_player_icon_labels.append(Label(self._game_frame, image=self._remote_player_icon, bg=self._bg_color))
        self._remote_player_icon_labels[1].place(x=1276, y=70)

        # Local player
        img = img.resize((138, 181))
        self._local_player_icon = ImageTk.PhotoImage(img)
        self._local_player_icon_label = Label(self._game_frame, image=self._local_player_icon, bg=self._bg_color)
        self._local_player_icon_label.place(x=1184, y=715)

    def _create_deck_of_cards(self):
        img = Image.open("assets/others/deck-of-cards.png") 
        img = img.resize((216, 234))
        self._deck = ImageTk.PhotoImage(img)
        self._deck_btn = Button(
            self._game_frame,
            image=self._deck,
            bd=0,
            bg=self._bg_color,
            activebackground=self._bg_color,
            highlightthickness=0,
            command=self._on_deck_click
        )
        self._deck_btn.place(x=436, y=391)

    def _create_discard_pile(self):
        img = Image.open("assets/others/discard-pile-default.png") 
        img = img.resize((135, 190))
        self._discard_pile_img = ImageTk.PhotoImage(img)
        self._discard_pile_btn = Button(
            self._game_frame,
            image=self._discard_pile_img,
            bd=0,
            bg=self._bg_color,
            activebackground=self._bg_color,
            highlightthickness=0,
            command=self._on_discard_click
        )
        self._discard_pile_btn.place(x=1092, y=422)

        img = Image.open("assets/others/trash-can.png") 
        img = img.resize((49, 51))
        self._trash_can_img = ImageTk.PhotoImage(img)
        self._trash_can_label = Label(self._game_frame, image=self._trash_can_img, bg=self._bg_color)
        self._trash_can_label.place(x=1230, y=480)

    def _create_remote_player_boards(self):
        # Frame for the first remote player (top left)
        self._remote_players_boards.append(Frame(
            self._game_frame,
            bg=self._bg_color,
            padx=0,
            pady=0,
            bd=0,
            highlightthickness=0
        ))
        self._remote_players_boards[0].place(x=450, y=50, width=310, height=310)
        
        # Frame for the second remote player (top right)
        self._remote_players_boards.append(Frame(
            self._game_frame,
            bg=self._bg_color,
            padx=0,
            pady=0,
            bd=0,
            highlightthickness=0
        ))
        self._remote_players_boards[1].place(x=950, y=50, width=310, height=310)
        
        # Add face-down cards for each remote board (images only)
        for i, remote_board in enumerate(self._remote_players_boards):
            self._add_remote_player_cards(remote_board, i)

    def _add_remote_player_cards(self, parent_frame, player_index, card_size=(90, 141)):
        img = Image.open("assets/cards/back.png")
        img = img.resize(card_size)
        # Use a different variable for each player
        setattr(self, f"remote_card_back_img_{player_index}", ImageTk.PhotoImage(img))
    
        # Create 2x3 grid of cards (images only)
        self._remote_player_card_labels.append([])
        for row in range(2):
            self._remote_player_card_labels[player_index].append([])
            for col in range(3):
                self._remote_player_card_labels[player_index][row].append(Label(
                    parent_frame,
                    image=getattr(self, f"remote_card_back_img_{player_index}"),
                    bg=self._bg_color
                ))
                self._remote_player_card_labels[player_index][row][col].grid(row=row, column=col, padx=5, pady=5)

    def _clear_placeholder(self):
        if self._nickname_entry.get() == "Nickname":
            self._nickname_entry.delete(0, END)
            self._nickname_entry.config(fg="black")

    def _restore_placeholder(self):
        if self._nickname_entry.get() == "":
            self._nickname_entry.insert(0, "Nickname")
            self._nickname_entry.config(fg="#A9A9A9")

    def _validate_and_start_game(self):
        nickname = self._nickname_entry.get().strip()
        if not nickname or nickname == "Nickname":
            messagebox.showerror("Error", "Please enter a valid nickname.")
            return
        # Simulate server confirmation
        self._init_game_frame(nickname)

    def _create_local_player_board(self):
        # Main frame for local player board
        self._local_player_board = Frame(
            self._game_frame,
            bg=self._bg_color,
            padx=0,
            pady=0,
            bd=0,
            highlightthickness=0
        )
        self._local_player_board.place(x=600, y=550, width=470, height=450)
        
        # Frame for cards
        self._local_player_cards_frame = Frame(
            self._local_player_board, 
            bg=self._bg_color,
            bd=0,
            highlightthickness=0
        )
        self._local_player_cards_frame.pack(expand=False)
        
        # Add face-down cards (back cards)
        self._add_back_cards(self._local_player_cards_frame)
        
    def _add_back_cards(self, parent_frame, card_size=(125, 196), clickable=True):
        img = Image.open("assets/cards/back.png")
        img = img.resize(card_size)
        self._card_back_img = ImageTk.PhotoImage(img)
        
        # Create 2x3 grid of cards
        for row in range(2):
            self._local_player_card_btn.append([])
            for col in range(3):
                self._local_player_card_btn[row].append(Button(
                    parent_frame,
                    image=self._card_back_img,
                    bg=self._bg_color,
                    bd=0,
                    highlightthickness=0,
                    activebackground=self._bg_color
                ))
                self._local_player_card_btn[row][col].grid(row=row, column=col, padx=10, pady=5)
                
                # Add click event only if cards are clickable
                if clickable:
                    card_index = row * 3 + col  # Calculate index based on position
                    self._local_player_card_btn[row][col].bind("<Button-1>", lambda _, idx=card_index: self._on_card_click(idx))
                
    def _on_card_click(self, card_index):
        print(f"Card {card_index+1} clicked")

    def _on_discard_click(self):
        print("discard pile clicked")

    def _on_deck_click(self):
        print("draw pile clicked!")