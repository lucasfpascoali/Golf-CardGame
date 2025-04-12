from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

# Simulação de comunicação com o servidor
def enviar_nickname_ao_servidor(nickname):
    print(f"Enviando '{nickname}' ao servidor...")
    return "OK" if nickname.strip().lower() != "erro" else "ERRO"

class LoginScreen:
    def __init__(self):
        self.window = Tk()
        self.window.title("Golf - Entrada")
        self.window.geometry("1080x768")
        self.window.resizable(False, False)
        self.window.configure(bg="#5CA35F")

        self.setup_ui()
        self.window.mainloop()

    def setup_ui(self):
        main_frame = Frame(self.window, bg="#5CA35F")
        main_frame.pack(expand=True)

        # Logo
        img = Image.open("assets/others/logo.png") 
        img = img.resize((470, 503))
        self.logo_img = ImageTk.PhotoImage(img)

        logo_label = Label(main_frame, image=self.logo_img, bg="#5CA35F")
        logo_label.grid(row=0, column=0, padx=50)

        # Campo de entrada e botão
        right_frame = Frame(main_frame, bg="#5CA35F")
        right_frame.grid(row=0, column=1, padx=20)

        self.nickname_entry = Entry(
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

        # Placeholder funcional
        self.nickname_entry.bind("<FocusIn>", self._clear_placeholder)
        self.nickname_entry.bind("<FocusOut>", self._restore_placeholder)

        # Load the rounded button image
        btn_img = Image.open("assets/buttons/start_btn.png")
        btn_img = btn_img.resize((240, 60), Image.Resampling.LANCZOS)

        self.start_btn_img = ImageTk.PhotoImage(btn_img)

        # Button with image and centered text
        start_btn = Button(
            right_frame,
            image=self.start_btn_img,
            text="START",
            compound="center",
            font=("Helvetica", 24, "bold"),
            fg="white",
            bd=0,
            bg="#5CA35F",              # Match window bg if image is transparent
            activebackground="#5CA35F",
            highlightthickness=0,
            command=self.validar_e_iniciar_jogo
        )
        start_btn.pack(pady=10)

    def validar_e_iniciar_jogo(self):
        nickname = self.nickname_entry.get().strip()
        if not nickname or nickname == "Nickname":
            messagebox.showerror("Erro", "Digite um nickname válido.")
            return

        resposta = enviar_nickname_ao_servidor(nickname)
        if resposta == "OK":
            self.window.destroy()  # Fecha a janela atual
            GameInterface(nickname)  # Abre a interface principal
        else:
            messagebox.showerror("Erro", "Erro ao conectar com o servidor.")

    def _clear_placeholder(self, event):
        if self.nickname_entry.get() == "Nickname":
            self.nickname_entry.delete(0, END)
            self.nickname_entry.config(fg="black")

    def _restore_placeholder(self, event):
        if self.nickname_entry.get() == "":
            self.nickname_entry.insert(0, "Nickname")
            self.nickname_entry.config(fg="#A9A9A9")

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

        self.window.mainloop()

# Iniciar programa
if __name__ == "__main__":
    LoginScreen()