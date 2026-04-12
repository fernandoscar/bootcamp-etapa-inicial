import json
import os

# Define o caminho para o teu ficheiro de dados na raiz do projeto
ARQUIVO_DADOS = "dados.json"


def carregar_dados():
    """
    Lê o ficheiro JSON e converte o texto para uma lista de dicionários Python.
    """
    if not os.path.exists(ARQUIVO_DADOS):
        return []

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            return dados
    except json.JSONDecodeError:
        # Se o ficheiro estiver vazio ou corrompido, devolvemos uma lista vazia
        return []


def salvar_dados(itens):
    """
    Guarda a lista de itens no ficheiro JSON.
    Função exigida pelos testes automatizados.
    """
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(itens, arquivo, indent=4, ensure_ascii=False)


def atualizar_item(id_item, nova_data, novo_indice, status):
    """
    Procura um item pelo ID, atualiza os seus valores e guarda no JSON.
    """
    itens = carregar_dados()

    for item in itens:
        if item.get("id") == id_item:
            item["data_agendada"] = nova_data
            item["indice_intervalo"] = novo_indice
            item["status"] = status
            item["total_revisoes"] = item.get("total_revisoes", 0) + 1
            break

    salvar_dados(itens)


def adicionar_item(novo_item):
    """
    Guarda um novo assunto na base de dados.
    """
    itens = carregar_dados()
    itens.append(novo_item)
    salvar_dados(itens)


def deletar_item(id_item):
    """
    Lê os dados, remove o item correspondente ao ID e guarda novamente.
    """
    itens = carregar_dados()
    itens_filtrados = [item for item in itens if item.get("id") != id_item]
    salvar_dados(itens_filtrados)


def editar_item(id_item, novos_dados):
    """
    Procura o item pelo ID e atualiza as suas chaves com 'novos_dados'.
    """
    itens = carregar_dados()

    for item in itens:
        if item.get("id") == id_item:
            item.update(novos_dados)
            break

    salvar_dados(itens)


def get_atividade_semanal():
    """
    Retorna os dados para o gráfico de 'Atividade semanal' no Dashboard.
    """
    return [0, 0, 0, 0, 0, 0, 0]
