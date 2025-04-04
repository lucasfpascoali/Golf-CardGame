from tkinter import *

class PlayerInterface:
    def __init__(self):
        self.main_window = Tk()
        self.fill_main_window()
        self.main_window.mainloop()


    def fill_main_window(self):
        self.main_window.title("Golf")
        self.main_window.geometry("1440x1024")
        self.main_window.resizable(False, False)
        self.main_window.config(bg="#0F3F27")
        self.main_window.iconbitmap("../resources/logo-jogo.ico")