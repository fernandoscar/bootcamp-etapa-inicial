"""
Testes das APIs externas — clima, imagens, GitHub, feriados, países.
Todos usam mocks para não depender de rede.
"""

import json
from unittest.mock import patch, MagicMock
from src.core.apis_externas import (
    buscar_clima,
    buscar_imagem,
    buscar_perfil_github,
    buscar_repos_github,
    buscar_feriados,
    proximo_feriado,
    buscar_pais,
)


def _mock_response(data):
    resp = MagicMock()
    resp.read.return_value = json.dumps(data).encode("utf-8")
    resp.__enter__ = MagicMock(return_value=resp)
    resp.__exit__ = MagicMock(return_value=False)
    return resp


# ── Clima ──

def test_clima_sucesso():
    dados = {
        "current": {"temperature_2m": 25.3, "weather_code": 2}
    }
    with patch("urllib.request.urlopen", return_value=_mock_response(dados)):
        r = buscar_clima()
    assert r["encontrado"] is True
    assert r["temperatura"] == 25.3
    assert r["descricao"] == "Parcialmente nublado"
    assert r["icone"] == "⛅"


def test_clima_erro_rede():
    import urllib.error
    with patch(
        "urllib.request.urlopen",
        side_effect=urllib.error.URLError("fail"),
    ):
        r = buscar_clima()
    assert r["encontrado"] is False
    assert r["temperatura"] is None


# ── Imagens (Unsplash) ──

def test_imagem_retorna_url():
    r = buscar_imagem("algoritmo")
    assert r["encontrado"] is True
    assert "unsplash" in r["url"]
    assert "algoritmo" in r["url"]


def test_imagem_dimensoes_custom():
    r = buscar_imagem("python", largura=800, altura=600)
    assert "800x600" in r["url"]


# ── GitHub ──

def test_github_perfil_sucesso():
    dados = {
        "login": "fernandoscar",
        "name": "Fernando",
        "avatar_url": "https://avatar.com/foto.jpg",
        "public_repos": 8,
        "bio": "Estudante de ES",
        "html_url": "https://github.com/fernandoscar",
    }
    with patch("urllib.request.urlopen", return_value=_mock_response(dados)):
        r = buscar_perfil_github("fernandoscar")
    assert r["encontrado"] is True
    assert r["nome"] == "Fernando"
    assert r["repos_publicos"] == 8


def test_github_perfil_inexistente():
    import urllib.error
    with patch(
        "urllib.request.urlopen",
        side_effect=urllib.error.HTTPError("", 404, "", None, None),
    ):
        r = buscar_perfil_github("usuario_que_nao_existe_xyz")
    assert r["encontrado"] is False


def test_github_repos_sucesso():
    dados = [
        {
            "name": "pipostudy",
            "description": "App de revisão",
            "language": "Python",
            "html_url": "https://github.com/x/pipostudy",
            "stargazers_count": 2,
        },
        {
            "name": "site-pessoal",
            "description": None,
            "language": "HTML",
            "html_url": "https://github.com/x/site",
            "stargazers_count": 0,
        },
    ]
    with patch("urllib.request.urlopen", return_value=_mock_response(dados)):
        r = buscar_repos_github("fernandoscar", limite=2)
    assert len(r) == 2
    assert r[0]["nome"] == "pipostudy"
    assert r[0]["linguagem"] == "Python"


def test_github_repos_erro():
    import urllib.error
    with patch(
        "urllib.request.urlopen",
        side_effect=urllib.error.URLError("fail"),
    ):
        r = buscar_repos_github("x")
    assert r == []


# ── Feriados ──

def test_feriados_sucesso():
    dados = [
        {"date": "2026-01-01", "localName": "Ano Novo", "fixed": True},
        {"date": "2026-04-21", "localName": "Tiradentes", "fixed": True},
    ]
    with patch("urllib.request.urlopen", return_value=_mock_response(dados)):
        r = buscar_feriados(2026)
    assert len(r) == 2
    assert r[0]["nome"] == "Ano Novo"
    assert r[0]["data"] == "2026-01-01"


def test_feriados_erro():
    import urllib.error
    with patch(
        "urllib.request.urlopen",
        side_effect=urllib.error.URLError("fail"),
    ):
        r = buscar_feriados(2026)
    assert r == []


def test_proximo_feriado_encontra():
    dados = [
        {"date": "2020-01-01", "localName": "Passado", "fixed": True},
        {"date": "2099-12-25", "localName": "Natal Futuro", "fixed": True},
    ]
    with patch("urllib.request.urlopen", return_value=_mock_response(dados)):
        r = proximo_feriado()
    assert r is not None
    assert r["nome"] == "Natal Futuro"
    assert r["dias_restantes"] > 0


def test_proximo_feriado_nenhum():
    dados = [
        {"date": "2020-01-01", "localName": "Passado", "fixed": True},
    ]
    with patch("urllib.request.urlopen", return_value=_mock_response(dados)):
        r = proximo_feriado()
    assert r is None


# ── Países ──

def test_pais_sucesso():
    dados = [
        {
            "name": {"common": "France"},
            "capital": ["Paris"],
            "population": 67390000,
            "flag": "🇫🇷",
            "flags": {"png": "https://flags.com/fr.png"},
            "region": "Europe",
            "languages": {"fra": "French"},
        }
    ]
    with patch("urllib.request.urlopen", return_value=_mock_response(dados)):
        r = buscar_pais("França")
    assert r["encontrado"] is True
    assert r["nome"] == "France"
    assert r["capital"] == "Paris"
    assert r["bandeira_emoji"] == "🇫🇷"
    assert r["idiomas"] == ["French"]


def test_pais_inexistente():
    import urllib.error
    with patch(
        "urllib.request.urlopen",
        side_effect=urllib.error.HTTPError("", 404, "", None, None),
    ):
        r = buscar_pais("PaisQueNaoExiste")
    assert r["encontrado"] is False
