# --- PALETA CENTRALIZADA COM SUPORTE A TEMA ---
# Toda cor da aplicação vive aqui.
# Dois modos: "light" (claro) e "dark" (escuro).

_TEMA_ATUAL = "light"

TEMAS = {
    "light": {
        "BG": "#f8f5ff",
        "BG_SIDEBAR": "#ffffff",
        "BG_CARD": "#ffffff",
        "BG_ITEM": "#faf8ff",
        "BG_ATIVO": "#ede9fe",
        "BG_INPUT": "#faf8ff",
        "BORDER": "#f0eaf9",
        "BORDER_HOVER": "#e0d5f5",
        "COR_TEXTO": "#1e1233",
        "COR_MUTED": "#9b7fc0",
        "COR_ROXA": "#7c3aed",
        "COR_ROXA_HOVER": "#6d28d9",
        "COR_MAGENTA": "#db2777",
        "COR_VERDE": "#10b981",
        "COR_VERDE_ALT": "#0f6e56",
        "COR_VERMELHA": "#ef4444",
        "COR_VERMELHO": "#dc2626",
        "COR_AMARELO": "#f59e0b",
        "COR_AZUL": "#3b82f6",
        "BG_VERDE": "#e0f5ee",
        "BG_VERDE_ESCURO": "#e0f5ee",
        "BG_VERMELHO": "#fde8e8",
        "BG_VERMELHO_ESCURO": "#fde8e8",
        "BG_AMARELO": "#fef3e2",
        "BG_ALERTA": "#fde8e8",
        "BG_AZUL": "#e8f0fe",
        "ICON_PURPLE_BG": "#ede9fe",
        "ICON_RED_BG": "#fde8e8",
        "ICON_BLUE_BG": "#e8f0fe",
        "ICON_AMBER_BG": "#fef3e2",
        "ICON_TEAL_BG": "#e0f5ee",
        "ICON_PINK_BG": "#fce8f3",
    },
    "dark": {
        "BG": "#0d0b14",
        "BG_SIDEBAR": "#0a0812",
        "BG_CARD": "#12101a",
        "BG_ITEM": "#1a1025",
        "BG_ATIVO": "#2d1b4e",
        "BG_INPUT": "#1a1025",
        "BORDER": "rgba(124,58,237,0.1)",
        "BORDER_HOVER": "rgba(124,58,237,0.25)",
        "COR_TEXTO": "#e8d5ff",
        "COR_MUTED": "#9b7fc0",
        "COR_ROXA": "#7c3aed",
        "COR_ROXA_HOVER": "#6d28d9",
        "COR_MAGENTA": "#db2777",
        "COR_VERDE": "#10b981",
        "COR_VERDE_ALT": "#34d399",
        "COR_VERMELHA": "#ef4444",
        "COR_VERMELHO": "#f87171",
        "COR_AMARELO": "#fbbf24",
        "COR_AZUL": "#60a5fa",
        "BG_VERDE": "#064e3b",
        "BG_VERDE_ESCURO": "#064e3b",
        "BG_VERMELHO": "#3b1111",
        "BG_VERMELHO_ESCURO": "#3b1111",
        "BG_AMARELO": "#3b2506",
        "BG_ALERTA": "#3b1111",
        "BG_AZUL": "#172554",
        "ICON_PURPLE_BG": "#2d1b4e",
        "ICON_RED_BG": "#3b1111",
        "ICON_BLUE_BG": "#172554",
        "ICON_AMBER_BG": "#3b2506",
        "ICON_TEAL_BG": "#064e3b",
        "ICON_PINK_BG": "#4c0519",
    },
}

# --- Atalhos de acesso rápido ---
# Cada variável aponta pro valor do tema atual.
# Ao trocar tema, chame `aplicar_tema()`.

_t = TEMAS[_TEMA_ATUAL]

BG = _t["BG"]
BG_SIDEBAR = _t["BG_SIDEBAR"]
BG_CARD = _t["BG_CARD"]
BG_ITEM = _t["BG_ITEM"]
BG_ATIVO = _t["BG_ATIVO"]
BG_INPUT = _t["BG_INPUT"]
BORDER = _t["BORDER"]
COR_TEXTO = _t["COR_TEXTO"]
COR_MUTED = _t["COR_MUTED"]
COR_ROXA = _t["COR_ROXA"]
COR_ROXA_HOVER = _t["COR_ROXA_HOVER"]
COR_MAGENTA = _t["COR_MAGENTA"]
COR_VERDE = _t["COR_VERDE"]
COR_VERDE_ALT = _t["COR_VERDE_ALT"]
COR_VERMELHA = _t["COR_VERMELHA"]
COR_VERMELHO = _t["COR_VERMELHO"]
COR_AMARELO = _t["COR_AMARELO"]
COR_AZUL = _t["COR_AZUL"]
BG_VERDE = _t["BG_VERDE"]
BG_VERDE_ESCURO = _t["BG_VERDE_ESCURO"]
BG_VERMELHO = _t["BG_VERMELHO"]
BG_VERMELHO_ESCURO = _t["BG_VERMELHO_ESCURO"]
BG_AMARELO = _t["BG_AMARELO"]
BG_ALERTA = _t["BG_ALERTA"]


def get(chave: str) -> str:
    """Retorna uma cor do tema atual pelo nome."""
    return TEMAS[_TEMA_ATUAL][chave]


def tema_atual() -> str:
    """Retorna o nome do tema ativo ('light' ou 'dark')."""
    return _TEMA_ATUAL


def set_tema(nome: str) -> None:
    """Troca o tema atual. Atualiza os atalhos globais."""
    global _TEMA_ATUAL
    global BG, BG_SIDEBAR, BG_CARD, BG_ITEM, BG_ATIVO, BG_INPUT
    global BORDER, COR_TEXTO, COR_MUTED
    global COR_ROXA, COR_ROXA_HOVER, COR_MAGENTA
    global COR_VERDE, COR_VERDE_ALT, COR_VERMELHA, COR_VERMELHO
    global COR_AMARELO, COR_AZUL
    global BG_VERDE, BG_VERDE_ESCURO, BG_VERMELHO, BG_VERMELHO_ESCURO
    global BG_AMARELO, BG_ALERTA

    _TEMA_ATUAL = nome
    _t = TEMAS[nome]

    BG = _t["BG"]
    BG_SIDEBAR = _t["BG_SIDEBAR"]
    BG_CARD = _t["BG_CARD"]
    BG_ITEM = _t["BG_ITEM"]
    BG_ATIVO = _t["BG_ATIVO"]
    BG_INPUT = _t["BG_INPUT"]
    BORDER = _t["BORDER"]
    COR_TEXTO = _t["COR_TEXTO"]
    COR_MUTED = _t["COR_MUTED"]
    COR_ROXA = _t["COR_ROXA"]
    COR_ROXA_HOVER = _t["COR_ROXA_HOVER"]
    COR_MAGENTA = _t["COR_MAGENTA"]
    COR_VERDE = _t["COR_VERDE"]
    COR_VERDE_ALT = _t["COR_VERDE_ALT"]
    COR_VERMELHA = _t["COR_VERMELHA"]
    COR_VERMELHO = _t["COR_VERMELHO"]
    COR_AMARELO = _t["COR_AMARELO"]
    COR_AZUL = _t["COR_AZUL"]
    BG_VERDE = _t["BG_VERDE"]
    BG_VERDE_ESCURO = _t["BG_VERDE_ESCURO"]
    BG_VERMELHO = _t["BG_VERMELHO"]
    BG_VERMELHO_ESCURO = _t["BG_VERMELHO_ESCURO"]
    BG_AMARELO = _t["BG_AMARELO"]
    BG_ALERTA = _t["BG_ALERTA"]
