import json
import os
from datetime import date
from pathlib import Path

# Caminho padrão relativo à raiz do projeto, não ao diretório de execução.
_RAIZ_PROJETO = Path(__file__).resolve().parent.parent.parent
ARQUIVO_PADRAO = str(_RAIZ_PROJETO / "dados.json")


def carregar_dados(caminho: str = ARQUIVO_PADRAO) -> list[dict]:
    """Lê o ficheiro JSON e retorna uma lista de dicionários."""
    if not os.path.exists(caminho):
        return []
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError:
        return []


def salvar_dados(itens: list[dict], caminho: str = ARQUIVO_PADRAO) -> None:
    """Guarda a lista de itens no ficheiro JSON."""
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(itens, arquivo, indent=4, ensure_ascii=False)


def adicionar_item(
    materia_ou_dict, assunto=None, caminho: str = ARQUIVO_PADRAO
) -> None:
    """
    Guarda um novo assunto.
    Aceita um dicionário (UI) ou matéria + assunto separados (testes).
    """
    itens = carregar_dados(caminho)

    if assunto is not None:
        novo_item = {
            "id": len(itens) + 1,
            "materia": materia_ou_dict,
            "assunto": assunto,
            "data_agendada": str(date.today()),
            "indice_intervalo": 0,
            "total_revisoes": 0,
            "status": "Pendente",
        }
        itens.append(novo_item)
    else:
        itens.append(materia_ou_dict)

    salvar_dados(itens, caminho)


def atualizar_item(
    id_item, nova_data: str, novo_indice: int, status: str,
    caminho: str = ARQUIVO_PADRAO,
) -> None:
    """Atualiza as informações de revisão de um item."""
    itens = carregar_dados(caminho)
    for item in itens:
        if str(item.get("id")) == str(id_item):
            item["data_agendada"] = nova_data
            item["indice_intervalo"] = novo_indice
            item["status"] = status
            item["total_revisoes"] = item.get("total_revisoes", 0) + 1
            break
    salvar_dados(itens, caminho)


def deletar_item(id_item, caminho: str = ARQUIVO_PADRAO) -> None:
    """Remove um item pelo ID."""
    itens = carregar_dados(caminho)
    itens_filtrados = [i for i in itens if str(i.get("id")) != str(id_item)]
    salvar_dados(itens_filtrados, caminho)


def editar_item(id_item, novos_dados: dict, caminho: str = ARQUIVO_PADRAO) -> None:
    """Atualiza um item com novos dados."""
    itens = carregar_dados(caminho)
    for item in itens:
        if str(item.get("id")) == str(id_item):
            item.update(novos_dados)
            break
    salvar_dados(itens, caminho)


def get_atividade_semanal(caminho: str = ARQUIVO_PADRAO) -> list[int]:
    """Retorna dados para o gráfico do Dashboard."""
    return [0, 0, 0, 0, 0, 0, 0]
