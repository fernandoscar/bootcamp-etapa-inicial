import json
import os
from datetime import date

CAMINHO_DADOS = "dados.json"


def carregar_dados() -> list:
    """Lê o arquivo dados.json e retorna a lista de itens."""
    if not os.path.exists(CAMINHO_DADOS):
        return []
    with open(CAMINHO_DADOS, "r", encoding="utf-8") as f:
        conteudo = f.read().strip()
        if not conteudo:
            return []
        return json.loads(conteudo)


def salvar_dados(itens: list) -> None:
    """Salva a lista de itens no arquivo dados.json."""
    with open(CAMINHO_DADOS, "w", encoding="utf-8") as f:
        json.dump(itens, f, ensure_ascii=False, indent=2, default=str)


def adicionar_item(materia: str, assunto: str) -> None:
    """Cadastra um novo item no ciclo de revisão."""
    itens = carregar_dados()
    novo = {
        "id": len(itens) + 1,
        "materia": materia,
        "assunto": assunto,
        "indice_intervalo": 0,
        "data_agendada": str(date.today()),
        "status": "Pendente",
    }
    itens.append(novo)
    salvar_dados(itens)


def atualizar_item(item_id: int, nova_data: str, novo_indice: int, status: str) -> None:
    """Atualiza data, índice e status de um item após revisão."""
    itens = carregar_dados()
    for item in itens:
        if item["id"] == item_id:
            item["data_agendada"] = nova_data
            item["indice_intervalo"] = novo_indice
            item["status"] = status
            break
    salvar_dados(itens)
