import customtkinter as ctk
from src.ui.sidebar import Sidebar
from src.ui.dashboard import Dashboard
from src.ui.cadastro import Cadastro
from src.ui.revisao import Revisao
from src.ui.meus_assuntos import MeusAssuntos

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG_COLOR = "#0d0b14"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PipoStudy")
        self.configure(fg_color=BG_COLOR)
        try:
            self.state("zoomed")
        except Exception:  # Corrigido: E722 bare except
            self.attributes("-zoomed", True)
        self.minsize(900, 600)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(self, navegacao=self.navegar)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.conteudo = ctk.CTkFrame(self, fg_color=BG_COLOR)
        self.conteudo.grid(row=0, column=1, sticky="nsew")
        self.conteudo.grid_rowconfigure(0, weight=1)
        self.conteudo.grid_columnconfigure(0, weight=1)

        self.tela_atual = None
        self.navegar("dashboard")

    def navegar(self, tela: str):
        if self.tela_atual:
            self.tela_atual.destroy()

        if tela == "dashboard":
            self.tela_atual = Dashboard(
                self.conteudo,
                on_revisar=lambda: self.navegar("revisao"),
                on_cadastrar=lambda: self.navegar("cadastro"),
            )
        elif tela == "cadastro":
            self.tela_atual = Cadastro(
                self.conteudo, on_voltar=lambda: self.navegar("dashboard")
            )
        elif tela == "revisao":
            self.tela_atual = Revisao(
                self.conteudo, on_voltar=lambda: self.navegar("dashboard")
            )
        elif tela == "meus_assuntos":
            self.tela_atual = MeusAssuntos(
                self.conteudo,
                on_cadastrar=lambda: self.navegar("cadastro"),
                on_voltar=lambda: self.navegar("dashboard"),
            )

        self.sidebar.set_ativo(tela)
        self.tela_atual.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()
