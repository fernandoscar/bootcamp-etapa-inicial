import customtkinter as ctk
from datetime import date
import uuid
from src.core.repositorio import adicionar_item
from src.ui import theme


class Cadastro(ctk.CTkFrame):
    """Tela de Cadastro de novos assuntos."""

    def __init__(self, master, on_voltar, **kwargs):
        super().__init__(master, fg_color=theme.get("BG"), corner_radius=0, **kwargs)
        self.on_voltar = on_voltar
        self.categoria_var = ctk.StringVar(value="Semestre")
        self._build_ui()

    def _build_ui(self):
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            self.main_container, text="Novo Assunto",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=theme.get("COR_TEXTO"),
        ).pack(pady=(0, 4))

        ctk.CTkLabel(
            self.main_container,
            text="Adicione um tópico ao seu ciclo de revisão.",
            font=ctk.CTkFont(size=12), text_color=theme.get("COR_MUTED"),
        ).pack(pady=(0, 24))

        form = ctk.CTkFrame(
            self.main_container, fg_color=theme.get("BG_CARD"),
            corner_radius=16, width=420,
        )
        form.pack(padx=20, pady=10)

        inner = ctk.CTkFrame(form, fg_color="transparent")
        inner.pack(padx=28, pady=28)
        self._build_form_fields(inner)

    def _build_form_fields(self, inner):
        self._label(inner, "Categoria")
        self.seg_button = ctk.CTkSegmentedButton(
            inner, values=["Semestre", "Auto-Estudo"],
            variable=self.categoria_var,
            fg_color=theme.get("BG_INPUT"),
            selected_color=theme.get("COR_ROXA"),
            unselected_color=theme.get("BG_INPUT"),
            text_color="white", height=35,
        )
        self.seg_button.pack(fill="x", pady=(0, 16))

        self._label(inner, "Matéria")
        self.entry_materia = self._input(inner, "Digite o nome da disciplina...")

        self._label(inner, "Assunto")
        self.entry_assunto = self._input(inner, "O que vai estudar?")

        self._label(inner, "Anotação (opcional)")
        self.txt_anotacao = ctk.CTkTextbox(
            inner, fg_color=theme.get("BG_INPUT"),
            border_color=theme.get("BG_ATIVO"),
            height=80, width=340, corner_radius=10,
            text_color=theme.get("COR_TEXTO"),
        )
        self.txt_anotacao.pack(pady=(0, 16))

        self._label(inner, "Semestre")
        valores_semestre = [f"{i}º semestre" for i in range(1, 9)]
        self.combo_semestre = ctk.CTkComboBox(
            inner, values=valores_semestre,
            fg_color=theme.get("BG_INPUT"),
            border_color=theme.get("BG_ATIVO"),
            button_color=theme.get("COR_ROXA"),
            dropdown_fg_color=theme.get("BG_INPUT"),
            width=340,
        )
        self.combo_semestre.pack(fill="x", pady=(0, 20))
        self.combo_semestre.set("1º semestre")

        self.btn_salvar = ctk.CTkButton(
            inner, text="Salvar",
            font=ctk.CTkFont(weight="bold"),
            fg_color=theme.get("COR_ROXA"),
            hover_color=theme.get("COR_ROXA_HOVER"),
            height=42, corner_radius=10,
            command=self.salvar_dados,
        )
        self.btn_salvar.pack(fill="x", pady=(0, 8))

        self.btn_voltar = ctk.CTkButton(
            inner, text="Voltar",
            fg_color="transparent", text_color=theme.get("COR_MUTED"),
            border_width=1, border_color=theme.get("BG_ATIVO"),
            height=38, corner_radius=10,
            command=self.on_voltar,
        )
        self.btn_voltar.pack(fill="x")

    def _label(self, parent, txt):
        ctk.CTkLabel(
            parent, text=txt,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=theme.get("COR_MUTED"),
        ).pack(anchor="w", pady=(0, 4))

    def _input(self, parent, placeholder):
        entry = ctk.CTkEntry(
            parent, placeholder_text=placeholder,
            fg_color=theme.get("BG_INPUT"),
            border_color=theme.get("BG_ATIVO"),
            height=38, corner_radius=10,
            text_color=theme.get("COR_TEXTO"),
        )
        entry.pack(fill="x", pady=(0, 16))
        return entry

    def salvar_dados(self):
        materia = self.entry_materia.get().strip()
        assunto = self.entry_assunto.get().strip()
        anotacao = self.txt_anotacao.get("1.0", "end-1c").strip()
        categoria = self.categoria_var.get().lower()
        sem_str = self.combo_semestre.get()

        if not materia or not assunto:
            return

        novo_item = {
            "id": str(uuid.uuid4()),
            "materia": materia,
            "assunto": assunto,
            "anotacao": anotacao,
            "categoria": categoria,
            "semestre": int(sem_str[0]) if "semestre" in categoria else 0,
            "data_agendada": str(date.today()),
            "indice_intervalo": 0,
            "total_revisoes": 0,
            "status": "Pendente",
        }

        adicionar_item(novo_item)
        self.on_voltar()
