from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

class GameInterface:
    def __init__(self, nickname):
        self.window = Tk()
        self.window.title(f"Golf - Jogador {nickname}")
        self.window.geometry("1440x1024")
        self.window.resizable(False, False)
        self.window.configure(bg="#0F3F27")

        # Aqui virá toda a lógica da interface do jogo
        label = Label(self.window, text=f"Bem-vindo, {nickname}!", fg="white", bg="#0F3F27", font=("Helvetica", 20))
        label.pack(pady=20)
        
        self.setup_ui()
        self.window.mainloop()

# Iniciar programa
if __name__ == "__main__":
    GameInterface()