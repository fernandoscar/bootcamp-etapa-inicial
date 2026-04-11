import customtkinter as ctk
from src.core.repositorio import adicionar_item


class Cadastro(ctk.CTkFrame):
    def __init__(self, master, on_voltar):
        super().__init__(master)
        self.on_voltar = on_voltar

        self.label_titulo = ctk.CTkLabel(
            self, text="➕ Cadastrar Assunto", font=ctk.CTkFont(size=24, weight="bold")
        )
        self.label_titulo.pack(pady=20)

        self.label_materia = ctk.CTkLabel(self, text="Matéria:")
        self.label_materia.pack()
        self.entry_materia = ctk.CTkEntry(self, width=300)
        self.entry_materia.pack(pady=5)

        self.label_assunto = ctk.CTkLabel(self, text="Assunto:")
        self.label_assunto.pack()
        self.entry_assunto = ctk.CTkEntry(self, width=300)
        self.entry_assunto.pack(pady=5)

        self.label_feedback = ctk.CTkLabel(self, text="")
        self.label_feedback.pack(pady=5)

        self.btn_salvar = ctk.CTkButton(
            self, text="Salvar", command=self.salvar
        )
        self.btn_salvar.pack(pady=10)

        self.btn_voltar = ctk.CTkButton(
            self, text="Voltar", fg_color="gray", command=self.on_voltar
        )
        self.btn_voltar.pack(pady=5)

    def salvar(self):
        materia = self.entry_materia.get().strip()
        assunto = self.entry_assunto.get().strip()

        if not materia or not assunto:
            self.label_feedback.configure(
                text="⚠️ Preencha todos os campos!", text_color="red"
            )
            return

        adicionar_item(materia, assunto)
        self.entry_materia.delete(0, "end")
        self.entry_assunto.delete(0, "end")
        self.label_feedback.configure(
            text="✅ Assunto cadastrado!", text_color="green"
        )