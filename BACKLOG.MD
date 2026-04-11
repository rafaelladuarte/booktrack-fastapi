# BACKLOG.md — BookTrack API

> Backlog técnico de pendências identificadas na análise do repositório.
> Ordenado por prioridade. Atualizar status conforme progresso.

---

## Legenda

| Símbolo | Significado |
|---|---|
| 🔴 | Crítico — bloqueia segurança ou funcionalidade core |
| 🟡 | Médio — compromete qualidade ou funcionalidade esperada |
| 🟠 | Médio-baixo — necessário para produção, mas não bloqueia dev |
| 🟢 | Baixo — limpeza, organização e melhoria futura |
| ⬜ | Não iniciado |
| 🔄 | Em progresso |
| ✅ | Concluído |

---

## Sprint 1 — Segurança e Estabilidade

### BT-001 — Mover SECRET_KEY para variável de ambiente
**Prioridade:** 🔴 Crítico  
**Status:** ✅ Concluído  
**Arquivo:** `booktrack_fastapi/core/security.py`

**Problema:**  
`SECRET_KEY` está hardcoded como `'your-secret-key'` diretamente no código-fonte. Qualquer pessoa com acesso ao repositório consegue forjar tokens JWT válidos.

**Ação:**
1. Adicionar `SECRET_KEY` ao `.env` e ao `.env.example`
2. Expor a variável via `pydantic-settings` em `core/settings.py`
3. Importar `Settings().SECRET_KEY` em `core/security.py`
4. Garantir que `.env` está no `.gitignore`
5. Rodar `task test` e confirmar que `test_auth.py` e `test_security.py` passam

**Critério de aceite:**  
Nenhuma secret hardcoded no código. `SECRET_KEY` lida exclusivamente via `.env`.

---

### BT-002 — Corrigir inconsistência no campo de login (username vs email)
**Prioridade:** 🟡 Médio  
**Status:** ✅ Concluído  
**Arquivo:** `booktrack_fastapi/routers/auth.py`, `booktrack_fastapi/core/security.py`

**Problema:**  
O router de autenticação recebe o campo `username` no formulário OAuth2, mas internamente o sistema usa `email` como identificador do usuário e como `sub` do JWT. Isso cria ambiguidade e pode confundir consumidores da API.

**Ação:**
1. Decidir o identificador canônico: `email` (recomendado)
2. Atualizar o router de auth para deixar explícito que `username` deve receber o e-mail (via comentário ou renomeação do campo no schema)
3. Garantir consistência entre o campo recebido, a query no banco e o `sub` do token
4. Atualizar `test_auth.py` para refletir a decisão

**Critério de aceite:**  
Campo de login, query no banco e `sub` do JWT usam o mesmo identificador de forma explícita e documentada.

---

### BT-003 — Corrigir fixtures async em test_readings.py
**Prioridade:** 🟡 Médio  
**Status:** ✅ Concluído  
**Arquivo:** `tests/test_readings.py`, `tests/conftest.py`

**Problema:**  
`test_readings.py` usa `AsyncClient` e uma fixture `async_session` que não estão definidas no `conftest.py` atual (que usa `TestClient` síncrono e fixture `session` síncrona). Os testes provavelmente falham ou são ignorados.

**Ação:**
1. Rodar `task test` e confirmar quais testes estão falhando
2. Adicionar ao `conftest.py` as fixtures necessárias:
   - `async_session` — `AsyncSession` com banco de testes
   - `async_client` — `AsyncClient` do `httpx` apontando para a app
3. Ajustar `pytest.ini` ou `pyproject.toml` para `asyncio_mode = "auto"` se necessário
4. Garantir que os testes de readings passam sem afetar os demais

**Critério de aceite:**  
`task test` passa com 0 erros. `test_readings.py` executado e coberto.

---

## Sprint 2 — Funcionalidades Incompletas

### BT-004 — Implementar categories_service.list_by_filter()
**Prioridade:** 🟡 Médio  
**Status:** ✅ Concluído  
**Arquivo:** `booktrack_fastapi/services/categories_service.py`

**Problema:**  
O método `list_by_filter()` existe no service de categorias mas retorna `pass` — sem implementação real. Qualquer chamada ao endpoint correspondente retorna resultado incorreto ou erro.

**Ação:**
1. Ler `categories_repo.py` para entender os métodos disponíveis
2. Implementar `list_by_filter()` no service delegando ao repositório com os filtros recebidos
3. Verificar se o router de categorias já chama esse método ou se precisa de ajuste
4. Escrever teste cobrindo o filtro por `parent_id` (categoria hierárquica)

**Critério de aceite:**  
`GET /categories?parent_id=X` retorna apenas categorias filhas do parent informado.

---

### BT-005 — Implementar endpoint POST /readings
**Prioridade:** 🟡 Médio  
**Status:** ✅ Concluído  
**Arquivo:** `booktrack_fastapi/routers/readings.py`, `booktrack_fastapi/services/readings_service.py`

**Problema:**  
Não existe endpoint `POST /readings`. A criação de uma leitura só é possível via script de importação CSV (`migrate_csv_to_db.py`), o que torna a API incompleta como produto.

**Ação:**
1. Criar schema `ReadingCreate` em `schemas/readings.py` com os campos obrigatórios
2. Implementar método `create()` no `ReadingsRepository`
3. Implementar método `create()` no `ReadingsService` com validações necessárias (ex: livro deve existir)
4. Adicionar endpoint `POST /readings` no router com autenticação via `CurrentUser`
5. Escrever testes para o novo endpoint

**Critério de aceite:**  
`POST /readings` cria uma nova leitura vinculada ao usuário autenticado e retorna `201` com o objeto criado.

---

### BT-006 — Implementar filtro shelve_id em books_repo.py
**Prioridade:** 🟡 Médio  
**Status:** ⬜ Não iniciado  
**Arquivo:** `booktrack_fastapi/repositories/books_repo.py`

**Problema:**  
O schema `BookFilter` possui o campo `shelve_id`, mas o repositório ignora esse filtro (há comentário no código indicando isso). Usuários que tentam filtrar livros por prateleira não obtêm resultado correto.

**Ação:**
1. Localizar o método de listagem em `books_repo.py`
2. Adicionar a condição de filtro por `shelve_id` na query (relação M2M via `readings_shelves` ou campo direto — verificar o model)
3. Confirmar que o filtro funciona com `selectinload` ativo
4. Escrever teste cobrindo o filtro

**Critério de aceite:**  
`GET /books?shelve_id=X` retorna apenas livros da prateleira informada.

---

## Sprint 3 — Infraestrutura e Deploy

### BT-007 — Implementar Dockerfile
**Prioridade:** 🟠 Médio-baixo  
**Status:** ⬜ Não iniciado  
**Arquivo:** `Dockerfile`

**Problema:**  
O `Dockerfile` existe no repositório mas está completamente vazio. A aplicação não pode ser containerizada, o que impede deploy em qualquer ambiente baseado em container.

**Ação:**
1. Implementar `Dockerfile` multi-stage:
   - Stage `builder`: instala dependências via Poetry
   - Stage `runtime`: copia apenas o necessário, roda como usuário não-root
2. Testar localmente com `docker build` e `docker run`
3. Integrar ao `docker-compose.yml` como serviço `api`
4. Adicionar variáveis de ambiente necessárias no `docker-compose.yml`
5. Documentar o processo no `README.md`

**Critério de aceite:**  
`docker-compose up` sobe API + PostgreSQL + PgAdmin. `task test` passa apontando para o banco PostgreSQL.

---

### BT-008 — Migrar ambiente de desenvolvimento para PostgreSQL
**Prioridade:** 🟠 Médio-baixo  
**Status:** ⬜ Não iniciado  
**Arquivo:** `.env`, `alembic.ini`, `tests/conftest.py`

**Problema:**  
O desenvolvimento usa SQLite enquanto a produção planeja PostgreSQL. Isso pode ocultar comportamentos diferentes entre os bancos (ex: tipos de dados, constraints, comportamento de enums).

**Dependência:** BT-007 deve estar concluído antes.

**Ação:**
1. Atualizar `.env` com `DATABASE_URL` apontando para o PostgreSQL do docker-compose
2. Confirmar que `env.py` do Alembic usa `Settings().DATABASE_URL` (já configurado)
3. Rodar `alembic upgrade head` no PostgreSQL
4. Ajustar `conftest.py` para usar banco de testes PostgreSQL (ou SQLite isolado para testes)
5. Instalar driver `asyncpg` via Poetry e atualizar `pyproject.toml`

**Critério de aceite:**  
`task run` e `task test` funcionam com PostgreSQL como banco principal.

---

## Sprint 4 — Limpeza e Qualidade

### BT-009 — Avaliar e remover BooksExpandedView e ReadingExpandedView
**Prioridade:** 🟢 Baixo  
**Status:** ⬜ Não iniciado  
**Arquivo:** `booktrack_fastapi/models/books.py`, `booktrack_fastapi/models/readings.py`

**Problema:**  
`BooksExpandedView` e `ReadingExpandedView` são modelos mapeados para views SQL que existem no código mas não são utilizados pelas queries ativas (que usam `selectinload` nos modelos principais).

**Ação:**
1. Verificar se as views existem no banco e se há migrations que as criam
2. Decidir: **usar** as views nas queries ou **remover** os modelos e as views do banco
3. Se remover: criar migration de rollback das views + remover os modelos
4. Se manter: documentar o motivo e quando devem ser usadas

**Critério de aceite:**  
Não há código morto relacionado a views sem uso documentado ou aplicado.

---

### BT-010 — Remover arquivos de exemplo e arquivos soltos
**Prioridade:** 🟢 Baixo  
**Status:** ⬜ Não iniciado  
**Arquivos:** `repositories/example.py`, `tests/example_test_app.py`, `tests/example_test_db.py`, `simple.md`, `simple2.md`

**Problema:**  
Arquivos de exemplo e rascunhos antigos poluem o repositório e podem confundir quem lê o código (inclusive agentes de IA).

**Ação:**
1. Confirmar que nenhum arquivo listado é importado por outro módulo
2. Remover todos os arquivos listados
3. Rodar `task test` para garantir que nada quebrou

**Critério de aceite:**  
Repositório sem arquivos `example_*`, `simple.md` ou `simple2.md`.

---

### BT-011 — Adicionar docstrings nas funções públicas de services e repositories
**Prioridade:** 🟢 Baixo  
**Status:** ⬜ Não iniciado  
**Arquivos:** `services/`, `repositories/`

**Problema:**  
Por ser um projeto de portfólio, a ausência de docstrings reduz a legibilidade e a qualidade percebida do código.

**Ação:**
1. Adicionar docstring a cada método público de todos os services
2. Adicionar docstring a cada método público de todos os repositories
3. Seguir o formato Google Style Docstring:

```python
async def get_by_id(self, book_id: int) -> Book | None:
    """Busca um livro pelo ID com todos os relacionamentos carregados.

    Args:
        book_id: Identificador único do livro.

    Returns:
        Instância de Book com relacionamentos expandidos, ou None se não encontrado.
    """
```

**Critério de aceite:**  
Todas as funções públicas de `services/` e `repositories/` possuem docstrings no formato Google Style.

---

## Resumo

| ID | Título | Prioridade | Sprint | Status |
|---|---|---|---|---|
| BT-001 | Mover SECRET_KEY para variável de ambiente | 🔴 Crítico | 1 | ✅ |
| BT-002 | Corrigir inconsistência no campo de login | 🟡 Médio | 1 | ✅ |
| BT-003 | Corrigir fixtures async em test_readings.py | 🟡 Médio | 1 | ✅ |
| BT-004 | Implementar categories_service.list_by_filter() | 🟡 Médio | 2 | ✅ |
| BT-005 | Implementar endpoint POST /readings | 🟡 Médio | 2 | ✅ |
| BT-006 | Implementar filtro shelve_id em books_repo.py | 🟡 Médio | 2 | ⬜ |
| BT-007 | Implementar Dockerfile | 🟠 Médio-baixo | 3 | ⬜ |
| BT-008 | Migrar ambiente de dev para PostgreSQL | 🟠 Médio-baixo | 3 | ⬜ |
| BT-009 | Avaliar e remover Views não utilizadas | 🟢 Baixo | 4 | ⬜ |
| BT-010 | Remover arquivos de exemplo e arquivos soltos | 🟢 Baixo | 4 | ⬜ |
| BT-011 | Adicionar docstrings em services e repositories | 🟢 Baixo | 4 | ⬜ |