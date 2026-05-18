# 📚 PipoStudy — Revisão Espaçada

**🔗 Deploy:** [pipostudy.onrender.com](https://pipostudy.onrender.com)

---

## O Problema

Estudantes investem horas consumindo conteúdo, mas esquecem a maior parte da informação em poucos dias — a chamada **Curva do Esquecimento**. Isso gera retrabalho, ansiedade pré-provas e baixo aproveitamento do tempo de estudo.

## A Solução

Um aplicativo que automatiza o agendamento de revisões com base na técnica de **Spaced Repetition**, alertando o usuário sobre exatamente o que precisa revisar hoje para transferir o conhecimento para a memória de longo prazo. Disponível como **aplicação desktop** (CustomTkinter) e **versão web** (Flask) com deploy público.

## Público-alvo

Estudantes universitários e qualquer pessoa que precise reter conteúdo de forma eficiente.

---

## Funcionalidades

- **Dashboard inteligente** com contadores de revisões (hoje, atrasadas, total, sequência), gráfico de atividade semanal e próximas revisões
- **Clima em tempo real** na dashboard via Open-Meteo API
- **Alerta de feriados** brasileiros — "Amanhã é feriado, bom dia pra revisar!"
- **Perfil GitHub** integrado — avatar, repos recentes e bio do estudante
- **Cadastro enriquecido** — ao cadastrar um assunto, busca automática de resumo na Wikipedia e imagem de capa via Unsplash
- **Dados de países** — bandeira, capital e população via REST Countries
- **Revisão com feedback** em três níveis (Conexões Claras, Clareando, Ineficaz)
- **Agendamento automático** da próxima revisão com intervalos adaptativos: 1, 3, 7, 14, 30, 60, 120 dias
- **Tema claro/escuro** com toggle na sidebar
- **Busca e filtros** na tela de assuntos (todos, hoje, atrasados, próximos)
- **Edição e exclusão** de assuntos com diálogos de confirmação

---

## APIs Públicas Integradas

| API | Uso na aplicação |
|-----|-----------------|
| **Wikipedia REST API** | Resumo automático ao cadastrar assunto |
| **Open-Meteo** | Clima atual na dashboard (temperatura, condição) |
| **Unsplash** | Imagem de capa por assunto cadastrado |
| **GitHub API** | Perfil e repos do estudante na dashboard |
| **Nager.Date** | Próximos feriados brasileiros |
| **REST Countries** | Dados de países (bandeira, capital, população) |

Endpoints internos: `/api/wiki/<termo>` · `/api/clima` · `/api/github/<user>` · `/api/pais/<nome>` · `/api/feriado`

---

## Tecnologias

- **Python 3.12**
- **CustomTkinter** — interface desktop
- **Flask + Gunicorn** — versão web
- **pytest** — 39 testes (unitários + integração)
- **flake8 + black** — linting e formatação
- **GitHub Actions** — CI automatizado
- **Render** — deploy em nuvem
- **JSON** — armazenamento local

---

## Estrutura do Projeto

```
├── src/
│   ├── main.py                # App desktop (CustomTkinter)
│   ├── core/
│   │   ├── repositorio.py     # CRUD de dados (JSON)
│   │   ├── agendador.py       # Lógica de revisão espaçada
│   │   ├── wikipedia_api.py   # Integração Wikipedia
│   │   └── apis_externas.py   # Clima, Unsplash, GitHub, Feriados, Países
│   └── ui/
│       ├── theme.py           # Paleta centralizada (light/dark)
│       ├── sidebar.py         # Barra lateral com navegação
│       ├── dashboard.py       # Tela inicial
│       ├── cadastro.py        # Formulário de cadastro
│       ├── revisao.py         # Tela de revisão (flashcards)
│       └── meus_assuntos.py   # Grid de assuntos cadastrados
├── web_app.py                 # Versão web (Flask)
├── templates/                 # Templates HTML (Jinja2)
├── tests/                     # 39 testes automatizados
├── dados.json                 # Armazenamento local
├── requirements.txt
├── Procfile                   # Deploy (Render)
└── build.sh                   # Script de build (Render)
```

---

## Instalação

```bash
# Clone o repositório
git clone https://github.com/fernandoscar/bootcamp-etapa-inicial.git
cd bootcamp-etapa-inicial

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows

# Instale as dependências
pip install -r requirements.txt
```

## Execução

### Desktop (CustomTkinter)

```bash
python -m src.main
```

### Web (Flask)

```bash
python web_app.py
# Acesse http://localhost:5000
```

## Testes

```bash
pytest tests/ -v
# 39 testes passando (agendador, repositório, Wikipedia, APIs externas)
```

## Lint

```bash
flake8 src/ tests/ web_app.py
```

---

## Entrega Intermediária

- [x] Integração com 6 APIs públicas
- [x] 39 testes automatizados (unitários + integração)
- [x] Deploy no Render com link público
- [x] GitHub Issue → Branch `entrega-intermediaria` → PR → Merge
- [x] CI atualizado (GitHub Actions)
- [x] README atualizado com link do deploy

---

## Versão

2.0.0

## Autor

**Fernando Henrique Silva de Carvalho**
Engenharia de Software — 3º semestre — CEUB

## Repositório

https://github.com/fernandoscar/bootcamp-etapa-inicial
