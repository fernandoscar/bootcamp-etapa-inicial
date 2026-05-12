import customtkinter as ctk
from datetime import datetime, date
from src.core.repositorio import carregar_dados
from src.core.agendador import classificar_itens
from src.ui import theme


class Dashboard(ctk.CTkFrame):
    def __init__(self, master, on_revisar=None, on_cadastrar=None, **kwargs):
        super().__init__(master, fg_color=theme.get("BG"), corner_radius=0, **kwargs)

        self.on_revisar = on_revisar
        self.on_cadastrar = on_cadastrar

        self.itens = carregar_dados()
        res = classificar_itens(self.itens)
        self.para_hoje, self.atrasados = res
        self.fila_total = self.atrasados + self.para_hoje

        self._criar_cabecalho()
        self._criar_cards_resumo()

        # Layout principal: coluna esquerda + direita
        self.conteudo = ctk.CTkFrame(self, fg_color="transparent")
        self.conteudo.pack(fill="both", expand=True, padx=32, pady=(0, 24))

        self.col_esq = ctk.CTkFrame(self.conteudo, fg_color="transparent")
        self.col_esq.pack(side="left", fill="both", expand=True, padx=(0, 12))

        self.col_dir = ctk.CTkFrame(
            self.conteudo, fg_color="transparent", width=260
        )
        self.col_dir.pack(side="right", fill="y")
        self.col_dir.pack_propagate(False)

        self._criar_secao_revisoes()
        self._criar_grafico_atividade()
        self._criar_proximas_revisoes()

    def _criar_cabecalho(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(24, 18))

        hora = datetime.now().hour
        if hora < 12:
            saudacao = "Bom dia!"
        elif hora < 18:
            saudacao = "Boa tarde!"
        else:
            saudacao = "Boa noite!"

        ctk.CTkLabel(
            header, text=saudacao,
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=theme.get("COR_TEXTO"),
        ).pack(anchor="w")

        data_formatada = self._formatar_data_pt()

        ctk.CTkLabel(
            header, text=data_formatada,
            font=ctk.CTkFont(size=12), text_color=theme.get("COR_MUTED"),
        ).pack(anchor="w")

    @staticmethod
    def _formatar_data_pt() -> str:
        """Formata a data atual em português, sem depender de locale."""
        dias = [
            "segunda-feira", "terça-feira", "quarta-feira",
            "quinta-feira", "sexta-feira", "sábado", "domingo",
        ]
        meses = [
            "", "janeiro", "fevereiro", "março", "abril",
            "maio", "junho", "julho", "agosto",
            "setembro", "outubro", "novembro", "dezembro",
        ]
        agora = datetime.now()
        dia_semana = dias[agora.weekday()]
        mes = meses[agora.month]
        return f"{dia_semana}, {agora.day} de {mes} de {agora.year}"

    def _criar_cards_resumo(self):
        cards_f = ctk.CTkFrame(self, fg_color="transparent")
        cards_f.pack(fill="x", padx=32, pady=(0, 16))
        cards_f.grid_columnconfigure((0, 1, 2, 3), weight=1)

        dados = [
            (str(len(self.para_hoje)), "Para hoje", "📅", "ICON_PURPLE_BG", "COR_ROXA"),
            (str(len(self.atrasados)), "Atrasadas", "⚠", "ICON_RED_BG", "COR_VERMELHA"),
            (str(len(self.itens)), "Total", "📖", "ICON_BLUE_BG", "COR_AZUL"),
            ("0d", "Sequência", "🔥", "ICON_AMBER_BG", "COR_AMARELO"),
        ]

        for col, (valor, titulo, icone, bg_icon, cor_icon) in enumerate(dados):
            self._criar_card(cards_f, valor, titulo, icone, bg_icon, cor_icon, col)

    def _criar_card(self, parent, valor, titulo, icone, bg_icon, cor_icon, col):
        card = ctk.CTkFrame(
            parent, fg_color=theme.get("BG_CARD"),
            corner_radius=14, height=80,
        )
        card.grid(row=0, column=col, padx=5, sticky="nsew")
        card.pack_propagate(False)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=14, pady=14)

        # Ícone em círculo colorido
        icon_frame = ctk.CTkFrame(
            inner, fg_color=theme.get(bg_icon),
            corner_radius=10, width=38, height=38,
        )
        icon_frame.pack(side="left", padx=(0, 12))
        icon_frame.pack_propagate(False)
        ctk.CTkLabel(
            icon_frame, text=icone, font=ctk.CTkFont(size=16),
        ).pack(expand=True)

        info = ctk.CTkFrame(inner, fg_color="transparent")
        info.pack(side="left")
        ctk.CTkLabel(
            info, text=valor,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=theme.get("COR_TEXTO"),
        ).pack(anchor="w")
        ctk.CTkLabel(
            info, text=titulo,
            font=ctk.CTkFont(size=10), text_color=theme.get("COR_MUTED"),
        ).pack(anchor="w")

    def _criar_secao_revisoes(self):
        card = ctk.CTkFrame(
            self.col_esq, fg_color=theme.get("BG_CARD"), corner_radius=14,
        )
        card.pack(fill="both", expand=True)

        # Header
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=(16, 12))

        ctk.CTkLabel(
            header, text="✓  Revisões pendentes",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=theme.get("COR_TEXTO"),
        ).pack(side="left")

        # Lista
        lista = ctk.CTkFrame(card, fg_color="transparent")
        lista.pack(fill="both", expand=True, padx=10)

        if not self.fila_total:
            ctk.CTkLabel(
                lista, text="Tudo em dia! ✨",
                font=ctk.CTkFont(size=13), text_color=theme.get("COR_MUTED"),
            ).pack(expand=True)
        else:
            icones_materias = {
                "estrutura de dados": "🌳",
                "redes": "🌐",
                "banco de dados": "🗄",
                "algoritmos": "⚡",
                "poo": "🔷",
            }
            cores_materias = {
                "estrutura de dados": "ICON_PURPLE_BG",
                "redes": "ICON_TEAL_BG",
                "banco de dados": "ICON_PINK_BG",
                "algoritmos": "ICON_AMBER_BG",
                "poo": "ICON_BLUE_BG",
            }
            for item in self.fila_total[:5]:
                atrasado = item in self.atrasados
                mat_lower = item.get("materia", "").lower()
                icone = icones_materias.get(mat_lower, "📘")
                cor_bg = cores_materias.get(mat_lower, "ICON_PURPLE_BG")
                rev_num = item.get("total_revisoes", 0)
                self._criar_linha_revisao(
                    lista, item.get("assunto", ""),
                    item.get("materia", ""),
                    icone, cor_bg,
                    f"{rev_num + 1}ª rev",
                    atrasado,
                )

        # Botão + progresso
        bottom = ctk.CTkFrame(card, fg_color="transparent")
        bottom.pack(fill="x", padx=18, pady=(8, 16))

        ctk.CTkButton(
            bottom,
            text=f"▶  Começar revisão ({len(self.fila_total)})",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=theme.get("COR_ROXA"), hover_color=theme.get("COR_ROXA_HOVER"),
            height=40, corner_radius=10,
            command=self.on_revisar,
            state="normal" if self.fila_total else "disabled",
        ).pack(fill="x", pady=(0, 8))

        # Barra de progresso semanal
        prog_f = ctk.CTkFrame(bottom, fg_color="transparent")
        prog_f.pack(fill="x")
        ctk.CTkLabel(
            prog_f, text="Progresso semanal",
            font=ctk.CTkFont(size=9), text_color=theme.get("COR_MUTED"),
        ).pack(side="left")
        ctk.CTkLabel(
            prog_f, text="0%",
            font=ctk.CTkFont(size=9), text_color=theme.get("COR_MUTED"),
        ).pack(side="right")

        prog_bar = ctk.CTkProgressBar(
            bottom, fg_color=theme.get("BG_ITEM"),
            progress_color=theme.get("COR_ROXA"),
            height=5, corner_radius=3,
        )
        prog_bar.pack(fill="x", pady=(2, 0))
        prog_bar.set(0)

    def _criar_linha_revisao(self, parent, assunto, materia, icone, cor_bg,
                             rev_txt, atrasado):
        linha = ctk.CTkFrame(
            parent, fg_color=theme.get("BG_ITEM"), corner_radius=10,
        )
        linha.pack(fill="x", padx=8, pady=3)

        # Ícone da matéria
        ic_frame = ctk.CTkFrame(
            linha, fg_color=theme.get(cor_bg),
            corner_radius=8, width=30, height=30,
        )
        ic_frame.pack(side="left", padx=(10, 8), pady=8)
        ic_frame.pack_propagate(False)
        ctk.CTkLabel(
            ic_frame, text=icone, font=ctk.CTkFont(size=13),
        ).pack(expand=True)

        info = ctk.CTkFrame(linha, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True, pady=8)
        ctk.CTkLabel(
            info, text=assunto[:25],
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=theme.get("COR_TEXTO"),
        ).pack(anchor="w")
        ctk.CTkLabel(
            info, text=materia,
            font=ctk.CTkFont(size=9), text_color=theme.get("COR_MUTED"),
        ).pack(anchor="w")

        # Número da revisão
        ctk.CTkLabel(
            linha, text=rev_txt,
            font=ctk.CTkFont(size=9), text_color=theme.get("COR_MUTED"),
        ).pack(side="right", padx=(0, 6))

        # Tag de status
        if atrasado:
            tag_bg, tag_cor, tag_txt = (
                theme.get("BG_VERMELHO"), theme.get("COR_VERMELHO"), "atrasada"
            )
        else:
            tag_bg, tag_cor, tag_txt = (
                theme.get("BG_VERDE"), theme.get("COR_VERDE_ALT"), "hoje"
            )

        ctk.CTkLabel(
            linha, text=tag_txt,
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=tag_cor, fg_color=tag_bg,
            corner_radius=5, padx=7, pady=2,
        ).pack(side="right", padx=(0, 8))

    def _criar_grafico_atividade(self):
        card = ctk.CTkFrame(
            self.col_dir, fg_color=theme.get("BG_CARD"),
            corner_radius=14, height=160,
        )
        card.pack(fill="x", pady=(0, 10))
        card.pack_propagate(False)

        ctk.CTkLabel(
            card, text="📊  Atividade",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=theme.get("COR_TEXTO"),
        ).pack(anchor="w", padx=16, pady=(14, 8))

        # Barras simuladas
        bar_f = ctk.CTkFrame(card, fg_color="transparent", height=65)
        bar_f.pack(fill="x", padx=16)
        bar_f.pack_propagate(False)

        dias = ["S", "T", "Q", "Q", "S", "S", "D"]
        alturas = [0.2, 0.5, 0.35, 0.8, 0.25, 0.6, 0.1]
        bar_f.grid_columnconfigure(tuple(range(7)), weight=1)

        for i, (dia, h) in enumerate(zip(dias, alturas)):
            col_f = ctk.CTkFrame(bar_f, fg_color="transparent")
            col_f.grid(row=0, column=i, sticky="nsew", padx=2)
            col_f.grid_rowconfigure(0, weight=1)

            cor = theme.get("COR_ROXA") if i == 3 else theme.get("BG_ATIVO")
            bar = ctk.CTkFrame(col_f, fg_color=cor, corner_radius=3)
            bar.place(relx=0.2, rely=1.0 - h, relwidth=0.6, relheight=h)

        # Labels dos dias
        label_f = ctk.CTkFrame(card, fg_color="transparent")
        label_f.pack(fill="x", padx=16, pady=(4, 10))
        label_f.grid_columnconfigure(tuple(range(7)), weight=1)
        for i, dia in enumerate(dias):
            ctk.CTkLabel(
                label_f, text=dia,
                font=ctk.CTkFont(size=8), text_color=theme.get("COR_MUTED"),
            ).grid(row=0, column=i)

    def _criar_proximas_revisoes(self):
        card = ctk.CTkFrame(
            self.col_dir, fg_color=theme.get("BG_CARD"), corner_radius=14,
        )
        card.pack(fill="both", expand=True)

        ctk.CTkLabel(
            card, text="📅  Próximas",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=theme.get("COR_TEXTO"),
        ).pack(anchor="w", padx=16, pady=(14, 8))

        # Itens futuros (próximas revisões)
        futuros = [
            i for i in self.itens
            if i.get("data_agendada", "") > str(date.today())
        ]
        futuros.sort(key=lambda x: x.get("data_agendada", ""))

        if not futuros:
            ctk.CTkLabel(
                card, text="Nenhuma revisão agendada",
                font=ctk.CTkFont(size=11),
                text_color=theme.get("COR_MUTED"),
            ).pack(padx=16, pady=8)
        else:
            for item in futuros[:4]:
                self._criar_linha_proxima(card, item)

    def _criar_linha_proxima(self, parent, item):
        linha = ctk.CTkFrame(parent, fg_color="transparent")
        linha.pack(fill="x", padx=16, pady=4)

        ctk.CTkLabel(
            linha, text="●",
            font=ctk.CTkFont(size=8),
            text_color=theme.get("COR_ROXA"),
        ).pack(side="left", padx=(0, 8))

        info = ctk.CTkFrame(linha, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(
            info, text=item.get("assunto", "")[:20],
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=theme.get("COR_TEXTO"),
        ).pack(anchor="w")
        ctk.CTkLabel(
            info, text=item.get("materia", ""),
            font=ctk.CTkFont(size=8), text_color=theme.get("COR_MUTED"),
        ).pack(anchor="w")

        dias = (
            date.fromisoformat(item["data_agendada"]) - date.today()
        ).days
        txt = "amanhã" if dias == 1 else f"{dias} dias"

        ctk.CTkLabel(
            linha, text=txt,
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=theme.get("COR_AMARELO"),
        ).pack(side="right")
