import customtkinter as ctk
from src.core.repositorio import carregar_dados, atualizar_item
from src.core.agendador import calcular_proxima_data, classificar_itens
from src.ui import theme


class Revisao(ctk.CTkFrame):
    def __init__(self, master, on_voltar):
        super().__init__(master, fg_color=theme.get("BG"))
        self.on_voltar = on_voltar
        self.fila = []
        self.indice_atual = 0
        self.revelado = False
        self._build()
        self.carregar_fila()

    def _build(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(28, 0))
        header.grid_columnconfigure(1, weight=1)

        self.btn_voltar = ctk.CTkButton(
            header, text="←", font=ctk.CTkFont(size=16),
            fg_color="transparent", hover_color=theme.get("BG_ITEM"),
            text_color=theme.get("COR_MUTED"),
            width=36, height=36, corner_radius=10,
            command=self.on_voltar,
        )
        self.btn_voltar.grid(row=0, column=0, padx=(0, 14))

        self.progress_bar = ctk.CTkProgressBar(
            header, fg_color=theme.get("BG_ITEM"),
            progress_color=theme.get("COR_ROXA"),
            height=5, corner_radius=3,
        )
        self.progress_bar.grid(row=0, column=1, sticky="ew")
        self.progress_bar.set(0)

        self.label_progresso = ctk.CTkLabel(
            header, text="0 / 0",
            font=ctk.CTkFont(size=12), text_color=theme.get("COR_MUTED"),
            width=50,
        )
        self.label_progresso.grid(row=0, column=2, padx=(14, 0))

        self.card = ctk.CTkFrame(
            self, fg_color=theme.get("BG_CARD"),
            corner_radius=16, border_width=1,
            border_color=theme.get("BG_ATIVO"),
        )
        self.card.pack(fill="both", expand=True, padx=100, pady=28)

        self.card_inner = ctk.CTkFrame(self.card, fg_color="transparent")
        self.card_inner.pack(fill="both", expand=True, padx=28, pady=28)

        self._build_card_content()

    def _build_card_content(self):
        self.tags_frame = ctk.CTkFrame(self.card_inner, fg_color="transparent")
        self.tags_frame.pack(fill="x", pady=(0, 20))

        self.tag_materia = ctk.CTkLabel(
            self.tags_frame, text="",
            font=ctk.CTkFont(size=11),
            fg_color=theme.get("BG_ATIVO"), corner_radius=8,
            text_color=theme.get("COR_ROXA"), padx=10, pady=3,
        )
        self.tag_materia.pack(side="left", padx=(0, 6))

        self.tag_categoria = ctk.CTkLabel(
            self.tags_frame, text="",
            font=ctk.CTkFont(size=11),
            fg_color=theme.get("BG_ITEM"), corner_radius=8,
            text_color=theme.get("COR_MUTED"), padx=10, pady=3,
        )
        self.tag_categoria.pack(side="left")

        self.tag_revisoes = ctk.CTkLabel(
            self.tags_frame, text="",
            font=ctk.CTkFont(size=11),
            fg_color=theme.get("BG_ITEM"), corner_radius=8,
            text_color=theme.get("COR_MUTED"), padx=10, pady=3,
        )
        self.tag_revisoes.pack(side="right")

        self.label_assunto = ctk.CTkLabel(
            self.card_inner, text="",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=theme.get("COR_TEXTO"),
            wraplength=600, justify="left", anchor="w",
        )
        self.label_assunto.pack(anchor="w", pady=(0, 20))

        self.anotacao_frame = ctk.CTkFrame(
            self.card_inner, fg_color=theme.get("BG_ITEM"), corner_radius=12,
        )
        self.label_anotacao = ctk.CTkLabel(
            self.anotacao_frame, text="",
            font=ctk.CTkFont(size=13), text_color=theme.get("COR_TEXTO"),
            wraplength=560, justify="left",
        )
        self.label_anotacao.pack(padx=18, pady=14)

        self.btn_revelar = ctk.CTkButton(
            self.card_inner, text="⊙  Revelar conteúdo",
            font=ctk.CTkFont(size=13),
            fg_color=theme.get("BG_ITEM"),
            hover_color=theme.get("BG_ATIVO"),
            text_color=theme.get("COR_MUTED"),
            corner_radius=12, height=42,
            border_width=1, border_color=theme.get("BG_ATIVO"),
            command=self.revelar,
        )
        self.btn_revelar.pack(fill="x")

        self.feedback_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._build_feedback_section()

    def _build_feedback_section(self):
        ctk.CTkLabel(
            self.feedback_frame, text="Como foi sua lembrança?",
            font=ctk.CTkFont(size=12), text_color=theme.get("COR_MUTED"),
        ).pack(pady=(0, 10))

        btns = ctk.CTkFrame(self.feedback_frame, fg_color="transparent")
        btns.pack()
        btns.grid_columnconfigure((0, 1, 2), weight=1)

        self._criar_btn_feedback(
            btns, "✓", "Conexões Claras", "Lembrei bem",
            theme.get("BG_VERDE_ESCURO"), theme.get("COR_VERDE_ALT"),
            "claro", 0,
        )
        self._criar_btn_feedback(
            btns, "−", "Clareando", "Com esforço",
            theme.get("BG_AMARELO"), theme.get("COR_AMARELO"),
            "clareando", 1,
        )
        self._criar_btn_feedback(
            btns, "✕", "Ineficaz", "Não lembrei",
            theme.get("BG_VERMELHO_ESCURO"), theme.get("COR_MAGENTA"),
            "ineficaz", 2,
        )

    def _criar_btn_feedback(self, parent, icone, tit, sub, bg, cor, feed, col):
        btn = ctk.CTkFrame(
            parent, fg_color=bg, corner_radius=12,
            width=170, height=80, cursor="hand2",
        )
        btn.grid(row=0, column=col, padx=6)
        btn.pack_propagate(False)

        ctk.CTkLabel(
            btn, text=icone, font=ctk.CTkFont(size=16), text_color=cor,
        ).pack(pady=(14, 2))
        ctk.CTkLabel(
            btn, text=tit, font=ctk.CTkFont(size=12, weight="bold"),
            text_color=cor,
        ).pack()
        ctk.CTkLabel(
            btn, text=sub, font=ctk.CTkFont(size=10),
            text_color=theme.get("COR_MUTED"),
        ).pack()

        btn.bind("<Button-1>", lambda e: self.responder(feed))
        for w in btn.winfo_children():
            w.bind("<Button-1>", lambda e: self.responder(feed))

    def carregar_fila(self):
        itens = carregar_dados()
        para_hoje, atrasados = classificar_itens(itens)
        self.fila = atrasados + para_hoje
        self.indice_atual = 0
        self.mostrar_atual()

    def mostrar_atual(self):
        self.revelado = False
        self.anotacao_frame.pack_forget()
        self.feedback_frame.pack_forget()
        self.btn_revelar.pack(fill="x")

        if self.indice_atual >= len(self.fila):
            self._concluir_revisao()
            return

        item = self.fila[self.indice_atual]
        total = len(self.fila)

        self.progress_bar.set(self.indice_atual / total if total > 0 else 0)
        self.label_progresso.configure(text=f"{self.indice_atual + 1} / {total}")

        self.tag_materia.configure(text=f"● {item['materia']}")
        cat = item.get("categoria", "semestre")
        sem = item.get("semestre")
        txt_cat = f"{sem}º semestre" if cat == "semestre" else "auto-estudo"
        self.tag_categoria.configure(text=txt_cat)

        total_rev = item.get("total_revisoes", 0)
        self.tag_revisoes.configure(text=f"↻ {total_rev}ª revisão")
        self.label_assunto.configure(text=item["assunto"])

        anotacao = item.get("anotacao", "").strip()
        if anotacao:
            self.label_anotacao.configure(text=f'"{anotacao}"')
        else:
            self.btn_revelar.pack_forget()
            self.feedback_frame.pack(pady=(0, 28))

    def _concluir_revisao(self):
        self.label_assunto.configure(text="🎉 Revisão concluída!")
        self.tag_materia.configure(text="")
        self.tag_categoria.configure(text="")
        self.tag_revisoes.configure(text="")
        self.btn_revelar.pack_forget()
        ctk.CTkLabel(
            self.card_inner, text="Você está em dia com tudo.",
            font=ctk.CTkFont(size=13), text_color=theme.get("COR_MUTED"),
        ).pack()

    def revelar(self):
        if self.revelado:
            return
        self.revelado = True
        self.btn_revelar.pack_forget()
        self.anotacao_frame.pack(fill="x", pady=(0, 20))
        self.feedback_frame.pack(pady=(0, 28))

    def responder(self, feedback: str):
        item = self.fila[self.indice_atual]
        res = calcular_proxima_data(item["indice_intervalo"], feedback)
        nova_data, novo_indice = res
        status = "Precisa Reestudar" if feedback == "ineficaz" else "Revisado"
        atualizar_item(item["id"], str(nova_data), novo_indice, status)
        self.indice_atual += 1
        self.mostrar_atual()
