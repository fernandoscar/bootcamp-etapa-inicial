import json
import os
import uuid
from datetime import date

ARQUIVO_DADOS = "dados.json"


def carregar_dados():
    """Lê o ficheiro JSON e converte para uma lista de dicionários."""
    if not os.path.exists(ARQUIVO_DADOS):
        return []
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError:
        return []


def salvar_dados(itens):
    """Guarda a lista de itens no ficheiro JSON."""
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(itens, arquivo, indent=4, ensure_ascii=False)


def adicionar_item(materia_ou_dict, assunto=None):
    """
    Guarda um novo assunto. Aceita um dicionário (UI)
    ou matéria e assunto separados (Testes).
    """
    itens = carregar_dados()

    if assunto is not None:
        # Se veio dos testes, usamos um ID numérico (1, 2, 3...)
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
        # Se veio da UI, usamos o dicionário que já tem UUID
        itens.append(materia_ou_dict)

    salvar_dados(itens)


def atualizar_item(id_item, nova_data, novo_indice, status):
    """Atualiza as informações de revisão de um item."""
    itens = carregar_dados()
    for item in itens:
        # str() em ambos os lados garante que '1' == 1
        if str(item.get("id")) == str(id_item):
            item["data_agendada"] = nova_data
            item["indice_intervalo"] = novo_indice
            item["status"] = status
            item["total_revisoes"] = item.get("total_revisoes", 0) + 1
            break
    salvar_dados(itens)


def deletar_item(id_item):
    """Remove um item pelo ID."""
    itens = carregar_dados()
    # Comparação segura com string para não falhar no ID
    itens_filtrados = [i for i in itens if str(i.get("id")) != str(id_item)]
    salvar_dados(itens_filtrados)


def editar_item(id_item, novos_dados):
    """Atualiza um item com novos dados."""
    itens = carregar_dados()
    for item in itens:
        if str(item.get("id")) == str(id_item):
            item.update(novos_dados)
            break
    salvar_dados(itens)


def get_atividade_semanal():
    """Retorna dados para o gráfico do Dashboard."""
    return [0, 0, 0, 0, 0, 0, 0]
