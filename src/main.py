import customtkinter as ctk
from src.ui.dashboard import Dashboard
from src.ui.cadastro import Cadastro
from src.ui.revisao import Revisao

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Revisão Espaçada")
        self.geometry("500x500")
        self.resizable(False, False)
        self.tela_atual = None
        self.mostrar_dashboard()

    def mostrar_dashboard(self):
        self._trocar_tela(
            Dashboard(
                self,
                on_revisar=self.mostrar_revisao,
                on_cadastrar=self.mostrar_cadastro,
            )
        )

    def mostrar_cadastro(self):
        self._trocar_tela(Cadastro(self, on_voltar=self.mostrar_dashboard))

    def mostrar_revisao(self):
        self._trocar_tela(Revisao(self, on_voltar=self.mostrar_dashboard))

    def _trocar_tela(self, nova_tela):
        if self.tela_atual:
            self.tela_atual.destroy()
        self.tela_atual = nova_tela
        self.tela_atual.pack(expand=True, fill="both", padx=20, pady=20)


if __name__ == "__main__":
    app = App()
    app.mainloop()
