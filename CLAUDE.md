# CLAUDE.md

> Arquivo de contrato técnico e comportamental do repositório **booktrack-fastapi**.
> Leia este arquivo integralmente antes de qualquer intervenção no código.

---

## 1. Contexto do Projeto

**BookTrack** é uma API REST para rastreamento pessoal de leituras e gerenciamento de biblioteca.

| Item | Detalhe |
|---|---|
| Tipo | API backend REST (sem frontend) |
| Propósito | Portfólio profissional + uso pessoal |
| Autora | Rafaella Duarte (`rafaella.d.d.carvalho@gmail.com`) |
| Versão | `0.1.0` |
| Repositório | `booktrack-fastapi` |

### Domínio da aplicação

A API permite ao usuário autenticado:
- Cadastrar e gerenciar livros, autores, categorias, editoras, coleções, formatos, prateleiras e tags
- Registrar e acompanhar o progresso de leituras (status, páginas lidas, clube do livro, metas)
- Importar dados via script CSV

### Contexto de portfólio

Por ser um projeto de portfólio, **qualidade supera velocidade**. Isso implica:
- Código limpo, legível e bem nomeado em toda a base
- Boas práticas de segurança aplicadas consistentemente
- Testes automatizados para toda funcionalidade nova
- Documentação inline (docstrings) em funções públicas de services e repositories

---

## 2. Stack Tecnológica

### Runtime e linguagem

| Item | Versão |
|---|---|
| Python | `^3.12` |
| Gerenciador de pacotes | Poetry (`pyproject.toml`) |

### Dependências principais

| Biblioteca | Versão | Responsabilidade |
|---|---|---|
| `fastapi[standard]` | `^0.121.0` | Framework web |
| `sqlalchemy` | `^2.0.44` | ORM — async |
| `aiosqlite` | `^0.22.0` | Driver SQLite async (dev) |
| `alembic` | `^1.17.1` | Migrations |
| `pydantic-settings` | `^2.12.0` | Configurações via `.env` |
| `pyjwt` | `^2.10.1` | Tokens JWT |
| `pwdlib[argon2]` | `^0.3.0` | Hash de senhas (Argon2) |
| `pandas` | `^2.3.3` | Script de importação CSV |

### Ferramentas de desenvolvimento

| Ferramenta | Versão | Uso |
|---|---|---|
| `pytest` | `>=8.4.2` | Testes |
| `pytest-asyncio` | `>=1.3.0` | Testes async |
| `pytest-cov` | `>=7.0.0` | Cobertura de testes |
| `httpx` | `>=0.28.1` | Cliente HTTP nos testes |
| `ruff` | `>=0.14.4` | Linting e formatação |
| `taskipy` | `>=1.14.1` | Atalhos de comandos |

### Banco de dados

| Ambiente | Banco | Observação |
|---|---|---|
| Desenvolvimento | SQLite (`database.db`) | Driver `aiosqlite` |
| Produção (planejado) | PostgreSQL 16 | Definido no `docker-compose.yml` |

### Comandos essenciais

```bash
task run      # fastapi dev booktrack_fastapi/main.py
task test     # ruff check → pytest --cov → coverage html
task lint     # ruff check (somente verificação)
task format   # ruff check --fix + ruff format

alembic revision --autogenerate -m "descrição"  # nova migration
alembic upgrade head                             # aplicar migrations
alembic downgrade -1                             # reverter última

docker-compose up -d    # PostgreSQL (5432) + PgAdmin (5050)
docker-compose down
```

---

## 3. Padrões de Arquitetura

### Fluxo de camadas

```
Router → Service → Repository → Banco de dados
  ↑           ↑          ↑
HTTP       Negócio    Persistência
```

### Responsabilidades por camada

| Camada | Faz | Não faz |
|---|---|---|
| **Router** | Valida entrada via Pydantic, retorna status codes, trata `None` como `404` | Lógica de negócio, queries diretas |
| **Service** | Validações, orquestração de repositórios, controle de fluxo | Queries SQL, HTTP exceptions |
| **Repository** | Queries SQLAlchemy, `commit`, `refresh` | Lógica de negócio, HTTP exceptions |

### Exceção documentada — Authors sem Service

Para entidades com CRUD simples e sem regras de negócio, o router injeta o repositório diretamente via `Depends()`, suprimindo a camada de Service. Esse padrão aplica-se **somente** a entidades sem regras de negócio (ex: Authors). Books, Readings e Categories mantêm a camada de Service.

### Padrões SQLAlchemy

- **Async obrigatório**: toda a stack usa `AsyncSession` e `asyncio engine`
- **Eager loading com `selectinload`**: todos os relacionamentos são carregados explicitamente — nunca lazy loading (incompatível com sessões async)
- **Dois registros de metadados**: `Base` (modelos principais) e `table_registry` (modelo `User` via `mapped_as_dataclass`) — ambos combinados no Alembic e nos testes
- **Nunca usar** `lazy='select'` ou acessar relacionamentos fora de sessão ativa

### Padrões de schemas Pydantic

Schemas são separados por operação — nunca reutilizar o mesmo schema para fins diferentes:

| Sufixo | Uso |
|---|---|
| `XCreate` | Payload de criação (POST) |
| `XUpdate` | Payload de atualização (PUT/PATCH) |
| `XFilter` | Parâmetros de query/filtro |
| `XList` | Resposta paginada ou lista |
| `XExpanded` | Resposta com relacionamentos expandidos |

### Repositório genérico — Properties

`PropertiesRepository` recebe o model como parâmetro e é reutilizado para entidades simples com apenas `id` e `name`: Collections, Publishers, Tags, Shelves, Formats, ReadingStatus.

### Autenticação

| Item | Detalhe |
|---|---|
| Estratégia | JWT com dois tokens |
| `access_token` | Expiração: 30 minutos |
| `refresh_token` | Expiração: 7 dias |
| Algoritmo | HS256 |
| Hash de senha | Argon2 via `pwdlib` |
| Campo de login | Campo `username` recebe o e-mail do usuário |

---

## 4. Regras de Desenvolvimento

### Código

- Usar `async/await` em todos os endpoints, services e repositories
- Tipagem completa obrigatória em todas as funções (`Mapped`, `Annotated`, return types)
- Usar `Annotated` + `Depends` para aliases de injeção (`SessionDep`, `CurrentUser`)
- Docstrings em todas as funções públicas de services e repositories
- Nomear arquivos em `snake_case`, classes em `PascalCase`, funções e variáveis em `snake_case`, constantes em `UPPER_SNAKE_CASE`

### Testes

- Toda funcionalidade nova deve ter testes correspondentes antes de ser considerada concluída
- Não quebrar os testes existentes: `test_auth.py`, `test_security.py`, `test_properties.py`
- Rodar `task test` após qualquer modificação antes de reportar conclusão
- Fixtures compartilhadas ficam em `tests/conftest.py`

### Segurança

- Secrets, URLs e credenciais **sempre** via `.env` + `pydantic-settings` — nunca hardcoded
- Nunca versionar `.env`, `database.db` ou qualquer arquivo com dados reais
- Toda rota autenticada deve usar `CurrentUser` como dependência

### Migrations

- Nunca criar migrations automaticamente sem confirmar com a autora
- Toda migration deve ter nome descritivo em português ou inglês técnico
- Testar migration com `alembic upgrade head` + `alembic downgrade -1` antes de commitar

---

## 5. Restrições e Boas Práticas

### Nunca fazer sem aprovação explícita

- ❌ Criar migrations com `alembic revision` automaticamente
- ❌ Alterar o modelo `User` ou `core/security.py`
- ❌ Remover endpoints, modelos ou migrations existentes
- ❌ Instalar novas dependências sem listar, justificar e aguardar aprovação
- ❌ Usar lazy loading em qualquer relacionamento SQLAlchemy
- ❌ Hardcodar qualquer secret, URL de banco ou credencial
- ❌ Reutilizar schemas com propósitos diferentes (ex: usar `XCreate` como resposta)

### Sempre fazer

- ✅ Ler o arquivo existente antes de modificá-lo — nunca assumir o conteúdo
- ✅ Rodar `task test` após qualquer alteração e reportar resultado
- ✅ Usar `selectinload` explícito para todos os relacionamentos carregados
- ✅ Validar entrada via schemas Pydantic em todos os endpoints
- ✅ Tratar `None` como `404` nos routers (nunca retornar `null` ao cliente)
- ✅ Manter variáveis sensíveis exclusivamente em `.env`

---

## 6. Fluxos de Trabalho

### Implementar uma nova funcionalidade

```
1. Ler os arquivos existentes da camada correspondente
2. Criar/atualizar o model (se necessário → gerar migration)
3. Criar/atualizar o schema Pydantic (request + response separados)
4. Implementar o repository (query + eager loading)
5. Implementar o service (regra de negócio + chamada ao repo)
6. Implementar o router (endpoint + injeção de dependências)
7. Escrever os testes
8. Rodar task test e confirmar que tudo passa
```

### Corrigir um bug

```
1. Identificar a camada onde o problema ocorre
2. Ler o arquivo completo antes de editar
3. Escrever um teste que reproduza o bug
4. Corrigir o código
5. Confirmar que o teste passa + demais testes não quebram
```

### Refatorar código existente

```
1. Confirmar escopo com a autora antes de iniciar
2. Garantir cobertura de testes antes de refatorar
3. Refatorar em passos pequenos e verificáveis
4. Rodar task test a cada passo
5. Reportar lista de arquivos modificados ao final
```

### Migrar de SQLite para PostgreSQL

```
1. Atualizar DATABASE_URL no .env
2. Confirmar que docker-compose está rodando (docker-compose up -d)
3. Implementar o Dockerfile (atualmente vazio)
4. Atualizar alembic.ini se necessário (env.py já usa Settings().DATABASE_URL)
5. Rodar alembic upgrade head no novo banco
6. Validar com task test
```

---

## 7. Instruções Específicas para Agentes

### Comportamento geral

- Responder sempre em **português**
- Ler o arquivo completo antes de qualquer edição — nunca editar por memória ou suposição
- Quando a solicitação tiver mais de uma interpretação possível, perguntar antes de implementar
- Ao concluir qualquer tarefa, listar os arquivos criados ou modificados
- Não inventar informações: se algo não estiver claro no código, sinalizar como "a verificar"

### Ao iniciar uma sessão

1. Confirmar que este `CLAUDE.md` foi lido integralmente
2. Verificar o estado atual dos testes com `task test`
3. Perguntar qual é o objetivo da sessão antes de propor qualquer mudança


### Estrutura de pastas de referência

```
booktrack_fastapi/
├── main.py
├── core/
│   ├── database.py       # Engine async + get_session
│   ├── dependencies.py   # SessionDep, CurrentUser
│   ├── security.py       # JWT, hash de senha, get_current_user
│   └── settings.py       # Configurações via .env
├── models/               # SQLAlchemy ORM
├── schemas/              # Pydantic (request/response por operação)
├── repositories/         # Queries SQLAlchemy
├── services/             # Regras de negócio
├── routers/              # Endpoints HTTP
└── utility/              # Helpers (date_tools.py)
```