from datetime import date, timedelta
from src.core.agendador import calcular_proxima_data, classificar_itens, INTERVALOS


def test_feedback_claro_avanca_indice():
    _, novo_indice = calcular_proxima_data(0, "claro")
    assert novo_indice == 1


def test_feedback_clareando_mantem_indice():
    _, novo_indice = calcular_proxima_data(2, "clareando")
    assert novo_indice == 2


def test_feedback_ineficaz_zera_indice():
    _, novo_indice = calcular_proxima_data(4, "ineficaz")
    assert novo_indice == 0


def test_indice_nao_passa_do_limite():
    _, novo_indice = calcular_proxima_data(len(INTERVALOS) - 1, "claro")
    assert novo_indice == len(INTERVALOS) - 1


def test_proxima_data_calculada_corretamente():
    proxima_data, _ = calcular_proxima_data(0, "claro")
    esperado = date.today() + timedelta(days=INTERVALOS[1])
    assert proxima_data == esperado


def test_classificar_itens_separa_corretamente():
    hoje = str(date.today())
    ontem = str(date.today() - timedelta(days=1))
    itens = [
        {"data_agendada": hoje},
        {"data_agendada": ontem},
    ]
    para_hoje, atrasados = classificar_itens(itens)
    assert len(para_hoje) == 1
    assert len(atrasados) == 1


def test_atrasados_ordenados_por_data():
    d1 = str(date.today() - timedelta(days=1))
    d2 = str(date.today() - timedelta(days=5))
    itens = [{"data_agendada": d1}, {"data_agendada": d2}]
    _, atrasados = classificar_itens(itens)
    assert atrasados[0]["data_agendada"] == d2
