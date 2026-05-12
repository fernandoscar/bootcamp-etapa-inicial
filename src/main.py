import sys
import customtkinter as ctk
from src.ui.sidebar import Sidebar
from src.ui.dashboard import Dashboard
from src.ui.cadastro import Cadastro
from src.ui.revisao import Revisao
from src.ui.meus_assuntos import MeusAssuntos
from src.ui import theme

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PipoStudy")
        self.configure(fg_color=theme.get("BG"))
        self._maximizar_janela()
        self.minsize(1000, 650)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(
            self, navegacao=self.navegar, on_toggle_tema=self.toggle_tema
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.conteudo = ctk.CTkFrame(self, fg_color=theme.get("BG"))
        self.conteudo.grid(row=0, column=1, sticky="nsew")
        self.conteudo.grid_rowconfigure(0, weight=1)
        self.conteudo.grid_columnconfigure(0, weight=1)

        self.tela_atual = None
        self.tela_nome = "dashboard"
        self.navegar("dashboard")

    def _maximizar_janela(self):
        """Maximiza a janela de forma compatível com cada OS."""
        plataforma = sys.platform
        if plataforma == "win32":
            # Windows: state("zoomed") funciona nativamente
            self.state("zoomed")
        elif plataforma == "darwin":
            # macOS: fullscreen via atributo
            self.attributes("-fullscreen", False)
            self.after(100, lambda: self.state("zoomed"))
        else:
            # Linux: -zoomed é o equivalente no X11
            try:
                self.attributes("-zoomed", True)
            except Exception:
                # Fallback: define tamanho grande manualmente
                self.geometry("1200x800")

    def navegar(self, tela: str):
        if self.tela_atual:
            self.tela_atual.destroy()

        self.tela_nome = tela

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

    def toggle_tema(self):
        novo = "dark" if theme.tema_atual() == "light" else "light"
        theme.set_tema(novo)
        modo = "dark" if novo == "dark" else "light"
        ctk.set_appearance_mode(modo)
        self.configure(fg_color=theme.get("BG"))
        self.conteudo.configure(fg_color=theme.get("BG"))
        self.sidebar.destroy()
        self.sidebar = Sidebar(
            self, navegacao=self.navegar, on_toggle_tema=self.toggle_tema
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.navegar(self.tela_nome)


if __name__ == "__main__":
    app = App()
    app.mainloop()
