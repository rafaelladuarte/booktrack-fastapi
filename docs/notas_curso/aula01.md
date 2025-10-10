# FastAPI do Zero

## Aula 1 - Configurando Ambiente de Desenvolvimento

### Poetry

* Recomendou utilizar Poetry como gerenciador de projetos Python, e a versão python 3.13.
* Comando executar a aplicação fora do ambiente virtual:

```
poetry run fastapi dev fast_zero/app.py
```

* Quando executar o comando a mensagem de resposta do CLI: 
    * serving: http://127.0.0.1:8000
        * http: -> protocolo  (padrão web)
        * 127.0.0.1 -> endereço de rede IP (endereço especial que aponta para a nossa própria máquina)
        * 8000 -> porta da nossa máquina que está reservada para nossa aplicação
    * O navegador é o cliente tradicional do protocolo padrão web

* Internamente o FastAPI utiliza o [Uvicorn](https://uvicorn.dev/#quickstart), que atua como servidor, disponibilizando a API do FastAPI em rede, ou seja, disponibilizando o acesso a API por um navegador ou de outras aplicações clientes.
* Comando executar a aplicação direto pelo Uvicorn:

```
uvicorn fast_zero.app:app
```

* [Ruff](https://docs.astral.sh/ruff/) = Linter (analisador estático de código) + Formatter (formatador de código PEP8)

### Pytest +  Taskipy

* Para executar os testes com o [Pytest](https://docs.pytest.org/en/stable/) tem que instalar o [Taskipy](https://github.com/taskipy/taskipy) 
* Para testar o arquivo app da api que foi definido no arquivo pyproject.toml, execute o comando:

```
task lint
```

* E para corrigir a formatação do arquivo, execute o comando:

```
task format
```

* Para executar os testes da pasta tests, execute o comando:

```
task test
```

* Quando executamos o comando abaixo, ele gera um relatorio dos testes em formato HTML, que pode ser aberto no navegador (funcionalidade definida no arquivo pyproject.toml)

```
task post_test
```

* A estrutura dos teste do curso é desenvolvida pelo método [AAA](https://xp123.com/3a-arrange-act-assert/) que divide o teste em três fases distintas:
    * Arrange: fase em que monta o ambiente para o teste poder ser executado.
    * Act: fase em que o código de testes executa o código de produção que está sendo testado.
    * Assert: etapa de verificar se tudo correu como esperado.

### Aprofundamento nos estudos

* [Uma introdução aos testes: Como fazer? | Live de Python #232](youtube.com/watch?v=-8H2Pyxnoek&feature=youtu.be)
* [Pytest: Uma introdução - Live de Python #167](https://www.youtube.com/watch?v=MjQCvJmc31A)
* [Pytest Fixtures - Live de Python #168](youtube.com/watch?v=sidi9Z_IkLU&feature=youtu.be)