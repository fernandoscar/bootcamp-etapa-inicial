import customtkinter as ctk
from datetime import date
import uuid  # Dois espaços antes do comentário corrigem o E261
from src.core.repositorio import adicionar_item

# --- CONFIGURAÇÃO DE CORES ---
BG = "#0d0b14"
BG_CARD = "#12101a"
BG_INPUT = "#1a1025"
COR_ROXA = "#7c3aed"
COR_TEXTO = "#e8d5ff"
COR_MUTED = "#9b7fc0"


class Cadastro(ctk.CTkFrame):
    """
    Tela de Cadastro de novos assuntos.
    Permite ao utilizador inserir matéria, assunto, anotações e semestre.
    """
    def __init__(self, master, on_voltar, **kwargs):
        super().__init__(master, fg_color=BG, corner_radius=0, **kwargs)
        self.on_voltar = on_voltar

        # Estado inicial da categoria
        self.categoria_var = ctk.StringVar(value="Semestre")

        self._build_ui()

    def _build_ui(self):
        # Container Centralizado para manter o design focado
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.place(relx=0.5, rely=0.5, anchor="center")

        # Títulos superiores
        ctk.CTkLabel(
            self.main_container, text="Novo Assunto",
            font=ctk.CTkFont(size=28, weight="bold"), text_color="white"
        ).pack(pady=(0, 5))

        ctk.CTkLabel(
            self.main_container, text="Adicione um tópico ao seu ciclo de revisão.",
            font=ctk.CTkFont(size=14), text_color=COR_MUTED
        ).pack(pady=(0, 30))

        # Card Principal (Fundo escuro arredondado)
        form = ctk.CTkFrame(
            self.main_container, fg_color=BG_CARD, corner_radius=20, width=420
        )
        form.pack(padx=20, pady=20)

        # Frame Interno para aplicar margens (padding)
        inner = ctk.CTkFrame(form, fg_color="transparent")
        inner.pack(padx=30, pady=30)

        self._build_form_fields(inner)

    def _build_form_fields(self, inner):
        # 1. Seleção de Categoria
        self._label(inner, "Categoria")
        self.seg_button = ctk.CTkSegmentedButton(
            inner, values=["Semestre", "Auto-Estudo"],
            variable=self.categoria_var, fg_color=BG_INPUT,
            selected_color=COR_ROXA, unselected_color=BG_INPUT,
            text_color="white", height=35
        )
        self.seg_button.pack(fill="x", pady=(0, 20))

        # 2. Matéria
        self._label(inner, "Matéria")
        self.entry_materia = self._input(inner, "Digite o nome da disciplina...")

        # 3. Assunto
        self._label(inner, "Assunto")
        self.entry_assunto = self._input(inner, "O que vai estudar?")

        # 4. Anotação
        self._label(inner, "Anotação (opcional)")
        self.txt_anotacao = ctk.CTkTextbox(
            inner, fg_color=BG_INPUT, border_color="#2d1b4e",
            height=80, width=340, corner_radius=10, text_color=COR_TEXTO
        )
        self.txt_anotacao.pack(pady=(0, 20))

        # 5. Botões e 6. Semestre
        self._build_actions(inner)

    def _build_actions(self, inner):
        # 5. Botões de Ação
        self.btn_salvar = ctk.CTkButton(
            inner, text="Salvar", font=ctk.CTkFont(weight="bold"),
            fg_color=COR_ROXA, hover_color="#6d28d9",
            height=45, corner_radius=12, command=self.salvar_dados
        )
        self.btn_salvar.pack(fill="x", pady=(0, 10))

        self.btn_voltar = ctk.CTkButton(
            inner, text="Voltar", fg_color="transparent",
            text_color=COR_MUTED, border_width=1, border_color="#2d1b4e",
            height=40, corner_radius=12, command=self.on_voltar
        )
        self.btn_voltar.pack(fill="x", pady=(0, 20))

        # 6. Semestre
        self._label(inner, "Semestre")
        valores_semestre = [f"{i}º semestre" for i in range(1, 9)]
        self.combo_semestre = ctk.CTkComboBox(
            inner, values=valores_semestre, fg_color=BG_INPUT,
            border_color="#2d1b4e", button_color=COR_ROXA,
            dropdown_fg_color=BG_INPUT, width=340
        )
        self.combo_semestre.pack(fill="x")
        self.combo_semestre.set("1º semestre")

    def _label(self, parent, txt):
        """Auxiliar para criar labels padronizados."""
        ctk.CTkLabel(
            parent, text=txt, font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COR_MUTED
        ).pack(anchor="w", pady=(0, 5))

    def _input(self, parent, placeholder):
        """Auxiliar para criar campos de entrada padronizados."""
        entry = ctk.CTkEntry(
            parent, placeholder_text=placeholder, fg_color=BG_INPUT,
            border_color="#2d1b4e", height=40, corner_radius=10,
            text_color=COR_TEXTO
        )
        entry.pack(fill="x", pady=(0, 20))
        return entry

    def salvar_dados(self):
        """Recolhe os dados, valida e guarda no repositório."""
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
            "status": "Pendente"
        }

        adicionar_item(novo_item)
        self.on_voltar()