import pytest
from datetime import date
from src.core.repositorio import (
    carregar_dados,
    salvar_dados,
    adicionar_item,
    atualizar_item,
    deletar_item,
    editar_item,
)


@pytest.fixture
def db(tmp_path):
    """Retorna um caminho temporário isolado para cada teste."""
    return str(tmp_path / "dados_teste.json")


def test_carregar_dados_arquivo_inexistente(db):
    resultado = carregar_dados(db)
    assert resultado == []


def test_salvar_e_carregar_dados(db):
    itens = [{"id": 1, "assunto": "Teste"}]
    salvar_dados(itens, db)
    resultado = carregar_dados(db)
    assert resultado == itens


def test_adicionar_item_cria_estrutura_correta(db):
    adicionar_item("Matemática", "Derivadas", caminho=db)
    itens = carregar_dados(db)
    assert len(itens) == 1
    assert itens[0]["materia"] == "Matemática"
    assert itens[0]["assunto"] == "Derivadas"
    assert itens[0]["indice_intervalo"] == 0
    assert itens[0]["data_agendada"] == str(date.today())
    assert itens[0]["status"] == "Pendente"


def test_adicionar_multiplos_itens(db):
    adicionar_item("Física", "Cinemática", caminho=db)
    adicionar_item("Química", "Mol", caminho=db)
    itens = carregar_dados(db)
    assert len(itens) == 2


def test_atualizar_item(db):
    adicionar_item("História", "Revolução Francesa", caminho=db)
    atualizar_item(1, "2025-12-01", 2, "Revisado", caminho=db)
    itens = carregar_dados(db)
    assert itens[0]["data_agendada"] == "2025-12-01"
    assert itens[0]["indice_intervalo"] == 2
    assert itens[0]["status"] == "Revisado"


def test_atualizar_item_incrementa_total_revisoes(db):
    adicionar_item("Redes", "TCP/IP", caminho=db)
    atualizar_item(1, "2025-12-01", 1, "Revisado", caminho=db)
    atualizar_item(1, "2025-12-10", 2, "Revisado", caminho=db)
    itens = carregar_dados(db)
    assert itens[0]["total_revisoes"] == 2


def test_deletar_item(db):
    adicionar_item("Física", "MRU", caminho=db)
    adicionar_item("Química", "Ácidos", caminho=db)
    itens = carregar_dados(db)
    deletar_item(itens[0]["id"], caminho=db)
    restantes = carregar_dados(db)
    assert len(restantes) == 1
    assert restantes[0]["assunto"] == "Ácidos"


def test_deletar_item_inexistente_nao_altera(db):
    adicionar_item("Bio", "DNA", caminho=db)
    deletar_item("id-que-nao-existe", caminho=db)
    itens = carregar_dados(db)
    assert len(itens) == 1


def test_editar_item(db):
    adicionar_item("POO", "Herança", caminho=db)
    itens = carregar_dados(db)
    editar_item(
        itens[0]["id"],
        {"assunto": "Polimorfismo", "materia": "POO Avançado"},
        caminho=db,
    )
    atualizados = carregar_dados(db)
    assert atualizados[0]["assunto"] == "Polimorfismo"
    assert atualizados[0]["materia"] == "POO Avançado"


def test_editar_item_preserva_campos_existentes(db):
    adicionar_item("Banco de Dados", "Joins", caminho=db)
    itens = carregar_dados(db)
    editar_item(itens[0]["id"], {"assunto": "Inner Join"}, caminho=db)
    atualizados = carregar_dados(db)
    assert atualizados[0]["materia"] == "Banco de Dados"
    assert atualizados[0]["assunto"] == "Inner Join"
    assert atualizados[0]["status"] == "Pendente"


def test_carregar_dados_json_corrompido(tmp_path):
    arquivo = tmp_path / "corrompido.json"
    arquivo.write_text("{ isso nao e json valido }", encoding="utf-8")
    resultado = carregar_dados(str(arquivo))
    assert resultado == []


def test_adicionar_item_como_dicionario(db):
    item_dict = {
        "id": "abc-123",
        "materia": "Algoritmos",
        "assunto": "Recursão",
        "data_agendada": "2026-01-01",
        "indice_intervalo": 0,
        "total_revisoes": 0,
        "status": "Pendente",
    }
    adicionar_item(item_dict, caminho=db)
    itens = carregar_dados(db)
    assert len(itens) == 1
    assert itens[0]["id"] == "abc-123"
    assert itens[0]["assunto"] == "Recursão"
