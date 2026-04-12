from datetime import date, timedelta

INTERVALOS = [3, 7, 14, 21, 30, 60]


def calcular_proxima_data(indice_atual: int, feedback: str) -> tuple[date, int]:
    """
    Retorna (proxima_data, novo_indice) com base no feedback do usuário.
    feedback: "claro" | "clareando" | "ineficaz"
    """
    if feedback == "claro":
        novo_indice = min(indice_atual + 1, len(INTERVALOS) - 1)
    elif feedback == "clareando":
        novo_indice = indice_atual
    else:  # ineficaz
        novo_indice = 0

    dias = INTERVALOS[novo_indice]
    proxima_data = date.today() + timedelta(days=dias)
    return proxima_data, novo_indice


def classificar_itens(itens: list) -> tuple[list, list]:
    """
    Separa itens em (para_hoje, atrasados).
    Ordena por data_agendada crescente.
    """
    hoje = str(date.today())

    para_hoje = [i for i in itens if i["data_agendada"] == hoje]
    atrasados = sorted(
        [i for i in itens if i["data_agendada"] < hoje],
        key=lambda x: x["data_agendada"],
    )
    return para_hoje, atrasados
