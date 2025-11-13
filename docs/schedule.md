# Cronograma de Desenvolvimento da API (FastAPI)

## 1. Planejamento

**Objetivo:** entender o propósito da API, escopo e principais recursos.

- [X] Definir o **propósito**
- [X] Listar as **funcionalidades principais**
- [X] Escolher a **arquitetura base**
- [X] Esboçar um **diagrama simples de entidades**
- [X] Decidir o **banco de dados**
- [X] Anotar quais **ferramentas/libraries** serão usadas

## 2. Modelagem e Design

**Objetivo:** estruturar os dados e organizar o código.

- [X] Criar o **diagrama ER** (entidades, chaves, relacionamentos)
- [X] Definir as **entidades principais**
- [X] Criar os **schemas Pydantic** (entrada/saída da API)
- [X] Esboçar a **estrutura de diretórios**
- [X] Definir um **padrão de nomenclatura**
- [ ] Planejar a **autenticação**

## 3. Implementação da API

**Objetivo:** desenvolver as funcionalidades com boas práticas.

* [X] Criar os **modelos de banco** (SQLAlchemy)
* [ ] Configurar o **banco e migrations** (Alembic)
* [ ] Criar as **rotas básicas**
* [ ] Implementar **validações** nos schemas
* [ ] Criar **services** ou **controllers** para separar lógica de negócio
* [ ] Adicionar **tratamento de erros** com `HTTPException`
* [ ] Implementar **autenticação** (JWT, OAuth2 ou básica)
* [ ] Adicionar **paginadores, filtros ou ordenações** (se necessário)

## 4. Testes e Documentação

**Objetivo:** garantir qualidade e clareza.

* [ ] Escrever **testes unitários** para cada endpoint (Pytest)
* [ ] Criar **fixtures** no `conftest.py`
* [ ] Testar rotas no **Swagger UI**
* [ ] Escrever **README.md** com:
  * [ ] Descrição do projeto
  * [ ] Como rodar localmente
  * [ ] Estrutura de diretórios
  * [ ] Exemplos de endpoints
* [X] Criar **notas de desenvolvimento**

## 5. Deploy e Manutenção

**Objetivo:** colocar no ar e garantir estabilidade.

* [ ] Escolher ambiente de deploy (Render, Railway, Deta, Vercel, Fly.io etc.)
* [ ] Configurar variáveis de ambiente no servidor
* [ ] Criar `Dockerfile` (opcional, mas recomendável)
* [ ] Testar deploy (rota raiz e CRUDs)
* [ ] Configurar logs e monitoramento básico
* [ ] Versionar com **Git + GitHub**
* [ ] Criar **releases** e **tags** no Git
* [ ] Planejar atualizações futuras (versões, novas features)