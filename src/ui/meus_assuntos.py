import customtkinter as ctk
from datetime import date
from src.core.repositorio import carregar_dados, deletar_item, editar_item
from src.core.agendador import classificar_itens, INTERVALOS

# --- PALETA DE CORES ---
BG = "#0d0b14"
BG_CARD = "#12101a"
BG_ITEM = "#1a1025"
COR_ROXA = "#7c3aed"
COR_MAGENTA = "#db2777"
COR_TEXTO = "#e8d5ff"
COR_MUTED = "#9b7fc0"
COR_VERDE = "#16a34a"
COR_VERMELHO = "#dc2626"
COR_AMARELO = "#d97706"


class MeusAssuntos(ctk.CTkFrame):
    def __init__(self, master, on_cadastrar=None, on_voltar=None, **kwargs):
        super().__init__(master, fg_color=BG, **kwargs)
        self.on_cadastrar = on_cadastrar
        self.on_voltar = on_voltar
        self.filtro_ativo = "todos"
        self.busca_var = ctk.StringVar()
        self.busca_var.trace("w", lambda *a: self._renderizar_cards())
        self._build()

    def _build(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(32, 16))
        header.grid_columnconfigure(0, weight=1)

        titulo_f = ctk.CTkFrame(header, fg_color="transparent")
        titulo_f.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            titulo_f, text="Meus Assuntos",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COR_TEXTO
        ).pack(anchor="w")

        self.label_total = ctk.CTkLabel(
            titulo_f, text="",
            font=ctk.CTkFont(size=13), text_color=COR_MUTED
        )
        self.label_total.pack(anchor="w", pady=(2, 0))

        if self.on_cadastrar:
            ctk.CTkButton(
                header, text="+ Novo Assunto",
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color=COR_ROXA, hover_color="#6d28d9",
                corner_radius=20, height=40, width=160,
                command=self.on_cadastrar
            ).grid(row=0, column=1, sticky="e")

        # Controles (Busca e Filtros)
        cntrls = ctk.CTkFrame(self, fg_color="transparent")
        cntrls.pack(fill="x", padx=40, pady=(0, 16))
        cntrls.grid_columnconfigure(0, weight=1)

        busca_f = ctk.CTkFrame(cntrls, fg_color=BG_CARD, corner_radius=12)
        busca_f.grid(row=0, column=0, sticky="ew", padx=(0, 16))

        ctk.CTkLabel(
            busca_f, text="⌕", font=ctk.CTkFont(size=16),
            text_color=COR_MUTED
        ).pack(side="left", padx=12)

        ctk.CTkEntry(
            busca_f, textvariable=self.busca_var,
            placeholder_text="Buscar assunto, disciplina...",
            placeholder_text_color=COR_MUTED, fg_color="transparent",
            border_width=0, text_color=COR_TEXTO,
            font=ctk.CTkFont(size=13), height=44
        ).pack(side="left", fill="x", expand=True, padx=(0, 12))

        # Filtros
        self.filtros_f = ctk.CTkFrame(cntrls, fg_color="transparent")
        self.filtros_f.grid(row=0, column=1)

        self.btns_filtro = {}
        filtros = [
            ("todos", "Todos"), ("hoje", "Hoje"),
            ("atrasados", "Atrasados"), ("proximos", "Próximos")
        ]
        for key, lbl in filtros:
            btn = ctk.CTkButton(
                self.filtros_f, text=lbl, font=ctk.CTkFont(size=12),
                fg_color=COR_ROXA if key == "todos" else BG_CARD,
                hover_color="#6d28d9",
                text_color=COR_TEXTO if key == "todos" else COR_MUTED,
                corner_radius=20, height=36, width=90,
                command=lambda k=key: self._set_filtro(k)
            )
            btn.pack(side="left", padx=4)
            self.btns_filtro[key] = btn

        # Alerta de atrasados
        itens = carregar_dados()
        _, atrasados = classificar_itens(itens)
        if atrasados:
            self._criar_alerta_atraso(atrasados)

        # Grid de cards
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=40, pady=(0, 32))

        self._renderizar_cards()

    def _criar_alerta_atraso(self, atrasados):
        alerta = ctk.CTkFrame(
            self, fg_color="#2d0a0a", corner_radius=12,
            border_width=1, border_color=COR_VERMELHO
        )
        alerta.pack(fill="x", padx=40, pady=(0, 16))
        txt = (
            f"  ⚠  {len(atrasados)} assunto"
            f"{'s' if len(atrasados) > 1 else ''} "
            "com revisão atrasada — clique para ver"
        )
        lbl = ctk.CTkLabel(
            alerta, text=txt, font=ctk.CTkFont(size=13),
            text_color="#f87171", cursor="hand2"
        )
        lbl.pack(side="left", padx=16, pady=12)
        lbl.bind("<Button-1>", lambda e: self._set_filtro("atrasados"))

    def _set_filtro(self, filtro: str):
        self.filtro_ativo = filtro
        for key, btn in self.btns_filtro.items():
            sel = key == filtro
            btn.configure(
                fg_color=COR_ROXA if sel else BG_CARD,
                text_color=COR_TEXTO if sel else COR_MUTED
            )
        self._renderizar_cards()

    def _renderizar_cards(self):
        for child in self.scroll.winfo_children():
            child.destroy()

        itens = carregar_dados()
        hoje_s = str(date.today())
        busca = self.busca_var.get().lower()

        para_hoje, atrasados = classificar_itens(itens)
        ids_hoje = {i["id"] for i in para_hoje}
        ids_atrasados = {i["id"] for i in atrasados}

        if self.filtro_ativo == "hoje":
            itens = [i for i in itens if i["id"] in ids_hoje]
        elif self.filtro_ativo == "atrasados":
            itens = [i for i in itens if i["id"] in ids_atrasados]
        elif self.filtro_ativo == "proximos":
            itens = [i for i in itens if i["data_agendada"] > hoje_s]

        if busca:
            itens = [
                i for i in itens
                if busca in i["assunto"].lower() or busca in i["materia"].lower()
            ]

        p = 's' if len(itens) != 1 else ''
        self.label_total.configure(text=f"{len(itens)} tópico{p} cadastrado{p}")

        if not itens:
            ctk.CTkLabel(
                self.scroll, text="Nenhum assunto encontrado.",
                font=ctk.CTkFont(size=14), text_color=COR_MUTED
            ).pack(pady=40)
            return

        grid = ctk.CTkFrame(self.scroll, fg_color="transparent")
        grid.pack(fill="x")
        grid.grid_columnconfigure((0, 1, 2), weight=1)

        for idx, item in enumerate(itens):
            self._criar_card(grid, item, ids_hoje, ids_atrasados, idx // 3, idx % 3)

    def _criar_card(self, parent, item, ids_hoje, ids_atrasados, row, col):
        hoje_s = str(date.today())
        is_atrasado = item["id"] in ids_atrasados
        is_hoje = item["id"] in ids_hoje

        cor_b = COR_VERMELHO if is_atrasado else (COR_VERDE if is_hoje else "#2d1b4e")

        card = ctk.CTkFrame(
            parent, fg_color=BG_CARD, corner_radius=16,
            border_width=1, border_color=cor_b
        )
        card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", padx=20, pady=20)

        # Tags
        tags = ctk.CTkFrame(inner, fg_color="transparent")
        tags.pack(fill="x", pady=(0, 8))

        cat = item.get("categoria", "semestre")
        sem = item.get("semestre")
        cor_c = COR_ROXA if cat == "semestre" else COR_MAGENTA
        txt_t = f"{sem}º semestre" if cat == "semestre" else "auto-estudo"

        ctk.CTkLabel(
            tags, text=txt_t, font=ctk.CTkFont(size=11), fg_color="#2d1b4e",
            corner_radius=8, text_color=cor_c, padx=8, pady=3
        ).pack(side="left", padx=(0, 6))

        ctk.CTkLabel(
            tags, text=cat, font=ctk.CTkFont(size=11), fg_color="#1a1025",
            corner_radius=8, text_color=COR_MUTED, padx=8, pady=3
        ).pack(side="left")

        # Texto Principal
        txt_ass = item["assunto"][:30] + ("..." if len(item["assunto"]) > 30 else "")
        ctk.CTkLabel(
            inner, text=txt_ass, font=ctk.CTkFont(size=15, weight="bold"),
            text_color=COR_TEXTO, anchor="w", wraplength=220
        ).pack(anchor="w", pady=(4, 2))

        ctk.CTkLabel(
            inner, text=item["materia"], font=ctk.CTkFont(size=12),
            text_color=COR_MUTED, anchor="w"
        ).pack(anchor="w", pady=(0, 12))

        ctk.CTkFrame(inner, fg_color="#2d1b4e", height=1).pack(fill="x", pady=(0, 12))

        # Rodapé Card
        self._criar_rodape_card(inner, item, hoje_s, is_atrasado, is_hoje)

    def _criar_rodape_card(self, inner, item, hoje_s, is_atrasado, is_hoje):
        prox_f = ctk.CTkFrame(inner, fg_color="transparent")
        prox_f.pack(fill="x", pady=(0, 6))
        ctk.CTkLabel(
            prox_f, text="📅 próxima revisão",
            font=ctk.CTkFont(size=11), text_color=COR_MUTED
        ).pack(side="left")

        if is_atrasado:
            dias = (date.today() - date.fromisoformat(item["data_agendada"])).days
            b_txt, b_cor = f"atrasada {dias}d", COR_VERMELHO
        elif is_hoje:
            b_txt, b_cor = "hoje", COR_VERDE
        else:
            dias = (date.fromisoformat(item["data_agendada"]) - date.today()).days
            b_txt = f"em {dias} dias" if dias > 1 else "amanhã"
            b_cor = COR_AMARELO

        ctk.CTkLabel(
            prox_f, text=b_txt, text_color=b_cor,
            font=ctk.CTkFont(size=11, weight="bold")
        ).pack(side="right")

        # Estatísticas
        rev_f = ctk.CTkFrame(inner, fg_color="transparent")
        rev_f.pack(fill="x", pady=(0, 12))
        t_rev = item.get("total_revisoes", 0)
        i_dias = INTERVALOS[item.get("indice_intervalo", 0)]

        ctk.CTkLabel(
            rev_f, text=f"📖 {t_rev} revisões feitas",
            font=ctk.CTkFont(size=11), text_color=COR_MUTED
        ).pack(side="left")

        ctk.CTkLabel(
            rev_f, text=f"intervalo: {i_dias}d",
            font=ctk.CTkFont(size=11), text_color=COR_MUTED
        ).pack(side="right")

        # Botões
        self._criar_botoes_acao(inner, item)

    def _criar_botoes_acao(self, inner, item):
        acoes = ctk.CTkFrame(inner, fg_color="transparent")
        acoes.pack(fill="x")

        ctk.CTkButton(
            acoes, text="✏ Editar", font=ctk.CTkFont(size=12),
            fg_color="#2d1b4e", hover_color="#3d2a5a",
            text_color=COR_MUTED, corner_radius=8, height=32,
            command=lambda i=item: self._abrir_edicao(i)
        ).pack(side="left", expand=True, fill="x", padx=(0, 4))

        ctk.CTkButton(
            acoes, text="✕ Deletar", font=ctk.CTkFont(size=12),
            fg_color="#2d0a0a", hover_color="#4c0519",
            text_color="#f87171", corner_radius=8, height=32,
            command=lambda i=item: self._confirmar_delete(i)
        ).pack(side="left", expand=True, fill="x", padx=(4, 0))

    def _confirmar_delete(self, item):
        dialog = ctk.CTkToplevel(self)
        dialog.title("")
        dialog.geometry("360x180")
        dialog.configure(fg_color=BG_CARD)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        ctk.CTkLabel(
            dialog, text="Deletar assunto?",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COR_TEXTO
        ).pack(pady=(24, 8))

        ctk.CTkLabel(
            dialog, text=f'"{item["assunto"]}" será removido.',
            font=ctk.CTkFont(size=12), text_color=COR_MUTED
        ).pack()

        btns = ctk.CTkFrame(dialog, fg_color="transparent")
        btns.pack(pady=20)

        ctk.CTkButton(
            btns, text="Cancelar", fg_color="#2d1b4e", width=120,
            command=dialog.destroy
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            btns, text="Deletar", fg_color="#4c0519", width=120,
            command=lambda: self._deletar(item["id"], dialog)
        ).pack(side="left", padx=8)

    def _deletar(self, item_id, dialog):
        dialog.destroy()
        deletar_item(item_id)
        self._renderizar_cards()

    def _abrir_edicao(self, item):
        dialog = ctk.CTkToplevel(self)
        dialog.geometry("480x560")
        dialog.configure(fg_color=BG_CARD)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        ctk.CTkLabel(
            dialog, text="Editar Assunto",
            font=ctk.CTkFont(size=18, weight="bold"), text_color=COR_TEXTO
        ).pack(pady=(24, 20))

        inner = ctk.CTkFrame(dialog, fg_color="transparent")
        inner.pack(fill="x", padx=28)

        # Inputs
        e_mat = self._criar_input_edicao(inner, "Matéria", item["materia"])
        e_ass = self._criar_input_edicao(inner, "Assunto", item["assunto"])

        ctk.CTkLabel(
            inner, text="Anotação", font=ctk.CTkFont(size=12),
            text_color=COR_MUTED
        ).pack(anchor="w")

        e_anot = ctk.CTkTextbox(
            inner, height=80, fg_color=BG_ITEM, border_color="#2d1b4e",
            text_color=COR_TEXTO, corner_radius=10
        )
        e_anot.pack(fill="x", pady=(4, 16))
        e_anot.insert("1.0", item.get("anotacao", ""))

        # Categoria e Botão Salvar
        self._build_footer_edicao(dialog, inner, item, e_mat, e_ass, e_anot)

    def _criar_input_edicao(self, parent, label, valor):
        ctk.CTkLabel(
            parent, text=label, font=ctk.CTkFont(size=12),
            text_color=COR_MUTED
        ).pack(anchor="w")

        entry = ctk.CTkEntry(
            parent, height=40, fg_color=BG_ITEM, border_color="#2d1b4e",
            text_color=COR_TEXTO, corner_radius=10
        )
        entry.pack(fill="x", pady=(4, 12))
        entry.insert(0, valor)
        return entry

    def _build_footer_edicao(self, dialog, inner, item, e_mat, e_ass, e_anot):
        cat_v = ctk.StringVar(value=item.get("categoria", "semestre"))
        cat_f = ctk.CTkFrame(inner, fg_color=BG_ITEM, corner_radius=10)
        cat_f.pack(fill="x", pady=(0, 12))

        b_sem = ctk.CTkButton(
            cat_f, text="Semestre", corner_radius=8, height=34,
            fg_color=COR_ROXA if cat_v.get() == "semestre" else "transparent"
        )
        b_sem.pack(side="left", expand=True, fill="x", padx=4, pady=4)

        b_aut = ctk.CTkButton(
            cat_f, text="Auto-Estudo", corner_radius=8, height=34,
            fg_color=COR_MAGENTA if cat_v.get() == "auto-estudo" else "transparent"
        )
        b_aut.pack(side="left", expand=True, fill="x", padx=4, pady=4)

        def mudar_cat(c):
            cat_v.set(c)
            b_sem.configure(fg_color=COR_ROXA if c == "semestre" else "transparent")
            b_aut.configure(fg_color=COR_MAGENTA if c == "auto-estudo" else "transparent")

        b_sem.configure(command=lambda: mudar_cat("semestre"))
        b_aut.configure(command=lambda: mudar_cat("auto-estudo"))

        s_v = ctk.StringVar(value=f"{item.get('semestre', 1)}º semestre")
        sems = [f"{i}º semestre" for i in range(1, 9)]
        ctk.CTkOptionMenu(
            inner, values=sems, variable=s_v, fg_color=BG_ITEM,
            button_color=COR_ROXA, corner_radius=10, height=40
        ).pack(fill="x", pady=(0, 16))

        def salvar():
            sem_n = int(s_v.get()[0]) if cat_v.get() == "semestre" else None
            novos = {
                "materia": e_mat.get().strip(),
                "assunto": e_ass.get().strip(),
                "categoria": cat_v.get(),
                "semestre": sem_n,
                "anotacao": e_anot.get("1.0", "end").strip()
            }
            editar_item(item["id"], novos)
            dialog.destroy()
            self._renderizar_cards()

        ctk.CTkButton(
            inner, text="Salvar Alterações", fg_color=COR_ROXA,
            hover_color="#6d28d9", corner_radius=12, height=44,
            font=ctk.CTkFont(weight="bold"), command=salvar
        ).pack(fill="x")

        