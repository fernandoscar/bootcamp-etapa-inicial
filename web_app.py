"""
PipoStudy — Versão Web (Flask).
Deploy: Render (gunicorn web_app:app).
"""

import json
import os
import uuid
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, jsonify
from src.core.agendador import calcular_proxima_data, classificar_itens, INTERVALOS
from src.core.wikipedia_api import buscar_resumo
from src.core.apis_externas import (
    buscar_clima,
    buscar_imagem,
    buscar_perfil_github,
    buscar_repos_github,
    proximo_feriado,
    buscar_pais,
)

app = Flask(__name__, template_folder="templates", static_folder="static")

DADOS_PATH = os.path.join(os.path.dirname(__file__), "dados.json")
GITHUB_USER = os.environ.get("GITHUB_USER", "fernandoscar")


# ---------- helpers ----------

def _carregar():
    if not os.path.exists(DADOS_PATH):
        return []
    try:
        with open(DADOS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def _salvar(itens):
    with open(DADOS_PATH, "w", encoding="utf-8") as f:
        json.dump(itens, f, indent=4, ensure_ascii=False)


# ---------- rotas ----------

@app.route("/")
def index():
    itens = _carregar()
    para_hoje, atrasados = classificar_itens(itens)
    fila = atrasados + para_hoje

    # APIs externas
    clima = buscar_clima()
    feriado = proximo_feriado()
    github = buscar_perfil_github(GITHUB_USER)
    repos = buscar_repos_github(GITHUB_USER, limite=3)

    return render_template(
        "index.html",
        itens=itens,
        para_hoje=para_hoje,
        atrasados=atrasados,
        fila=fila,
        total=len(itens),
        INTERVALOS=INTERVALOS,
        date=date,
        clima=clima,
        feriado=feriado,
        github=github,
        repos=repos,
    )


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        materia = request.form.get("materia", "").strip()
        assunto = request.form.get("assunto", "").strip()
        anotacao = request.form.get("anotacao", "").strip()
        categoria = request.form.get("categoria", "semestre")
        semestre = int(request.form.get("semestre", "1"))

        if materia and assunto:
            # Buscar resumo da Wikipedia
            wiki = buscar_resumo(assunto)
            if wiki["encontrado"] and not anotacao:
                anotacao = wiki["resumo"][:300]

            # Buscar imagem via Unsplash
            img = buscar_imagem(assunto)

            novo = {
                "id": str(uuid.uuid4()),
                "materia": materia,
                "assunto": assunto,
                "anotacao": anotacao,
                "categoria": categoria,
                "semestre": semestre if categoria == "semestre" else 0,
                "data_agendada": str(date.today()),
                "indice_intervalo": 0,
                "total_revisoes": 0,
                "status": "Pendente",
                "wiki_url": wiki.get("url", ""),
                "imagem_url": img.get("url", ""),
            }
            itens = _carregar()
            itens.append(novo)
            _salvar(itens)
            return redirect(url_for("index"))

    return render_template("cadastrar.html")


@app.route("/revisar")
def revisar():
    itens = _carregar()
    para_hoje, atrasados = classificar_itens(itens)
    fila = atrasados + para_hoje
    return render_template("revisar.html", fila=fila)


@app.route("/responder/<item_id>/<feedback>")
def responder(item_id, feedback):
    itens = _carregar()
    for item in itens:
        if str(item["id"]) == str(item_id):
            nova_data, novo_indice = calcular_proxima_data(
                item["indice_intervalo"], feedback
            )
            item["data_agendada"] = str(nova_data)
            item["indice_intervalo"] = novo_indice
            item["total_revisoes"] = item.get("total_revisoes", 0) + 1
            item["status"] = (
                "Precisa Reestudar" if feedback == "ineficaz" else "Revisado"
            )
            break
    _salvar(itens)
    return redirect(url_for("revisar"))


@app.route("/deletar/<item_id>")
def deletar(item_id):
    itens = _carregar()
    itens = [i for i in itens if str(i["id"]) != str(item_id)]
    _salvar(itens)
    return redirect(url_for("index"))


# ---------- endpoints de API ----------

@app.route("/api/wiki/<termo>")
def api_wiki(termo):
    """Retorna resumo da Wikipedia."""
    return jsonify(buscar_resumo(termo))


@app.route("/api/clima")
def api_clima():
    """Retorna clima atual de Brasília."""
    return jsonify(buscar_clima())


@app.route("/api/github/<username>")
def api_github(username):
    """Retorna perfil público do GitHub."""
    return jsonify(buscar_perfil_github(username))


@app.route("/api/pais/<nome>")
def api_pais(nome):
    """Retorna dados de um país."""
    return jsonify(buscar_pais(nome))


@app.route("/api/feriado")
def api_feriado():
    """Retorna o próximo feriado brasileiro."""
    f = proximo_feriado()
    return jsonify(f if f else {"encontrado": False})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
