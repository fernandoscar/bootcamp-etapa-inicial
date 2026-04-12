import customtkinter as ctk
from src.core.repositorio import carregar_dados
from src.core.agendador import classificar_itens


class Dashboard(ctk.CTkFrame):
    def __init__(self, master, on_revisar, on_cadastrar):
        super().__init__(master)
        self.on_revisar = on_revisar
        self.on_cadastrar = on_cadastrar

        self.label_titulo = ctk.CTkLabel(
            self, text="📚 Revisão Espaçada", font=ctk.CTkFont(size=24, weight="bold")
        )
        self.label_titulo.pack(pady=20)

        self.label_hoje = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=16))
        self.label_hoje.pack(pady=5)

        self.label_atrasados = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=16))
        self.label_atrasados.pack(pady=5)

        self.btn_revisar = ctk.CTkButton(
            self, text="Revisar Agora", command=self.on_revisar
        )
        self.btn_revisar.pack(pady=10)

        self.btn_cadastrar = ctk.CTkButton(
            self, text="Cadastrar Assunto", command=self.on_cadastrar
        )
        self.btn_cadastrar.pack(pady=10)

        self.atualizar()

    def atualizar(self):
        itens = carregar_dados()
        para_hoje, atrasados = classificar_itens(itens)
        self.label_hoje.configure(text=f"📅 Revisões para hoje: {len(para_hoje)}")
        self.label_atrasados.configure(text=f"⚠️ Atrasadas: {len(atrasados)}")
