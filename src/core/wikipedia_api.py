"""
Integração com a API pública da Wikipedia (pt.wikipedia.org).
Busca um resumo do assunto cadastrado para enriquecer as anotações.
"""

import urllib.request
import urllib.parse
import json


API_URL = "https://pt.wikipedia.org/api/rest_v1/page/summary/{titulo}"


def buscar_resumo(termo: str) -> dict:
    """
    Busca o resumo de um termo na Wikipedia em português.

    Retorna um dicionário com:
        - "titulo": título do artigo encontrado
        - "resumo": texto resumido (extract)
        - "url": link para o artigo completo
        - "encontrado": True/False

    Usa apenas urllib (sem dependências externas).
    """
    titulo_codificado = urllib.parse.quote(termo, safe="")
    url = API_URL.format(titulo=titulo_codificado)

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "PipoStudy/1.0 (estudante; revisao-espacada)"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            dados = json.loads(resp.read().decode("utf-8"))

        if dados.get("type") == "disambiguation":
            return {
                "titulo": dados.get("title", termo),
                "resumo": "Termo ambíguo — tente ser mais específico.",
                "url": dados.get("content_urls", {}).get("desktop", {}).get("page", ""),
                "encontrado": False,
            }

        return {
            "titulo": dados.get("title", termo),
            "resumo": dados.get("extract", "Sem resumo disponível."),
            "url": (
                dados.get("content_urls", {})
                .get("desktop", {})
                .get("page", "")
            ),
            "encontrado": True,
        }

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {
                "titulo": termo,
                "resumo": "Artigo não encontrado na Wikipedia.",
                "url": "",
                "encontrado": False,
            }
        return {
            "titulo": termo,
            "resumo": f"Erro ao consultar Wikipedia (HTTP {e.code}).",
            "url": "",
            "encontrado": False,
        }

    except (urllib.error.URLError, TimeoutError, OSError):
        return {
            "titulo": termo,
            "resumo": "Sem conexão com a Wikipedia.",
            "url": "",
            "encontrado": False,
        }
