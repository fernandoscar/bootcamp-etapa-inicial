import customtkinter as ctk
from src.core.repositorio import carregar_dados
from src.core.agendador import classificar_itens

# --- CONFIGURAÇÃO DE CORES ---
BG = "#0d0b14"
BG_CARD = "#12101a"
BG_ITEM = "#1a1025"
COR_TEXTO = "#e8d5ff"
COR_MUTED = "#9b7fc0"
COR_ROXA = "#7c3aed"
COR_VERDE = "#10b981"
COR_VERMELHA = "#ef4444"


class Dashboard(ctk.CTkFrame):
    def __init__(self, master, on_revisar=None, on_cadastrar=None, **kwargs):
        super().__init__(master, fg_color=BG, corner_radius=0, **kwargs)

        self.on_revisar = on_revisar
        self.on_cadastrar = on_cadastrar

        # CARREGAMENTO DE DADOS
        self.itens = carregar_dados()
        res = classificar_itens(self.itens)
        self.para_hoje, self.atrasados = res
        self.fila_total = self.atrasados + self.para_hoje

        self._criar_cabecalho()
        self._criar_cards_resumo()

        # Layout
        self.conteudo = ctk.CTkFrame(self, fg_color="transparent")
        self.conteudo.pack(fill="both", expand=True, padx=40, pady=(0, 24))

        self.col_esq = ctk.CTkFrame(self.conteudo, fg_color="transparent")
        self.col_esq.pack(side="left", fill="both", expand=True, padx=(0, 16))

        self.col_dir = ctk.CTkFrame(
            self.conteudo, fg_color="transparent", width=340
        )
        self.col_dir.pack(side="right", fill="y")
        self.col_dir.pack_propagate(False)

        self._criar_secao_revisoes()
        self._criar_grafico_atividade()
        self._criar_proximas_revisoes()

    def _criar_cabecalho(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(32, 24))
        ctk.CTkLabel(
            header, text="Boa tarde! 👋",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COR_TEXTO
        ).pack(anchor="w")
        ctk.CTkLabel(
            header, text="domingo, 12 de abril de 2026",
            font=ctk.CTkFont(size=14), text_color=COR_MUTED
        ).pack(anchor="w")

    def _criar_cards_resumo(self):
        cards_f = ctk.CTkFrame(self, fg_color="transparent")
        cards_f.pack(fill="x", padx=40, pady=(0, 24))

        self._criar_card(cards_f, str(len(self.para_hoje)), "Para Hoje", "📅")
        self._criar_card(cards_f, str(len(self.atrasados)), "Atrasadas", "⏰")
        self._criar_card(cards_f, str(len(self.itens)), "Total", "📖")
        self._criar_card(cards_f, "0d", "Sequência", "🔥")

    def _criar_card(self, parent, valor, titulo, icone):
        card = ctk.CTkFrame(
            parent, fg_color=BG_CARD, corner_radius=16, height=100
        )
        card.pack(side="left", expand=True, fill="both", padx=(0, 16))
        card.pack_propagate(False)

        ctk.CTkLabel(
            card, text=icone, font=ctk.CTkFont(size=18)
        ).pack(anchor="w", padx=20, pady=(16, 5))
        ctk.CTkLabel(
            card, text=valor, font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COR_TEXTO
        ).pack(anchor="w", padx=20)
        ctk.CTkLabel(
            card, text=titulo, font=ctk.CTkFont(size=12),
            text_color=COR_MUTED
        ).pack(anchor="w", padx=20, pady=(0, 16))

    def _criar_secao_revisoes(self):
        card_fila = ctk.CTkFrame(
            self.col_esq, fg_color=BG_CARD, corner_radius=16
        )
        card_fila.pack(fill="both", expand=True)

        ctk.CTkLabel(
            card_fila, text="Revisões Pendentes",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COR_TEXTO
        ).pack(anchor="w", padx=24, pady=24)

        lista = ctk.CTkFrame(card_fila, fg_color="transparent")
        lista.pack(fill="both", expand=True)

        if not self.fila_total:
            ctk.CTkLabel(
                lista, text="Tudo em dia! ✨",
                font=ctk.CTkFont(size=14), text_color=COR_MUTED
            ).pack(expand=True)
        else:
            for item in self.fila_total[:5]:
                atrasado = item in self.atrasados
                cor_s = COR_VERMELHA if atrasado else COR_VERDE
                bg_s = "#7f1d1d" if atrasado else "#064e3b"
                self._criar_linha(
                    lista, item.get("assunto", ""),
                    item.get("materia", ""),
                    "atrasada" if atrasado else "hoje",
                    cor_s, bg_s
                )

        self._btn_revisao(card_fila)

    def _btn_revisao(self, parent):
        ctk.CTkButton(
            parent, text=f"Começar Revisão ({len(self.fila_total)})",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=COR_ROXA, height=48, corner_radius=12,
            command=self.on_revisar,
            state="normal" if self.fila_total else "disabled"
        ).pack(fill="x", padx=24, pady=24, side="bottom")

    def _criar_linha(self, parent, tit, sub, txt_s, cor_t, cor_b):
        linha = ctk.CTkFrame(parent, fg_color="transparent")
        linha.pack(fill="x", padx=24, pady=(0, 15))
        ctk.CTkLabel(linha, text="●", text_color=COR_ROXA).pack(side="left")

        info = ctk.CTkFrame(linha, fg_color="transparent")
        info.pack(side="left", padx=10)
        ctk.CTkLabel(
            info, text=tit[:25], font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COR_TEXTO
        ).pack(anchor="w")
        ctk.CTkLabel(
            info, text=sub, font=ctk.CTkFont(size=11),
            text_color=COR_MUTED
        ).pack(anchor="w")

        ctk.CTkLabel(
            linha, text=txt_s, font=ctk.CTkFont(size=10, weight="bold"),
            text_color=cor_t, fg_color=cor_b, corner_radius=6, padx=8
        ).pack(side="right")

    def _criar_grafico_atividade(self):
        card = ctk.CTkFrame(
            self.col_dir, fg_color=BG_CARD, corner_radius=16, height=180
        )
        card.pack(fill="x", pady=(0, 16))
        card.pack_propagate(False)
        ctk.CTkLabel(
            card, text="📈 Atividade semanal",
            font=ctk.CTkFont(size=12), text_color=COR_TEXTO
        ).pack(anchor="w", padx=20, pady=15)

    def _criar_proximas_revisoes(self):
        card = ctk.CTkFrame(self.col_dir, fg_color=BG_CARD, corner_radius=16)
        card.pack(fill="both", expand=True)
        ctk.CTkLabel(
            card, text="Próximas Revisões",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO
        ).pack(anchor="w", padx=20, pady=15)
