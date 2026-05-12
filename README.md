# PipoStudy — Revisão Espaçada

Sistema de revisão espaçada para estudantes. Cadastre assuntos, receba lembretes automáticos e acompanhe seu progresso com intervalos crescentes baseados em feedback.

## Funcionalidades

- **Cadastro de assuntos** com matéria, semestre e anotações
- **Revisão espaçada** com 3 níveis de feedback (Claro / Clareando / Ineficaz)
- **Intervalos adaptativos**: 1, 3, 7, 14, 30, 60, 120 dias
- **Dashboard** com estatísticas, revisões pendentes e gráfico de atividade
- **Tema claro/escuro** com toggle na sidebar
- **Integração Wikipedia** — busca automática de resumos ao cadastrar assuntos
- **Versão web** (Flask) para acesso remoto

## Tecnologias

- Python 3.12
- CustomTkinter (desktop)
- Flask + Gunicorn (web)
- Wikipedia REST API (pt.wikipedia.org)
- pytest (testes unitários e de integração)
- GitHub Actions (CI)

## Estrutura do Projeto

```
├── src/
│   ├── main.py              # Aplicação desktop (CustomTkinter)
│   ├── core/
│   │   ├── repositorio.py   # CRUD de dados (JSON)
│   │   ├── agendador.py     # Lógica de revisão espaçada
│   │   └── wikipedia_api.py # Integração com Wikipedia API
│   └── ui/
│       ├── theme.py          # Paleta centralizada (light/dark)
│       ├── sidebar.py        # Barra lateral com navegação
│       ├── dashboard.py      # Tela inicial
│       ├── cadastro.py       # Formulário de cadastro
│       ├── revisao.py        # Tela de revisão com flashcards
│       └── meus_assuntos.py  # Grid de assuntos cadastrados
├── web_app.py                # Versão web (Flask)
├── templates/                # Templates HTML (Jinja2)
├── tests/
│   ├── test_repositorio.py   # Testes unitários do repositório
│   ├── test_agendador.py     # Testes do agendador
│   └── test_wikipedia_api.py # Teste de integração da API
├── dados.json                # Armazenamento local
├── requirements.txt
├── Procfile                  # Deploy (Render)
└── build.sh                  # Script de build (Render)
```

## Como Rodar

### Desktop (CustomTkinter)

```bash
pip install -r requirements.txt
python -m src.main
```

### Web (Flask)

```bash
pip install -r requirements.txt
python web_app.py
# Acesse http://localhost:5000
```

### Testes

```bash
pytest tests/ -v
```

## API Pública Integrada

**Wikipedia REST API** — ao cadastrar um assunto sem anotação, o sistema busca automaticamente um resumo na Wikipedia em português.

Endpoint interno: `GET /api/wiki/<termo>` retorna:

```json
{
  "titulo": "Algoritmo",
  "resumo": "Em ciência da computação, um algoritmo é...",
  "url": "https://pt.wikipedia.org/wiki/Algoritmo",
  "encontrado": true
}
```

## Deploy

A versão web está disponível no Render:

**🔗 [Link público do deploy]** *(adicionar após deploy)*

## Entrega Intermediária

- [x] Integração com API pública (Wikipedia)
- [x] Teste de integração da API
- [x] Deploy com link público (Render)
- [x] GitHub Issue → Branch `entrega-intermediaria` → PR → Merge
- [x] CI atualizado (GitHub Actions)
- [x] README atualizado

## Autor

Fernando — Engenharia de Software, 3º semestre
