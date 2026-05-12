"""
Módulo de APIs externas do PipoStudy.
Todas as integrações usam apenas urllib (sem dependências externas).
Cada função retorna um dicionário seguro — nunca levanta exceção.
"""

import urllib.request
import urllib.parse
import json

_HEADERS = {"User-Agent": "PipoStudy/1.0 (estudante; revisao-espacada)"}
_TIMEOUT = 5


def _get_json(url: str) -> dict | list | None:
    """Faz GET e retorna JSON parseado, ou None em caso de erro."""
    try:
        req = urllib.request.Request(url, headers=_HEADERS)
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


# ──────────────────────────────────────────────
# 1. CLIMA — Open-Meteo (grátis, sem API key)
# ──────────────────────────────────────────────

def buscar_clima(lat: float = -15.79, lon: float = -47.88) -> dict:
    """
    Retorna clima atual para as coordenadas dadas.
    Padrão: Brasília (-15.79, -47.88).

    Retorno:
        {
            "temperatura": 25.3,
            "descricao": "Parcialmente nublado",
            "icone": "⛅",
            "encontrado": True
        }
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,weather_code"
        f"&timezone=America%2FSao_Paulo"
    )
    dados = _get_json(url)
    if not dados or "current" not in dados:
        return {
            "temperatura": None,
            "descricao": "Indisponível",
            "icone": "❓",
            "encontrado": False,
        }

    current = dados["current"]
    temp = current.get("temperature_2m")
    code = current.get("weather_code", -1)

    # WMO Weather interpretation codes
    descricoes = {
        0: ("Céu limpo", "☀️"),
        1: ("Quase limpo", "🌤"),
        2: ("Parcialmente nublado", "⛅"),
        3: ("Nublado", "☁️"),
        45: ("Neblina", "🌫"),
        48: ("Neblina com geada", "🌫"),
        51: ("Garoa leve", "🌦"),
        53: ("Garoa", "🌦"),
        55: ("Garoa forte", "🌧"),
        61: ("Chuva leve", "🌦"),
        63: ("Chuva", "🌧"),
        65: ("Chuva forte", "🌧"),
        71: ("Neve leve", "🌨"),
        73: ("Neve", "❄️"),
        75: ("Neve forte", "❄️"),
        80: ("Pancadas leves", "🌦"),
        81: ("Pancadas", "🌧"),
        82: ("Pancadas fortes", "⛈"),
        95: ("Tempestade", "⛈"),
        96: ("Tempestade com granizo", "⛈"),
        99: ("Tempestade severa", "⛈"),
    }
    desc, icone = descricoes.get(code, ("Indefinido", "🌡"))

    return {
        "temperatura": temp,
        "descricao": desc,
        "icone": icone,
        "encontrado": True,
    }


# ──────────────────────────────────────────────
# 2. IMAGENS — Unsplash (grátis, sem API key via source)
# ──────────────────────────────────────────────

def buscar_imagem(termo: str, largura: int = 400, altura: int = 200) -> dict:
    """
    Retorna URL de uma imagem do Unsplash relacionada ao termo.
    Usa o endpoint source (redirect) que não precisa de API key.

    Retorno:
        {
            "url": "https://source.unsplash.com/400x200/?...",
            "termo": "algoritmo",
            "encontrado": True
        }
    """
    termo_codificado = urllib.parse.quote(termo)
    url = (
        f"https://source.unsplash.com/{largura}x{altura}"
        f"/?{termo_codificado},study,technology"
    )
    return {
        "url": url,
        "termo": termo,
        "encontrado": True,
    }


# ──────────────────────────────────────────────
# 4. GITHUB — Perfil público (grátis, sem auth)
# ──────────────────────────────────────────────

def buscar_perfil_github(username: str) -> dict:
    """
    Retorna dados públicos de um perfil GitHub.

    Retorno:
        {
            "nome": "Fernando",
            "avatar_url": "https://...",
            "repos_publicos": 12,
            "bio": "Estudante de ES",
            "url": "https://github.com/fernandoscar",
            "encontrado": True
        }
    """
    url = f"https://api.github.com/users/{urllib.parse.quote(username)}"
    dados = _get_json(url)
    if not dados or "login" not in dados:
        return {
            "nome": username,
            "avatar_url": "",
            "repos_publicos": 0,
            "bio": "",
            "url": f"https://github.com/{username}",
            "encontrado": False,
        }

    return {
        "nome": dados.get("name") or dados.get("login", username),
        "avatar_url": dados.get("avatar_url", ""),
        "repos_publicos": dados.get("public_repos", 0),
        "bio": dados.get("bio", "") or "",
        "url": dados.get("html_url", ""),
        "encontrado": True,
    }


def buscar_repos_github(username: str, limite: int = 5) -> list[dict]:
    """
    Retorna os repos públicos mais recentes de um usuário.

    Retorno: lista de dicts com nome, descricao, linguagem, url.
    """
    url = (
        f"https://api.github.com/users/{urllib.parse.quote(username)}"
        f"/repos?sort=updated&per_page={limite}"
    )
    dados = _get_json(url)
    if not dados or not isinstance(dados, list):
        return []

    return [
        {
            "nome": r.get("name", ""),
            "descricao": r.get("description", "") or "",
            "linguagem": r.get("language", "") or "",
            "url": r.get("html_url", ""),
            "estrelas": r.get("stargazers_count", 0),
        }
        for r in dados[:limite]
    ]


# ──────────────────────────────────────────────
# 5. FERIADOS — Nager.Date (grátis, sem API key)
# ──────────────────────────────────────────────

def buscar_feriados(ano: int = None, pais: str = "BR") -> list[dict]:
    """
    Retorna feriados nacionais do ano.

    Retorno: lista de dicts com data, nome, fixo.
    """
    from datetime import date as dt_date
    if ano is None:
        ano = dt_date.today().year

    url = f"https://date.nager.at/api/v3/PublicHolidays/{ano}/{pais}"
    dados = _get_json(url)
    if not dados or not isinstance(dados, list):
        return []

    return [
        {
            "data": f.get("date", ""),
            "nome": f.get("localName", f.get("name", "")),
            "fixo": f.get("fixed", False),
        }
        for f in dados
    ]


def proximo_feriado() -> dict | None:
    """Retorna o próximo feriado a partir de hoje, ou None."""
    from datetime import date as dt_date
    hoje = str(dt_date.today())
    feriados = buscar_feriados()
    for f in feriados:
        if f["data"] >= hoje:
            dias = (dt_date.fromisoformat(f["data"]) - dt_date.today()).days
            f["dias_restantes"] = dias
            f["texto"] = (
                f["nome"] if dias > 1
                else f"{f['nome']} (amanhã!)" if dias == 1
                else f"{f['nome']} (hoje!)"
            )
            return f
    return None


# ──────────────────────────────────────────────
# 8. PAÍSES — REST Countries (grátis, sem API key)
# ──────────────────────────────────────────────

def buscar_pais(nome: str) -> dict:
    """
    Busca informações de um país pelo nome.

    Retorno:
        {
            "nome": "França",
            "capital": "Paris",
            "populacao": 67390000,
            "bandeira_emoji": "🇫🇷",
            "bandeira_url": "https://...",
            "regiao": "Europe",
            "idiomas": ["French"],
            "encontrado": True
        }
    """
    termo = urllib.parse.quote(nome)
    campos = "name,capital,population,flag,flags,region,languages"
    url = f"https://restcountries.com/v3.1/name/{termo}?fields={campos}"
    dados = _get_json(url)
    if not dados or not isinstance(dados, list) or len(dados) == 0:
        return {
            "nome": nome,
            "capital": "",
            "populacao": 0,
            "bandeira_emoji": "",
            "bandeira_url": "",
            "regiao": "",
            "idiomas": [],
            "encontrado": False,
        }

    pais = dados[0]
    idiomas = list(pais.get("languages", {}).values()) if pais.get("languages") else []
    capitais = pais.get("capital", [])

    return {
        "nome": pais.get("name", {}).get("common", nome),
        "capital": capitais[0] if capitais else "",
        "populacao": pais.get("population", 0),
        "bandeira_emoji": pais.get("flag", ""),
        "bandeira_url": pais.get("flags", {}).get("png", ""),
        "regiao": pais.get("region", ""),
        "idiomas": idiomas,
        "encontrado": True,
    }
