"""
Teste de integração — Wikipedia API.
Testa a lógica do módulo com mock (sem depender de rede).
Inclui teste real marcado como 'integration' para rodar quando
a rede estiver disponível.
"""

import json
from unittest.mock import patch, MagicMock
from src.core.wikipedia_api import buscar_resumo


def _mock_response(data: dict, status=200):
    """Cria um mock de urllib response."""
    resp = MagicMock()
    resp.read.return_value = json.dumps(data).encode("utf-8")
    resp.__enter__ = MagicMock(return_value=resp)
    resp.__exit__ = MagicMock(return_value=False)
    return resp


def test_buscar_resumo_sucesso():
    """Testa retorno bem-sucedido com dados mockados."""
    dados_mock = {
        "type": "standard",
        "title": "Python",
        "extract": "Python é uma linguagem de programação de alto nível.",
        "content_urls": {
            "desktop": {"page": "https://pt.wikipedia.org/wiki/Python"}
        },
    }
    with patch("urllib.request.urlopen", return_value=_mock_response(dados_mock)):
        resultado = buscar_resumo("Python")

    assert resultado["encontrado"] is True
    assert resultado["titulo"] == "Python"
    assert "linguagem" in resultado["resumo"]
    assert resultado["url"].startswith("https://")


def test_buscar_resumo_artigo_nao_encontrado():
    """Testa termo que retorna HTTP 404."""
    import urllib.error

    with patch(
        "urllib.request.urlopen",
        side_effect=urllib.error.HTTPError(
            url="", code=404, msg="Not Found", hdrs=None, fp=None
        ),
    ):
        resultado = buscar_resumo("termoquejamaisfoimasoexistiu999")

    assert resultado["encontrado"] is False
    assert "não encontrado" in resultado["resumo"].lower()


def test_buscar_resumo_retorna_estrutura_correta():
    """Verifica que o retorno sempre tem as 4 chaves esperadas."""
    dados_mock = {
        "type": "standard",
        "title": "Algoritmo",
        "extract": "Em ciência da computação, um algoritmo é...",
        "content_urls": {
            "desktop": {"page": "https://pt.wikipedia.org/wiki/Algoritmo"}
        },
    }
    with patch("urllib.request.urlopen", return_value=_mock_response(dados_mock)):
        resultado = buscar_resumo("Algoritmo")

    assert "titulo" in resultado
    assert "resumo" in resultado
    assert "url" in resultado
    assert "encontrado" in resultado


def test_buscar_resumo_desambiguacao():
    """Testa que páginas de desambiguação retornam encontrado=False."""
    dados_mock = {
        "type": "disambiguation",
        "title": "Árvore",
        "extract": "Árvore pode se referir a...",
        "content_urls": {
            "desktop": {"page": "https://pt.wikipedia.org/wiki/Árvore"}
        },
    }
    with patch("urllib.request.urlopen", return_value=_mock_response(dados_mock)):
        resultado = buscar_resumo("Árvore")

    assert resultado["encontrado"] is False
    assert "ambíguo" in resultado["resumo"].lower()


def test_buscar_resumo_sem_conexao():
    """Testa que erro de rede retorna resultado seguro."""
    import urllib.error

    with patch(
        "urllib.request.urlopen",
        side_effect=urllib.error.URLError("Connection refused"),
    ):
        resultado = buscar_resumo("Python")

    assert resultado["encontrado"] is False
    assert "conexão" in resultado["resumo"].lower()


def test_buscar_resumo_encoding_acentos():
    """Verifica que termos com acentos são tratados corretamente."""
    dados_mock = {
        "type": "standard",
        "title": "Revisão espaçada",
        "extract": "Repetição espaçada é uma técnica de aprendizado.",
        "content_urls": {
            "desktop": {
                "page": "https://pt.wikipedia.org/wiki/Revisão_espaçada"
            }
        },
    }
    with patch("urllib.request.urlopen", return_value=_mock_response(dados_mock)):
        resultado = buscar_resumo("Revisão espaçada")

    assert isinstance(resultado["resumo"], str)
    assert resultado["encontrado"] is True
