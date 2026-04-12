import customtkinter as ctk
from src.core.repositorio import carregar_dados, atualizar_item
from src.core.agendador import calcular_proxima_data, classificar_itens


class Revisao(ctk.CTkFrame):
    def __init__(self, master, on_voltar):
        super().__init__(master)
        self.on_voltar = on_voltar
        self.fila = []
        self.indice_atual = 0

        self.label_titulo = ctk.CTkLabel(
            self, text="🎯 Modo Revisão", font=ctk.CTkFont(size=24, weight="bold")
        )
        self.label_titulo.pack(pady=20)

        self.label_materia = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14))
        self.label_materia.pack()

        self.label_assunto = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.label_assunto.pack(pady=20)

        self.label_progresso = ctk.CTkLabel(self, text="")
        self.label_progresso.pack()

        self.btn_claro = ctk.CTkButton(
            self,
            text="✅ Conexões Claras",
            fg_color="green",
            command=lambda: self.responder("claro"),
        )
        self.btn_claro.pack(pady=5)

        self.btn_clareando = ctk.CTkButton(
            self,
            text="🟡 Conexões Clareando",
            fg_color="orange",
            command=lambda: self.responder("clareando"),
        )
        self.btn_clareando.pack(pady=5)

        self.btn_ineficaz = ctk.CTkButton(
            self,
            text="❌ Ineficaz",
            fg_color="red",
            command=lambda: self.responder("ineficaz"),
        )
        self.btn_ineficaz.pack(pady=5)

        self.btn_voltar = ctk.CTkButton(
            self, text="Voltar", fg_color="gray", command=self.on_voltar
        )
        self.btn_voltar.pack(pady=20)

        self.carregar_fila()

    def carregar_fila(self):
        itens = carregar_dados()
        para_hoje, atrasados = classificar_itens(itens)
        self.fila = atrasados + para_hoje
        self.indice_atual = 0
        self.mostrar_atual()

    def mostrar_atual(self):
        if self.indice_atual >= len(self.fila):
            self.label_materia.configure(text="")
            self.label_assunto.configure(text="🎉 Nenhuma revisão pendente!")
            self.label_progresso.configure(text="")
            for btn in [self.btn_claro, self.btn_clareando, self.btn_ineficaz]:
                btn.configure(state="disabled")
            return

        item = self.fila[self.indice_atual]
        self.label_materia.configure(text=f"Matéria: {item['materia']}")
        self.label_assunto.configure(text=item["assunto"])
        self.label_progresso.configure(
            text=f"{self.indice_atual + 1} de {len(self.fila)}"
        )

    def responder(self, feedback: str):
        item = self.fila[self.indice_atual]
        nova_data, novo_indice = calcular_proxima_data(
            item["indice_intervalo"], feedback
        )
        status = "Precisa Reestudar" if feedback == "ineficaz" else "Revisado"
        atualizar_item(item["id"], str(nova_data), novo_indice, status)
        self.indice_atual += 1
        self.mostrar_atual()
