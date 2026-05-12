import customtkinter as ctk
from src.core.repositorio import carregar_dados
from src.core.agendador import classificar_itens
from src.ui import theme


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, navegacao, on_toggle_tema=None):
        super().__init__(
            master, width=220, fg_color=theme.get("BG_SIDEBAR"), corner_radius=0
        )
        self.navegacao = navegacao
        self.on_toggle_tema = on_toggle_tema
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.botoes = {}

        self._criar_logo()
        self._criar_avatar()
        self._criar_menu()
        self._criar_rodape()
        self.atualizar_badge()

    def _criar_logo(self):
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(pady=(20, 16), padx=16, anchor="w")

        icon_box = ctk.CTkFrame(
            logo_frame, fg_color=theme.get("COR_ROXA"),
            corner_radius=10, width=36, height=36,
        )
        icon_box.pack(side="left", padx=(0, 10))
        icon_box.pack_propagate(False)
        ctk.CTkLabel(
            icon_box, text="⬡", font=ctk.CTkFont(size=18),
            text_color="white",
        ).pack(expand=True)

        info = ctk.CTkFrame(logo_frame, fg_color="transparent")
        info.pack(side="left")
        ctk.CTkLabel(
            info, text="PipoStudy",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=theme.get("COR_TEXTO"),
        ).pack(anchor="w")
        ctk.CTkLabel(
            info, text="SPACED REPETITION",
            font=ctk.CTkFont(size=8), text_color=theme.get("COR_MUTED"),
        ).pack(anchor="w")

    def _criar_avatar(self):
        avatar_row = ctk.CTkFrame(
            self, fg_color=theme.get("BG_ITEM"), corner_radius=10,
        )
        avatar_row.pack(fill="x", padx=14, pady=(0, 16))

        avatar_circle = ctk.CTkFrame(
            avatar_row, fg_color=theme.get("ICON_PURPLE_BG"),
            corner_radius=16, width=32, height=32,
        )
        avatar_circle.pack(side="left", padx=(10, 8), pady=8)
        avatar_circle.pack_propagate(False)
        ctk.CTkLabel(
            avatar_circle, text="E",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=theme.get("COR_ROXA"),
        ).pack(expand=True)

        info = ctk.CTkFrame(avatar_row, fg_color="transparent")
        info.pack(side="left", pady=8)
        ctk.CTkLabel(
            info, text="Estudante",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=theme.get("COR_TEXTO"),
        ).pack(anchor="w")
        ctk.CTkLabel(
            info, text="Engenharia de Software",
            font=ctk.CTkFont(size=9), text_color=theme.get("COR_MUTED"),
        ).pack(anchor="w")

    def _criar_menu(self):
        ctk.CTkLabel(
            self, text="PRINCIPAL",
            font=ctk.CTkFont(size=9),
            text_color=theme.get("COR_MUTED"),
        ).pack(anchor="w", padx=20, pady=(4, 4))

        self._criar_item("dashboard", "⊞", "Início")
        self._criar_item("meus_assuntos", "☰", "Meus Assuntos")
        self._criar_item("revisao", "↻", "Revisar")

        ctk.CTkLabel(
            self, text="OUTROS",
            font=ctk.CTkFont(size=9),
            text_color=theme.get("COR_MUTED"),
        ).pack(anchor="w", padx=20, pady=(12, 4))

        self._criar_item("cadastro", "+", "Cadastrar")

    def _criar_rodape(self):
        # Toggle de tema
        toggle_f = ctk.CTkFrame(
            self, fg_color=theme.get("BG_ITEM"), corner_radius=10,
            cursor="hand2",
        )
        toggle_f.pack(side="bottom", fill="x", padx=14, pady=(0, 14))

        icone = "☀" if theme.tema_atual() == "dark" else "☾"
        label = "Modo claro" if theme.tema_atual() == "light" else "Modo escuro"

        ctk.CTkLabel(
            toggle_f, text=icone, font=ctk.CTkFont(size=14),
            text_color=theme.get("COR_MUTED"),
        ).pack(side="left", padx=(12, 6), pady=8)

        ctk.CTkLabel(
            toggle_f, text=label,
            font=ctk.CTkFont(size=11),
            text_color=theme.get("COR_MUTED"),
        ).pack(side="left", pady=8)

        if self.on_toggle_tema:
            for w in [toggle_f] + toggle_f.winfo_children():
                w.bind("<Button-1>", lambda e: self.on_toggle_tema())

        # Rodapé com total
        self.rodape = ctk.CTkFrame(
            self, fg_color=theme.get("BG_ITEM"), corner_radius=10,
        )
        self.rodape.pack(side="bottom", fill="x", padx=14, pady=(0, 6))

        ctk.CTkLabel(
            self.rodape, text="◉", font=ctk.CTkFont(size=12),
            text_color=theme.get("COR_MUTED"),
        ).pack(side="left", padx=(12, 6), pady=8)

        ctk.CTkLabel(
            self.rodape, text="Total de assuntos",
            font=ctk.CTkFont(size=11), text_color=theme.get("COR_MUTED"),
        ).pack(side="left", pady=8)

        self.label_total = ctk.CTkLabel(
            self.rodape, text="0",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=theme.get("COR_TEXTO"),
        )
        self.label_total.pack(side="right", padx=12, pady=8)

    def _criar_item(self, tela: str, icone: str, label: str):
        frame = ctk.CTkFrame(
            self, fg_color="transparent", corner_radius=10, cursor="hand2",
        )
        frame.pack(fill="x", padx=12, pady=1)

        icone_label = ctk.CTkLabel(
            frame, text=icone, font=ctk.CTkFont(size=14),
            text_color=theme.get("COR_MUTED"), width=24,
        )
        icone_label.pack(side="left", padx=(10, 8), pady=8)

        texto_label = ctk.CTkLabel(
            frame, text=label, font=ctk.CTkFont(size=12),
            text_color=theme.get("COR_MUTED"),
        )
        texto_label.pack(side="left", pady=8)

        if tela == "revisao":
            self.badge = ctk.CTkLabel(
                frame, text="0",
                font=ctk.CTkFont(size=9, weight="bold"),
                text_color="white", fg_color="#ef4444",
                corner_radius=8, width=22, height=18,
            )
            self.badge.pack(side="right", padx=10)

        def on_click(e=None):
            self.navegacao(tela)

        for widget in [frame, icone_label, texto_label]:
            widget.bind("<Button-1>", on_click)

        self.botoes[tela] = (frame, icone_label, texto_label)

    def set_ativo(self, tela: str):
        for nome, (frame, icone, texto) in self.botoes.items():
            if nome == tela:
                frame.configure(fg_color=theme.get("COR_ROXA"))
                icone.configure(text_color="white")
                texto.configure(
                    text_color="white",
                    font=ctk.CTkFont(size=12, weight="bold"),
                )
            else:
                frame.configure(fg_color="transparent")
                icone.configure(text_color=theme.get("COR_MUTED"))
                texto.configure(
                    text_color=theme.get("COR_MUTED"),
                    font=ctk.CTkFont(size=12),
                )
        self.atualizar_badge()

    def atualizar_badge(self):
        itens = carregar_dados()
        para_hoje, atrasados = classificar_itens(itens)
        total_pendentes = len(para_hoje) + len(atrasados)
        total = len(itens)
        self.label_total.configure(text=str(total))
        if hasattr(self, "badge"):
            self.badge.configure(text=str(total_pendentes))
