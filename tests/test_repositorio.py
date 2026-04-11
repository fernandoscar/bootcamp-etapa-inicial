import json
import os
import pytest
from datetime import date
from src.core.repositorio import (
    carregar_dados, salvar_dados, adicionar_item, atualizar_item
)

ARQUIVO_TESTE = "dados.json"


@pytest.fixture(autouse=True)
def limpar_arquivo():
    """Garante um dados.json limpo antes e depois de cada teste."""
    if os.path.exists(ARQUIVO_TESTE):
        os.remove(ARQUIVO_TESTE)
    yield
    if os.path.exists(ARQUIVO_TESTE):
        os.remove(ARQUIVO_TESTE)


def test_carregar_dados_arquivo_inexistente():
    resultado = carregar_dados()
    assert resultado == []


def test_salvar_e_carregar_dados():
    itens = [{"id": 1, "assunto": "Teste"}]
    salvar_dados(itens)
    resultado = carregar_dados()
    assert resultado == itens


def test_adicionar_item_cria_estrutura_correta():
    adicionar_item("Matemática", "Derivadas")
    itens = carregar_dados()
    assert len(itens) == 1
    assert itens[0]["materia"] == "Matemática"
    assert itens[0]["assunto"] == "Derivadas"
    assert itens[0]["indice_intervalo"] == 0
    assert itens[0]["data_agendada"] == str(date.today())
    assert itens[0]["status"] == "Pendente"


def test_adicionar_multiplos_itens():
    adicionar_item("Física", "Cinemática")
    adicionar_item("Química", "Mol")
    itens = carregar_dados()
    assert len(itens) == 2


def test_atualizar_item():
    adicionar_item("História", "Revolução Francesa")
    atualizar_item(1, "2025-12-01", 2, "Revisado")
    itens = carregar_dados()
    assert itens[0]["data_agendada"] == "2025-12-01"
    assert itens[0]["indice_intervalo"] == 2
    assert itens[0]["status"] == "Revisado"