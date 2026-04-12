import customtkinter as ctk
from src.core.repositorio import carregar_dados, get_atividade_semanal
from src.core.agendador import classificar_itens

# --- CONFIGURAÇÃO DE CORES ---
BG = "#0d0b14"
BG_CARD = "#1a1025"
BG_ITEM = "#2d1b4e"
COR_TEXTO = "#e8d5ff"
COR_MUTED = "#9b7fc0"
COR_ROXA = "#7c3aed"
COR_VERDE = "#10b981"
COR_VERMELHA = "#ef4444"

class Dashboard(ctk.CTkFrame):
    def __init__(self, master, on_revisar=None, on_cadastrar=None, **kwargs):
        super().__init__(master, fg_color=BG, corner_radius=0)
        
        self.on_revisar = on_revisar
        self.on_cadastrar = on_cadastrar
        
        # 1. CARREGAMENTO DE DADOS REAIS
        self.itens = carregar_dados()
        self.para_hoje, self.atrasados = classificar_itens(self.itens)
        self.fila_total = self.atrasados + self.para_hoje
        
        # 2. CONSTRUÇÃO DA INTERFACE
        self._criar_cabecalho()
        self._criar_cards_resumo()

        # Layout de Colunas
        self.conteudo_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.conteudo_frame.pack(fill="both", expand=True, padx=40, pady=(0, 24))

        self.coluna_esq = ctk.CTkFrame(self.conteudo_frame, fg_color="transparent")
        self.coluna_esq.pack(side="left", fill="both", expand=True, padx=(0, 16))

        self.coluna_dir = ctk.CTkFrame(self.conteudo_frame, fg_color="transparent", width=340)
        self.coluna_dir.pack(side="right", fill="y")
        self.coluna_dir.pack_propagate(False)

        # Preencher seções
        self._criar_secao_revisoes()
        self._criar_grafico_atividade()
        self._criar_proximas_revisoes()

    def _criar_cabecalho(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(32, 24))
        ctk.CTkLabel(header, text="Boa tarde! 👋", font=ctk.CTkFont(size=28, weight="bold"), text_color=COR_TEXTO).pack(anchor="w")
        ctk.CTkLabel(header, text="domingo, 12 de abril de 2026", font=ctk.CTkFont(size=14), text_color=COR_MUTED).pack(anchor="w")

    def _criar_cards_resumo(self):
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="x", padx=40, pady=(0, 24))
        
        # Valores dinâmicos baseados no que existe no JSON
        self._criar_card(cards_frame, str(len(self.para_hoje)), "Para Hoje", "📅")
        self._criar_card(cards_frame, str(len(self.atrasados)), "Atrasadas", "⏰")
        self._criar_card(cards_frame, str(len(self.itens)), "Total", "📖")
        self._criar_card(cards_frame, "0d", "Sequência", "🔥")

    def _criar_card(self, parent, valor, titulo, icone):
        card = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=16, height=100)
        card.pack(side="left", expand=True, fill="both", padx=(0, 16))
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=icone, font=ctk.CTkFont(size=18)).pack(anchor="w", padx=20, pady=(16, 5))
        ctk.CTkLabel(card, text=valor, font=ctk.CTkFont(size=24, weight="bold"), text_color=COR_TEXTO).pack(anchor="w", padx=20)
        ctk.CTkLabel(card, text=titulo, font=ctk.CTkFont(size=12), text_color=COR_MUTED).pack(anchor="w", padx=20, pady=(0, 16))

    def _criar_secao_revisoes(self):
        """Esta seção agora é totalmente dinâmica."""
        card_fila = ctk.CTkFrame(self.coluna_esq, fg_color=BG_CARD, corner_radius=16)
        card_fila.pack(fill="both", expand=True)

        header = ctk.CTkFrame(card_fila, fg_color="transparent")
        header.pack(fill="x", padx=24, pady=24)
        ctk.CTkLabel(header, text="Revisões Pendentes", font=ctk.CTkFont(size=16, weight="bold"), text_color=COR_TEXTO).pack(side="left")
        
        self.lista_container = ctk.CTkFrame(card_fila, fg_color="transparent")
        self.lista_container.pack(fill="both", expand=True)

        # VERIFICAÇÃO DE DADOS REAIS
        if not self.fila_total:
            # Estado Vazio: Nada no JSON = Nada na tela
            ctk.CTkLabel(self.lista_container, text="Nenhum assunto para revisar agora. ✨", 
                         font=ctk.CTkFont(size=14), text_color=COR_MUTED).pack(expand=True)
        else:
            # Se existirem dados, percorre a lista real do utilizador
            for item in self.fila_total[:5]: # Mostra os primeiros 5
                status = "atrasada" if item in self.atrasados else "hoje"
                cor_status = COR_VERMELHA if status == "atrasada" else COR_VERDE
                bg_status = "#7f1d1d" if status == "atrasada" else "#064e3b"
                
                self._criar_linha_assunto(
                    self.lista_container, 
                    item.get("assunto", "Sem título"), 
                    item.get("materia", "Geral"), 
                    status, cor_status, bg_status
                )

        # Botão de ação
        btn_text = f"Começar Revisão ({len(self.fila_total)})"
        self.btn_revisar = ctk.CTkButton(
            card_fila, text=btn_text, font=ctk.CTkFont(size=14, weight="bold"), 
            fg_color=COR_ROXA, height=48, corner_radius=12,
            command=self.on_revisar,
            state="normal" if self.fila_total else "disabled" # Botão só ativa se houver dados
        )
        self.btn_revisar.pack(fill="x", padx=24, pady=24, side="bottom")

    def _criar_linha_assunto(self, parent, titulo, materia, status_txt, cor_txt, cor_bg):
        linha = ctk.CTkFrame(parent, fg_color="transparent")
        linha.pack(fill="x", padx=24, pady=(0, 15))
        
        ctk.CTkLabel(linha, text="●", text_color=COR_ROXA).pack(side="left", padx=(0, 10))
        
        textos = ctk.CTkFrame(linha, fg_color="transparent")
        textos.pack(side="left")
        ctk.CTkLabel(textos, text=titulo, font=ctk.CTkFont(size=13, weight="bold"), text_color=COR_TEXTO).pack(anchor="w")
        ctk.CTkLabel(textos, text=materia, font=ctk.CTkFont(size=11), text_color=COR_MUTED).pack(anchor="w")

        ctk.CTkLabel(linha, text=status_txt, font=ctk.CTkFont(size=10, weight="bold"), 
                     text_color=cor_txt, fg_color=cor_bg, corner_radius=6, padx=8).pack(side="right")

    def _criar_grafico_atividade(self):
        card = ctk.CTkFrame(self.coluna_dir, fg_color=BG_CARD, corner_radius=16, height=180)
        card.pack(fill="x", pady=(0, 16))
        card.pack_propagate(False)
        ctk.CTkLabel(card, text="📈 Atividade semanal", font=ctk.CTkFont(size=12), text_color=COR_TEXTO).pack(anchor="w", padx=20, pady=15)
        
        # Gráfico dinâmico (por enquanto mostra valores base do sistema)
        barras_frame = ctk.CTkFrame(card, fg_color="transparent")
        barras_frame.pack(fill="both", expand=True, padx=20)
        dias = ["S", "T", "Q", "Q", "S", "S", "D"]
        for dia in dias:
            col = ctk.CTkFrame(barras_frame, fg_color="transparent")
            col.pack(side="left", expand=True, fill="y")
            ctk.CTkFrame(col, fg_color=COR_ROXA, width=6, height=8, corner_radius=3).pack(side="bottom", pady=5)
            ctk.CTkLabel(col, text=dia, font=ctk.CTkFont(size=9), text_color=COR_MUTED).pack(side="bottom")

    def _criar_proximas_revisoes(self):
        card = ctk.CTkFrame(self.coluna_dir, fg_color=BG_CARD, corner_radius=16)
        card.pack(fill="both", expand=True)
        ctk.CTkLabel(card, text="Próximas Revisões", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO).pack(anchor="w", padx=20, pady=15)
        
        # Mostra apenas o que não é para hoje nem está atrasado
        proximos = [i for i in self.itens if i not in self.fila_total]
        if not proximos:
            ctk.CTkLabel(card, text="Sem agendamentos futuros.", font=ctk.CTkFont(size=11), text_color=COR_MUTED).pack(pady=10)
        else:
            for item in proximos[:3]:
                f = ctk.CTkFrame(card, fg_color="transparent")
                f.pack(fill="x", padx=20, pady=5)
                ctk.CTkLabel(f, text=f"● {item.get('assunto','')[:18]}...", font=ctk.CTkFont(size=11), text_color=COR_TEXTO).pack(side="left")