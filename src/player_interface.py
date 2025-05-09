from tkinter import messagebox, Tk, PhotoImage, Label, Frame, Button, END, simpledialog
from PIL import Image, ImageTk
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from dog.start_status import StartStatus
from core.match import Match
from core.board import Board

class PlayerInterface(DogPlayerInterface):
    def __init__(self):
        # Problem domain
        self._match: Match = None

        # Colors
        self._bg_color = "#0F3F27"          # dark green
        self._primary_color = "#5CA35F"     # bright green
        self._side_color = "#B7C3AD"        # very light grayish green
        self._secondary_color = "#DBE0D2"   # ice white

        # Window
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
        self._remote_players_board_frames : list[Frame] = [None, None]
        self._local_player_board: Frame = None
        self._local_player_cards_frame: Frame = None

        # PhotoImages
        self._login_logo_img: PhotoImage = None
        self._start_btn_img: PhotoImage = None
        self._game_logo_img: PhotoImage = None
        self._remote_player_icon: PhotoImage = None
        self._local_player_icon: PhotoImage = None
        self._deck_img: PhotoImage = None
        self._discard_pile_img: PhotoImage = None
        self._trash_can_img: PhotoImage = None
        self._local_player_card_back_img: PhotoImage = None
        self._remote_player_card_back_img: PhotoImage = None
        self._local_player_board_card_imgs: list[list[PhotoImage]] = [
            [None, None, None],
            [None, None, None]
        ]
        self._remote_players_board_card_imgs: list[list[list[PhotoImage]]] = [
            [
                [None, None, None],
                [None, None, None]
            ],
            [
                [None, None, None],
                [None, None, None]
            ]
        ]
        
        # Labels
        self._login_logo_label: Label = None
        self._game_logo_label: Label = None
        self._round_label: Label = None
        self._players_label: list[Label] = [None, None, None]
        self._remote_player_icon_labels_text: list[Label] = [None, None]
        self._remote_player_icon_labels: list[Label] = [None, None]
        self._local_player_icon_label_text: Label = None
        self._local_player_icon_label: Label = None
        self._turn_text_label: Label = None
        self._player_turn_label: Label = None
        self._trash_can_label: Label = None
        self._remote_player_card_labels: list[list[list[Label]]] = [
            [
                [None, None, None],
                [None, None, None]
            ],
            [
                [None, None, None],
                [None, None, None]
            ]
        ]
        
        # Button
        self._start_btn: Button = None
        self._deck_btn: Button = None
        self._discard_pile_btn: Button = None
        self._local_player_card_btn : list[list[Button]] = [
            [None, None, None],
            [None, None, None]
        ]

        self._load_default_images()

        self._init_login_frame() # Aqui é init login frame, mas só pra testes botei esse

        nickname = simpledialog.askstring(title="Nickname", prompt="Enter your nickname:")

        self.dog_server_interface = DogActor()

        message = self.dog_server_interface.initialize(nickname, self)
        messagebox.showinfo(message=message)
        if message != "Conectado a Dog Server":
            self._window.quit()
            return

        self._window.mainloop()

    ###################################################################################################
    ### GUI + Game State Control                                                                    ###
    ###################################################################################################

    def _update_gui(self):
        if self._match == None or not self._match.is_running():
            return

        self._set_local_player_board()
        self._set_local_player_icon_name()
        self._set_remote_players_boards()
        self._set_remote_players_icon_name()
        self._set_discard_pile_card() 
        self._set_round_label()
        self._set_players_label()
        self._set_player_turn_label()


    ###################################################################################################
    ### Load default images                                                                         ###
    ###################################################################################################

    def _load_default_images(self) -> None:
        self._load_card_back_img()
        self._load_player_icon_img()
        self._load_deck_and_discard_pile_img()

    def _load_card_back_img(self) -> None:
        img = Image.open("assets/cards/back.png")
        img_local = img.resize((125, 196))
        img_remote = img.resize((90, 141))
        self._local_player_card_back_img: PhotoImage = ImageTk.PhotoImage(img_local)
        self._remote_player_card_back_img: PhotoImage = ImageTk.PhotoImage(img_remote)
    
    def _load_player_icon_img(self) -> None:
        img = Image.open("assets/others/player.png") 
        img = img.resize((106, 139))
        self._remote_player_icon = ImageTk.PhotoImage(img)
        img = img.resize((138, 181))
        self._local_player_icon = ImageTk.PhotoImage(img)

    def _load_deck_and_discard_pile_img(self) -> None:
        img = Image.open("assets/others/deck-of-cards.png") 
        img = img.resize((216, 234))
        self._deck_img = ImageTk.PhotoImage(img)

        img = Image.open("assets/others/trash-can.png") 
        img = img.resize((49, 51))
        self._trash_can_img = ImageTk.PhotoImage(img)

    ##################################################################################################
    ### Login Frame                                                                                ###
    ##################################################################################################

    def _init_login_frame(self) -> None:
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
            command=self._start_match
        )
        self._start_btn.pack(pady=10)

    ##################################################################################################
    ### Game Frame                                                                                 ###
    ##################################################################################################

    def _init_game_frame(self) -> None:
        # Destroy login
        if self._login_frame:
            self._login_frame.destroy()

        self._game_frame = Frame(self._window, bg=self._bg_color)
        self._game_frame.place(x=0, y=0, width=1440, height=1024)

        self._create_side_frame()

        self._create_game_main_frame()

        self._create_local_player_board()

    def _create_game_main_frame(self) -> None:
        self._create_player_icons()
        self._create_deck_of_cards()
        self._create_discard_pile()
        self._create_local_player_board()
        self._create_remote_player_boards()

    ##################################################################################################
    ### SCOREBOARD (Side Frame)                                                                    ###
    ##################################################################################################

    def _create_side_frame(self) -> None:
        self._side_frame = Frame(self._game_frame, height=1024, width=295, bg=self._side_color)
        self._side_frame.place(x=0, y=0)
        self._create_logo()
        self._create_round_label()
        self._create_players_label()
        self._create_player_turn_label()

    def _create_logo(self) -> None:
        self._game_logo_img = PhotoImage(file="assets/others/logo.png")
        self._game_logo_label = Label(self._side_frame, image=self._game_logo_img, bg=self._side_color)
        self._game_logo_label.place(x=26, y=54)

    def _create_round_label(self) -> None:
        self._round_label = Label(
            self._side_frame,
            text=f"Round 0/9",
            bg=self._primary_color,
            fg="white",
            font=("Inter", 14, "bold"),
            padx=20,
            pady=10,
            width=20
        )
        self._round_label.place(x=0, y=439, width=295, height=33)
    
    def _create_players_label(self) -> None:
        for i in range(3):
            self._players_label[i] = Label(
                self._side_frame,
                text=f"Player {i + 1}: 0 pts",
                bg=self._secondary_color,
                fg=self._bg_color,
                font=("Inter", 12, "bold"),
                padx=20,
                pady=5,
                width=20
            )
            # Each label 50px below the previous one, starting at y=200 (example)
            self._players_label[i].place(x=0, y=486 + i * 40, width=295, height=33)

    def _create_player_turn_label(self) -> None:
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
            text="Player 1",
            bg=self._primary_color,
            fg=self._bg_color,
            font=("Inter", 14, "bold"),
            padx=20,
            pady=10,
            width=20
        )
        self._player_turn_label.place(x=0, y=853, width=295, height=33)

    def _set_round_label(self) -> None:
        if self._match == None or not self._match.is_running():
            return
        
        round_number = self._match.get_current_round().get_round_number()
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
        
    def _set_players_label(self) -> None:
        if self._match == None or not self._match.is_running():
            return

        players = self._match.get_players()
        for i in range(len(players)):
            self._players_label[i] = Label(
                self._side_frame,
                text=f"{players[i].get_nickname()}: {players[i].get_score()} pts",
                bg=self._secondary_color,
                fg=self._bg_color,
                font=("Inter", 12, "bold"),
                padx=20,
                pady=5,
                width=20
            )
            # Each label 50px below the previous one, starting at y=200 (example)
            self._players_label[i].place(x=0, y=486 + i * 40, width=295, height=33)

    def _set_player_turn_label(self) -> None:
        if self._match == None or not self._match.is_running():
            return
        
        current_player_name = self._match.get_current_player().get_nickname()
        self._player_turn_label = Label(
            self._side_frame,
            text=f"{current_player_name}",
            bg=self._primary_color,
            fg=self._bg_color,
            font=("Inter", 14, "bold"),
            padx=20,
            pady=10,
            width=20
        )
        self._player_turn_label.place(x=0, y=853, width=295, height=33)
        
    ##################################################################################################
    ### PLAYER ICONS                                                                               ###
    ##################################################################################################

    def _create_player_icons(self) -> None:
        # Remote players
        positions = [(323, 70), (1276, 70)]
        for i in range(2):
            x, y = positions[i]
            self._create_remote_player_icon(i, x, y)

        # Local player
        self._local_player_icon_label = Label(
            self._game_frame,
            image=self._local_player_icon,
            bg=self._bg_color,
            anchor="center",
            justify="center", 
        )
        self._local_player_icon_label.place(x=1184, y=715)

    def _create_remote_player_icon(self, player_index: int, x: int, y: int) -> None:
        self._remote_player_icon_labels[player_index] = Label(self._game_frame, image=self._remote_player_icon, bg=self._bg_color)
        self._remote_player_icon_labels[player_index].place(x=x, y=y)
    
    def _set_remote_players_icon_name(self) -> None:
        if self._match == None or not self._match.is_running:
            return
        
        remote_players = self._match.get_remote_players()
        for i in range(2):
            self._remote_player_icon_labels_text[i] = Label(
                self._remote_player_icon_labels[i],
                text=remote_players[i].get_nickname(),
                bg=self._primary_color,
                fg="white",
                font=("Inter", 10, "bold"),
                justify="center",
                anchor="center",
            )
            self._remote_player_icon_labels_text[i].place(x=0, y=110, width=110, height=30)

    def _set_local_player_icon_name(self) -> None:
        if self._match == None or not self._match.is_running:
            return

        local_player_nickname = self._match.get_local_player().get_nickname() 
        self._local_player_icon_label_text = Label(
            self._local_player_icon_label,
            text=local_player_nickname,
            bg=self._primary_color,
            fg="white",
            font=("Inter", 12, "bold"),
            justify="center",
            anchor="center",
        )
        self._local_player_icon_label_text.place(x=0, y=145, width=160, height=38)

    ##################################################################################################
    ### DECK OF CARDS                                                                              ###
    ##################################################################################################

    def _create_deck_of_cards(self) -> None:
        self._deck_btn = Button(
            self._game_frame,
            image=self._deck_img,
            bd=0,
            bg=self._bg_color,
            activebackground=self._bg_color,
            highlightthickness=0,
            command=self._on_deck_click
        )
        self._deck_btn.place(x=436, y=391)

    ##################################################################################################
    ### DISCARD PILE                                                                               ###
    ##################################################################################################
    
    def _create_discard_pile(self) -> None:
        self._trash_can_label = Label(self._game_frame, image=self._trash_can_img, bg=self._bg_color)
        self._trash_can_label.place(x=1230, y=480)
        self._set_discard_pile_img(self._get_default_discard_pile())

    def _get_default_discard_pile(self) -> str:
        return "assets/others/discard-pile-default.png"

    def _set_discard_pile_card(self) -> None:
        if self._match == None or not self._match.is_running():
            return

        card_id = self._match.get_current_round().get_discard_pile().get_id()
        self._set_discard_pile_img(f"assets/cards/{card_id}.png")

    def _set_discard_pile_img(self, img_path: str) -> None:
        img = Image.open(img_path) 
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

    ##################################################################################################
    ### LOCAL PLAYER BOARD                                                                         ###
    ##################################################################################################

    def _create_local_player_board(self) -> None:
        self._create_local_player_board_frames()
        self._load_default_local_player_board()

    def _create_local_player_board_frames(self) -> None:
        # Frame for local player board
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

    def _load_default_local_player_board(self) -> None:
        for row in range(2):
            for col in range(3):
                self._local_player_card_btn[row][col] = Button(
                    self._local_player_cards_frame,
                    image=self._local_player_card_back_img,
                    bg=self._bg_color,
                    bd=0,
                    highlightthickness=0,
                    activebackground=self._bg_color,
                    command=lambda idx="": self._on_card_click(idx)
                )
                self._local_player_card_btn[row][col].grid(row=row, column=col, padx=10, pady=5)
                
    def _set_local_player_board(self) -> None:
        if self._match == None or not self._match.is_running():
            return

        local_player_board = self._match.get_local_player_board()        
        for row in range(2):
            for col in range(3):
                card = local_player_board.get_card_in_position(row, col)
                card_id = card.get_id()
                
                img = Image.open(f"assets/cards/{card_id}.png")
                img = img.resize((125, 196))
                img = ImageTk.PhotoImage(img)
                if not card.is_face_up():
                    img = self._local_player_card_back_img
                
                self._local_player_board_card_imgs[row][col] = img
                self._local_player_card_btn[row][col] = Button(
                    self._local_player_cards_frame,
                    image=self._local_player_board_card_imgs[row][col],
                    bg=self._bg_color,
                    bd=0,
                    highlightthickness=0,
                    activebackground=self._bg_color,
                    command=lambda c=card_id: self._on_card_click(c)
                )
                self._local_player_card_btn[row][col].grid(row=row, column=col, padx=10, pady=5)

    ###################################################################################################
    ### REMOTE PLAYER BOARDS                                                                        ###
    ###################################################################################################

    def _create_remote_player_boards(self) -> None:
        positions = [(450, 50), (950, 50)]
        for i in range(2):
            x, y = positions[i]
            self._create_remote_player_boards_frame(i, x, y)
            self._load_default_remote_player_board(i)

    def _create_remote_player_boards_frame(self, player_index: int, x: int, y: int) -> None:
        self._remote_players_board_frames[player_index] = Frame(
            self._game_frame,
            bg=self._bg_color,
            padx=0,
            pady=0,
            bd=0,
            highlightthickness=0
        )
        self._remote_players_board_frames[player_index].place(x=x, y=y, width=310, height=310)

    def _load_default_remote_player_board(self, player_index: int) -> None:
        for row in range(2):
            for col in range(3):
                self._remote_player_card_labels[player_index][row][col] = Label(
                    self._remote_players_board_frames[player_index],
                    image=self._remote_player_card_back_img,
                    bg=self._bg_color
                )
                self._remote_player_card_labels[player_index][row][col].grid(row=row, column=col, padx=5, pady=5)

    def _set_remote_players_boards(self) -> None:
        if self._match == None or not self._match.is_running():
            return
        
        remote_players_boards = self._match.get_remote_players_boards()
        for i in range(2):
            self._set_remote_player_cards(i, remote_players_boards[i])

    def _set_remote_player_cards(self, player_index, remote_player_board: Board) -> None:        
        for row in range(2):
            for col in range(3):
                card = remote_player_board.get_card_in_position(row, col)
                card_id = card.get_id()
                img = Image.open(f"assets/cards/{card_id}.png")
                img = img.resize((90, 141))
                img = ImageTk.PhotoImage(img)
                if not card.is_face_up():
                    img = self._remote_player_card_back_img

                self._remote_players_board_card_imgs[player_index][row][col] = img
                self._remote_player_card_labels[player_index][row].append(Label(
                    self._remote_players_board_frames[player_index],
                    image=self._remote_players_board_card_imgs[player_index][row][col],
                    bg=self._bg_color
                ))
                self._remote_player_card_labels[player_index][row][col].grid(row=row, column=col, padx=5, pady=5)

    ####################################################################################################
    ### DOG Actions                                                                                 ###
    ####################################################################################################

    def _start_match(self) -> None:
        start_status = self.dog_server_interface.start_match(3)
        message = start_status.get_message()
        messagebox.showinfo(message=message)

        if start_status.get_code() == '2':
            self._match = Match(start_status.get_players(), start_status.get_local_id())
            self._match.start_match()
            a_move = self._match.get_move_dict()
            a_move["match_status"] = "next"
            self.dog_server_interface.send_move(a_move)
            self._init_game_frame()
            self._update_gui()

    def receive_start(self, start_status: StartStatus) -> None:
        if start_status.get_code() != '2':
            messagebox.showerror("Failed to start match")
            self._window.quit()
            return
        
        self._match = Match(start_status.get_players(), start_status.get_local_id())
        self._match.set_as_running()
        self._init_game_frame()

    def receive_move(self, a_move: dict) -> None:
        if self._match == None or not self._match.is_running():
            return
        
        print(a_move)
        # self._match.load_match_from_move(a_move)
        # self._update_gui()

    def _on_card_click(self, card_id: str) -> None:
        if self._match == None:
            return
        
        print(f"Card {card_id} clicked")

    def _on_discard_click(self) -> None:
        if self._match == None:
            return

        print("discard pile clicked")

    def _on_deck_click(self) -> None:
        if self._match == None:
            return

        print("draw pile clicked!")