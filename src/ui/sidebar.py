import customtkinter as ctk
from src.core.repositorio import carregar_dados
from src.core.agendador import classificar_itens

BG_SIDEBAR = "#0d0b14"
BG_ITEM = "#1a1025"
BG_ATIVO = "#2d1b4e"
COR_ROXA = "#7c3aed"
COR_TEXTO = "#e8d5ff"
COR_MUTED = "#9b7fc0"


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, navegacao):
        super().__init__(master, width=220, fg_color=BG_SIDEBAR, corner_radius=0)
        self.navegacao = navegacao
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.botoes = {}

        # Logo
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(pady=(24, 32), padx=20, anchor="w")

        ctk.CTkLabel(
            logo_frame,
            text="⬡",
            font=ctk.CTkFont(size=28),
            text_color=COR_ROXA
        ).pack(side="left", padx=(0, 10))

        info = ctk.CTkFrame(logo_frame, fg_color="transparent")
        info.pack(side="left")

        ctk.CTkLabel(
            info,
            text="PipoStudy",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=COR_TEXTO
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text="REVISÃO ESPAÇADA",
            font=ctk.CTkFont(size=9),
            text_color=COR_MUTED
        ).pack(anchor="w")

        # Menu
        ctk.CTkLabel(
            self,
            text="MENU",
            font=ctk.CTkFont(size=10),
            text_color=COR_MUTED
        ).pack(anchor="w", padx=24, pady=(0, 8))

        self._criar_item("dashboard", "⊞", "Início")
        self._criar_item("meus_assuntos", "☰", "Meus Assuntos")
        self._criar_item("revisao", "↻", "Revisar")

        # Total de assuntos no rodapé
        self.rodape = ctk.CTkFrame(self, fg_color=BG_ITEM, corner_radius=12)
        self.rodape.pack(side="bottom", fill="x", padx=16, pady=16)

        ctk.CTkLabel(
            self.rodape,
            text="⊙",
            font=ctk.CTkFont(size=13),
            text_color=COR_MUTED
        ).pack(side="left", padx=(12, 6), pady=10)

        ctk.CTkLabel(
            self.rodape,
            text="Total de assuntos",
            font=ctk.CTkFont(size=12),
            text_color=COR_MUTED
        ).pack(side="left", pady=10)

        self.label_total = ctk.CTkLabel(
            self.rodape,
            text="0",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COR_TEXTO
        )
        self.label_total.pack(side="right", padx=12, pady=10)

        self.atualizar_badge()

    def _criar_item(self, tela: str, icone: str, label: str):
        frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            corner_radius=10,
            cursor="hand2"
        )
        frame.pack(fill="x", padx=12, pady=2)

        icone_label = ctk.CTkLabel(
            frame,
            text=icone,
            font=ctk.CTkFont(size=15),
            text_color=COR_MUTED,
            width=28
        )
        icone_label.pack(side="left", padx=(12, 8), pady=10)

        texto_label = ctk.CTkLabel(
            frame,
            text=label,
            font=ctk.CTkFont(size=13),
            text_color=COR_MUTED
        )
        texto_label.pack(side="left", pady=10)

        # Badge de revisões pendentes para "Revisar"
        if tela == "revisao":
            self.badge = ctk.CTkLabel(
                frame,
                text="0",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="white",
                fg_color="#db2777",
                corner_radius=10,
                width=24,
                height=20
            )
            self.badge.pack(side="right", padx=12)

        def on_click(e=None):
            self.navegacao(tela)

        for widget in [frame, icone_label, texto_label]:
            widget.bind("<Button-1>", on_click)

        self.botoes[tela] = (frame, icone_label, texto_label)

    def set_ativo(self, tela: str):
        for nome, (frame, icone, texto) in self.botoes.items():
            if nome == tela:
                frame.configure(fg_color=BG_ATIVO)
                icone.configure(text_color=COR_ROXA)
                texto.configure(text_color=COR_TEXTO, font=ctk.CTkFont(size=13, weight="bold"))
            else:
                frame.configure(fg_color="transparent")
                icone.configure(text_color=COR_MUTED)
                texto.configure(text_color=COR_MUTED, font=ctk.CTkFont(size=13))
        self.atualizar_badge()

    def atualizar_badge(self):
        itens = carregar_dados()
        para_hoje, atrasados = classificar_itens(itens)
        total_pendentes = len(para_hoje) + len(atrasados)
        total = len(itens)
        self.label_total.configure(text=str(total))
        if hasattr(self, "badge"):
            self.badge.configure(text=str(total_pendentes))