# 📚 Revisão Espaçada

## O Problema
Estudantes investem horas consumindo conteúdo, mas esquecem a maior parte da informação em poucos dias — a chamada **Curva do Esquecimento**. Isso gera retrabalho, ansiedade pré-provas e baixo aproveitamento do tempo de estudo.

## A Solução
Um aplicativo desktop que automatiza o agendamento de revisões com base na técnica de **Spaced Repetition**, alertando o usuário sobre exatamente o que precisa revisar hoje para transferir o conhecimento para a memória de longo prazo.

## Público-alvo
Estudantes universitários e qualquer pessoa que precise reter conteúdo de forma eficiente.

## Funcionalidades
- Dashboard com contadores de revisões para hoje e atrasadas
- Cadastro de matérias e assuntos
- Modo de revisão com feedback em três níveis (Conexões Claras, Clareando, Ineficaz)
- Agendamento automático da próxima revisão com base no desempenho
- Interface gráfica moderna com suporte a Dark Mode

## Tecnologias
- Python 3.12
- CustomTkinter
- pytest
- flake8 + black
- GitHub Actions
- JSON (armazenamento local)

## Instalação

```bash
# Clone o repositório
git clone https://github.com/fernandoscar/bootcamp-etapa-inicial.git
cd bootcamp-etapa-inicial

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
```

## Execução

```bash
python -m src.main
```

## Testes

```bash
pytest tests/
```

## Lint

```bash
flake8 src/ tests/
```

## Versão
1.0.0

## Autor
Fernando Henrique Silva de Carvalho

## Repositório
https://github.com/fernandoscar/bootcamp-etapa-inicial
