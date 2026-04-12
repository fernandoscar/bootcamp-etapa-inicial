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

        titulo_frame = ctk.CTkFrame(header, fg_color="transparent")
        titulo_frame.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            titulo_frame,
            text="Meus Assuntos",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COR_TEXTO
        ).pack(anchor="w")

        self.label_total = ctk.CTkLabel(
            titulo_frame,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=COR_MUTED
        )
        self.label_total.pack(anchor="w", pady=(2, 0))

        if self.on_cadastrar:
            ctk.CTkButton(
                header,
                text="+ Novo Assunto",
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color=COR_ROXA,
                hover_color="#6d28d9",
                corner_radius=20,
                height=40,
                width=160,
                command=self.on_cadastrar
            ).grid(row=0, column=1, sticky="e")

        # Busca e filtros
        controles = ctk.CTkFrame(self, fg_color="transparent")
        controles.pack(fill="x", padx=40, pady=(0, 16))
        controles.grid_columnconfigure(0, weight=1)

        busca = ctk.CTkFrame(controles, fg_color=BG_CARD, corner_radius=12)
        busca.grid(row=0, column=0, sticky="ew", padx=(0, 16))

        ctk.CTkLabel(busca, text="⌕", font=ctk.CTkFont(size=16), text_color=COR_MUTED).pack(side="left", padx=12)
        ctk.CTkEntry(
            busca,
            textvariable=self.busca_var,
            placeholder_text="Buscar assunto, disciplina...",
            placeholder_text_color=COR_MUTED,
            fg_color="transparent",
            border_width=0,
            text_color=COR_TEXTO,
            font=ctk.CTkFont(size=13),
            height=44
        ).pack(side="left", fill="x", expand=True, padx=(0, 12))

        # Filtros
        self.filtros_frame = ctk.CTkFrame(controles, fg_color="transparent")
        self.filtros_frame.grid(row=0, column=1)

        self.btns_filtro = {}
        filtros = [("todos", "Todos"), ("hoje", "Hoje"), ("atrasados", "Atrasados"), ("proximos", "Próximos")]
        for key, label in filtros:
            btn = ctk.CTkButton(
                self.filtros_frame,
                text=label,
                font=ctk.CTkFont(size=12),
                fg_color=COR_ROXA if key == "todos" else BG_CARD,
                hover_color="#6d28d9",
                text_color=COR_TEXTO if key == "todos" else COR_MUTED,
                corner_radius=20,
                height=36,
                width=90,
                command=lambda k=key: self._set_filtro(k)
            )
            btn.pack(side="left", padx=4)
            self.btns_filtro[key] = btn

        # Alerta de atrasados
        itens = carregar_dados()
        _, atrasados = classificar_itens(itens)
        if atrasados:
            alerta = ctk.CTkFrame(self, fg_color="#2d0a0a", corner_radius=12, border_width=1, border_color=COR_VERMELHO)
            alerta.pack(fill="x", padx=40, pady=(0, 16))
            label_alerta = ctk.CTkLabel(
                alerta,
                text=f"  ⚠  {len(atrasados)} assunto{'s' if len(atrasados) > 1 else ''} com revisão atrasada — clique para ver",
                font=ctk.CTkFont(size=13),
                text_color="#f87171",
                cursor="hand2"
            )
            label_alerta.pack(side="left", padx=16, pady=12)
            label_alerta.bind("<Button-1>", lambda e: self._set_filtro("atrasados"))

        # Grid de cards
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=40, pady=(0, 32))

        self._renderizar_cards()

    def _set_filtro(self, filtro: str):
        self.filtro_ativo = filtro
        for key, btn in self.btns_filtro.items():
            if key == filtro:
                btn.configure(fg_color=COR_ROXA, text_color=COR_TEXTO)
            else:
                btn.configure(fg_color=BG_CARD, text_color=COR_MUTED)
        self._renderizar_cards()

    def _renderizar_cards(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        itens = carregar_dados()
        hoje_str = str(date.today())
        busca = self.busca_var.get().lower()

        para_hoje, atrasados = classificar_itens(itens)
        ids_hoje = {i["id"] for i in para_hoje}
        ids_atrasados = {i["id"] for i in atrasados}

        if self.filtro_ativo == "hoje":
            itens = [i for i in itens if i["id"] in ids_hoje]
        elif self.filtro_ativo == "atrasados":
            itens = [i for i in itens if i["id"] in ids_atrasados]
        elif self.filtro_ativo == "proximos":
            itens = [i for i in itens if i["data_agendada"] > hoje_str]

        if busca:
            itens = [i for i in itens if busca in i["assunto"].lower() or busca in i["materia"].lower()]

        self.label_total.configure(text=f"{len(itens)} tópico{'s' if len(itens) != 1 else ''} cadastrado{'s' if len(itens) != 1 else ''}")

        if not itens:
            ctk.CTkLabel(self.scroll, text="Nenhum assunto encontrado.", font=ctk.CTkFont(size=14), text_color=COR_MUTED).pack(pady=40)
            return

        grid = ctk.CTkFrame(self.scroll, fg_color="transparent")
        grid.pack(fill="x")
        grid.grid_columnconfigure((0, 1, 2), weight=1)

        for idx, item in enumerate(itens):
            col = idx % 3
            row = idx // 3
            self._criar_card(grid, item, ids_hoje, ids_atrasados, row, col)

    def _criar_card(self, parent, item, ids_hoje, ids_atrasados, row, col):
        hoje_str = str(date.today())
        atrasado = item["id"] in ids_atrasados
        hoje = item["id"] in ids_hoje

        if atrasado:
            border_cor = COR_VERMELHO
        elif hoje:
            border_cor = COR_VERDE
        else:
            border_cor = "#2d1b4e"

        card = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=16, border_width=1, border_color=border_cor)
        card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", padx=20, pady=20)

        # Tags
        tags = ctk.CTkFrame(inner, fg_color="transparent")
        tags.pack(fill="x", pady=(0, 8))

        cat = item.get("categoria", "semestre")
        sem = item.get("semestre")
        cor_cat = COR_ROXA if cat == "semestre" else COR_MAGENTA
        tag_text = f"{sem}º semestre" if cat == "semestre" else "auto-estudo"

        ctk.CTkLabel(tags, text=tag_text, font=ctk.CTkFont(size=11), fg_color="#2d1b4e", corner_radius=8, text_color=cor_cat, padx=8, pady=3).pack(side="left", padx=(0, 6))
        ctk.CTkLabel(tags, text=cat, font=ctk.CTkFont(size=11), fg_color="#1a1025", corner_radius=8, text_color=COR_MUTED, padx=8, pady=3).pack(side="left")

        # Assunto e matéria
        ctk.CTkLabel(inner, text=item["assunto"][:30] + ("..." if len(item["assunto"]) > 30 else ""), font=ctk.CTkFont(size=15, weight="bold"), text_color=COR_TEXTO, anchor="w", wraplength=220).pack(anchor="w", pady=(4, 2))
        ctk.CTkLabel(inner, text=item["materia"], font=ctk.CTkFont(size=12), text_color=COR_MUTED, anchor="w").pack(anchor="w", pady=(0, 12))

        ctk.CTkFrame(inner, fg_color="#2d1b4e", height=1).pack(fill="x", pady=(0, 12))

        # Próxima revisão
        prox_frame = ctk.CTkFrame(inner, fg_color="transparent")
        prox_frame.pack(fill="x", pady=(0, 6))
        ctk.CTkLabel(prox_frame, text="📅 próxima revisão", font=ctk.CTkFont(size=11), text_color=COR_MUTED).pack(side="left")

        if atrasado:
            dias = (date.today() - date.fromisoformat(item["data_agendada"])).days
            badge_text = f"atrasada {dias}d"
            badge_cor = COR_VERMELHO
        elif hoje:
            badge_text = "hoje"
            badge_cor = COR_VERDE
        else:
            dias = (date.fromisoformat(item["data_agendada"]) - date.today()).days
            badge_text = f"em {dias} dias" if dias > 1 else "amanhã"
            badge_cor = COR_AMARELO

        ctk.CTkLabel(prox_frame, text=badge_text, font=ctk.CTkFont(size=11, weight="bold"), text_color=badge_cor).pack(side="right")

        # Total revisões
        rev_frame = ctk.CTkFrame(inner, fg_color="transparent")
        rev_frame.pack(fill="x", pady=(0, 12))
        total_rev = item.get("total_revisoes", 0)
        intervalo = item.get("indice_intervalo", 0)
        intervalo_dias = INTERVALOS[intervalo]

        ctk.CTkLabel(rev_frame, text=f"📖 {total_rev} revisões feitas", font=ctk.CTkFont(size=11), text_color=COR_MUTED).pack(side="left")
        ctk.CTkLabel(rev_frame, text=f"intervalo: {intervalo_dias}d", font=ctk.CTkFont(size=11), text_color=COR_MUTED).pack(side="right")

        # Botões
        acoes = ctk.CTkFrame(inner, fg_color="transparent")
        acoes.pack(fill="x")

        ctk.CTkButton(acoes, text="✏ Editar", font=ctk.CTkFont(size=12), fg_color="#2d1b4e", hover_color="#3d2a5a", 
                     text_color=COR_MUTED, corner_radius=8, height=32, 
                     command=lambda i=item: self._abrir_edicao(i)).pack(side="left", expand=True, fill="x", padx=(0, 4))

        ctk.CTkButton(acoes, text="✕ Deletar", font=ctk.CTkFont(size=12), fg_color="#2d0a0a", hover_color="#4c0519", 
                     text_color="#f87171", corner_radius=8, height=32, 
                     command=lambda i=item: self._confirmar_delete(i)).pack(side="left", expand=True, fill="x", padx=(4, 0))

    def _confirmar_delete(self, item):
        dialog = ctk.CTkToplevel(self)
        dialog.title("")
        dialog.geometry("360x180")
        dialog.configure(fg_color=BG_CARD)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Deletar assunto?", font=ctk.CTkFont(size=16, weight="bold"), text_color=COR_TEXTO).pack(pady=(24, 8))
        ctk.CTkLabel(dialog, text=f'"{item["assunto"]}" será removido.', font=ctk.CTkFont(size=12), text_color=COR_MUTED).pack()

        btns = ctk.CTkFrame(dialog, fg_color="transparent")
        btns.pack(pady=20)
        ctk.CTkButton(btns, text="Cancelar", fg_color="#2d1b4e", width=120, command=dialog.destroy).pack(side="left", padx=8)
        ctk.CTkButton(btns, text="Deletar", fg_color="#4c0519", width=120, command=lambda: self._deletar(item["id"], dialog)).pack(side="left", padx=8)

    def _deletar(self, item_id, dialog):
        dialog.destroy()
        deletar_item(item_id)
        self._renderizar_cards()

    def _abrir_edicao(self, item):
        dialog = ctk.CTkToplevel(self)
        dialog.title("")
        dialog.geometry("480x560")
        dialog.configure(fg_color=BG_CARD)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Editar Assunto", font=ctk.CTkFont(size=18, weight="bold"), text_color=COR_TEXTO).pack(pady=(24, 20))
        inner = ctk.CTkFrame(dialog, fg_color="transparent")
        inner.pack(fill="x", padx=28)

        # Matéria
        ctk.CTkLabel(inner, text="Matéria", font=ctk.CTkFont(size=12), text_color=COR_MUTED).pack(anchor="w")
        entry_mat = ctk.CTkEntry(inner, height=40, fg_color=BG_ITEM, border_color="#2d1b4e", text_color=COR_TEXTO, corner_radius=10)
        entry_mat.pack(fill="x", pady=(4, 12))
        entry_mat.insert(0, item["materia"])

        # Assunto
        ctk.CTkLabel(inner, text="Assunto", font=ctk.CTkFont(size=12), text_color=COR_MUTED).pack(anchor="w")
        entry_ass = ctk.CTkEntry(inner, height=40, fg_color=BG_ITEM, border_color="#2d1b4e", text_color=COR_TEXTO, corner_radius=10)
        entry_ass.pack(fill="x", pady=(4, 12))
        entry_ass.insert(0, item["assunto"])

        # Anotação
        ctk.CTkLabel(inner, text="Anotação", font=ctk.CTkFont(size=12), text_color=COR_MUTED).pack(anchor="w")
        entry_anot = ctk.CTkTextbox(inner, height=80, fg_color=BG_ITEM, border_color="#2d1b4e", text_color=COR_TEXTO, corner_radius=10)
        entry_anot.pack(fill="x", pady=(4, 16))
        entry_anot.insert("1.0", item.get("anotacao", ""))

        # Categoria
        cat_var = ctk.StringVar(value=item.get("categoria", "semestre"))
        cat_frame = ctk.CTkFrame(inner, fg_color=BG_ITEM, corner_radius=10)
        cat_frame.pack(fill="x", pady=(0, 12))

        btn_sem = ctk.CTkButton(cat_frame, text="Semestre", corner_radius=8, height=34,
                               fg_color=COR_ROXA if cat_var.get() == "semestre" else "transparent")
        btn_sem.pack(side="left", expand=True, fill="x", padx=4, pady=4)

        btn_auto = ctk.CTkButton(cat_frame, text="Auto-Estudo", corner_radius=8, height=34,
                                fg_color=COR_MAGENTA if cat_var.get() == "auto-estudo" else "transparent")
        btn_auto.pack(side="left", expand=True, fill="x", padx=4, pady=4)

        def mudar_cat(c):
            cat_var.set(c)
            btn_sem.configure(fg_color=COR_ROXA if c == "semestre" else "transparent")
            btn_auto.configure(fg_color=COR_MAGENTA if c == "auto-estudo" else "transparent")

        btn_sem.configure(command=lambda: mudar_cat("semestre"))
        btn_auto.configure(command=lambda: mudar_cat("auto-estudo"))

        # Semestre Menu
        sem_var = ctk.StringVar(value=f"{item.get('semestre', 1)}º semestre")
        semestres = [f"{i}º semestre" for i in range(1, 9)]
        ctk.CTkOptionMenu(inner, values=semestres, variable=sem_var, fg_color=BG_ITEM, button_color=COR_ROXA, corner_radius=10, height=40).pack(fill="x", pady=(0, 16))

        def salvar():
            # AQUI: Criamos o dicionário de atualização conforme o repositório espera
            novos_dados = {
                "materia": entry_mat.get().strip(),
                "assunto": entry_ass.get().strip(),
                "categoria": cat_var.get(),
                "semestre": int(sem_var.get()[0]) if cat_var.get() == "semestre" else None,
                "anotacao": entry_anot.get("1.0", "end").strip()
            }
            editar_item(item["id"], novos_dados) # Chamada corrigida para o formato do repositório
            dialog.destroy()
            self._renderizar_cards()

        ctk.CTkButton(inner, text="Salvar Alterações", fg_color=COR_ROXA, hover_color="#6d28d9", corner_radius=12, height=44, font=ctk.CTkFont(weight="bold"), command=salvar).pack(fill="x")