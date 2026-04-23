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
2. Atualizar o router de auth para deixar explícito que `username` deve receber o e-mail
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
`test_readings.py` usa `AsyncClient` e uma fixture `async_session` que não estão definidas no `conftest.py` atual. Os testes provavelmente falham ou são ignorados.

**Ação:**
1. Rodar `task test` e confirmar quais testes estão falhando
2. Adicionar ao `conftest.py` as fixtures necessárias: `async_session` e `async_client`
3. Ajustar `pyproject.toml` para `asyncio_mode = "auto"` se necessário
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
O método `list_by_filter()` existe no service de categorias mas retorna `pass` — sem implementação real.

**Ação:**
1. Ler `categories_repo.py` para entender os métodos disponíveis
2. Implementar `list_by_filter()` no service delegando ao repositório
3. Verificar se o router de categorias já chama esse método
4. Escrever teste cobrindo o filtro por `parent_id`

**Critério de aceite:**
`GET /categories?parent_id=X` retorna apenas categorias filhas do parent informado.

---

### BT-005 — Implementar endpoint POST /readings
**Prioridade:** 🟡 Médio
**Status:** ✅ Concluído
**Arquivo:** `booktrack_fastapi/routers/readings.py`, `booktrack_fastapi/services/readings_service.py`

**Problema:**
Não existe endpoint `POST /readings`. A criação de uma leitura só é possível via script de importação CSV.

**Ação:**
1. Criar schema `ReadingCreate` em `schemas/readings.py`
2. Implementar método `create()` no `ReadingsRepository`
3. Implementar método `create()` no `ReadingsService` com validações
4. Adicionar endpoint `POST /readings` no router com autenticação via `CurrentUser`
5. Escrever testes para o novo endpoint

**Critério de aceite:**
`POST /readings` cria uma nova leitura vinculada ao usuário autenticado e retorna `201`.

---

### BT-006 — Implementar filtro shelve_id em books_repo.py
**Prioridade:** 🟡 Médio
**Status:** ✅ Concluído
**Arquivo:** `booktrack_fastapi/repositories/books_repo.py`

**Problema:**
O schema `BookFilter` possui o campo `shelve_id`, mas o repositório ignora esse filtro.

**Ação:**
1. Localizar o método de listagem em `books_repo.py`
2. Adicionar condição de filtro por `shelve_id` via JOIN duplo (Books → Readings → readings_shelves)
3. Usar `.distinct()` para evitar duplicações
4. Escrever teste cobrindo o filtro

**Critério de aceite:**
`GET /books?shelve_id=X` retorna apenas livros da prateleira informada.

---

## Sprint 3 — Infraestrutura e Deploy

### BT-007 — Implementar Dockerfile
**Prioridade:** 🟠 Médio-baixo
**Status:** ✅ Concluído
**Arquivo:** `Dockerfile`

**Problema:**
O `Dockerfile` existe no repositório mas está completamente vazio.

**Ação:**
1. Implementar `Dockerfile` multi-stage (builder + runtime)
2. Rodar como usuário não-root
3. Integrar ao `docker-compose.yml` como serviço `api`

**Critério de aceite:**
`docker-compose up` sobe API + PostgreSQL + PgAdmin. `task test` passa.

---

### BT-008 — Migrar ambiente de desenvolvimento para PostgreSQL
**Prioridade:** 🟠 Médio-baixo
**Status:** ✅ Concluído
**Arquivo:** `.env`, `alembic.ini`, `tests/conftest.py`

**Problema:**
O desenvolvimento usa SQLite enquanto a produção planeja PostgreSQL.

**Dependência:** BT-007 concluído.

**Ação:**
1. Atualizar `.env` com `DATABASE_URL` apontando para o PostgreSQL do docker-compose
2. Rodar `alembic upgrade head` no PostgreSQL
3. Ajustar `conftest.py` para usar banco isolado nos testes
4. Instalar driver `asyncpg` via Poetry

**Critério de aceite:**
`task run` e `task test` funcionam com PostgreSQL como banco principal.

---

## Sprint 4 — Limpeza e Qualidade

### BT-009 — Avaliar e remover BooksExpandedView e ReadingExpandedView
**Prioridade:** 🟢 Baixo
**Status:** ✅ Concluído
**Arquivo:** `booktrack_fastapi/models/books.py`, `booktrack_fastapi/models/readings.py`

**Problema:**
`BooksExpandedView` e `ReadingExpandedView` existem no código mas não são utilizados.

**Critério de aceite:**
Não há código morto relacionado a views sem uso documentado ou aplicado.

---

### BT-010 — Remover arquivos de exemplo e arquivos soltos
**Prioridade:** 🟢 Baixo
**Status:** ✅ Concluído
**Arquivos:** `repositories/example.py`, `tests/example_test_app.py`, `tests/example_test_db.py`, `simple.md`, `simple2.md`

**Problema:**
Arquivos de exemplo e rascunhos antigos poluem o repositório.

**Critério de aceite:**
Repositório sem arquivos `example_*`, `simple.md` ou `simple2.md`.

---

### BT-011 — Adicionar docstrings em services e repositories
**Prioridade:** 🟢 Baixo
**Status:** ✅ Concluído
**Arquivos:** `services/`, `repositories/`

**Problema:**
A ausência de docstrings reduz a legibilidade e a qualidade percebida do código de portfólio.

**Critério de aceite:**
Todas as funções públicas de `services/` e `repositories/` possuem docstrings no formato Google Style.

---

## Sprint 5 — Importação de Dados Reais

### BT-012 — Analisar e mapear CSV para os models do banco
**Prioridade:** 🔴 Crítico
**Status:** ✅ Concluído
**Arquivo:** `migrate_csv_to_db.py`, `data/`

**Problema:**
O script de importação é um esboço nunca testado. É necessário mapear cada coluna do CSV para o model correto antes de implementar.

**Critério de aceite:**
Mapeamento completo confirmado. Estratégia definida para valores nulos, "-" e campos opcionais.

---

### BT-013 — Implementar script de importação CSV
**Prioridade:** 🔴 Crítico
**Status:** ✅ Concluído
**Arquivo:** `migrate_csv_to_db.py`

**Dependência:** BT-012 concluído.

**Problema:**
O banco PostgreSQL está vazio. Os dados reais precisam ser importados do CSV.

**Ação:**
1. Reescrever `migrate_csv_to_db.py` usando `AsyncSession` e `Settings().DATABASE_URL`
2. Implementar padrão `get_or_create` com cache em memória
3. Importar na ordem: entidades simples → categories → books → readings
4. Tratar valores nulos, "-" e datas nos formatos `MM/YYYY` e `DD/MM/YYYY`
5. Garantir idempotência (seguro para executar mais de uma vez)

**Critério de aceite:**
Script executa sem erros. Banco populado sem duplicações. Script é idempotente.

---

### BT-014 — Validar dados importados via API
**Prioridade:** 🟡 Médio
**Status:** ✅ Concluído
**Arquivo:** Endpoints existentes

**Dependência:** BT-013 concluído.

**Problema:**
Após a importação, é necessário validar que os dados e relacionamentos estão corretos nos endpoints.

**Ação:**
1. Verificar contagem de registros por tabela no banco
2. Testar `GET /books` e `GET /readings` com dados reais
3. Testar filtros: `author_id`, `shelve_id`, `status_id`
4. Identificar e corrigir problemas de serialização ou relacionamento

**Critério de aceite:**
Todos os endpoints retornam dados reais com relacionamentos expandidos corretamente.

---

## Sprint 6 — RBAC + Rate Limiting com Redis

### BT-015 — Adicionar campo `role` ao model User e migration
**Prioridade:** 🔴 Crítico
**Status:** ✅ Concluído
**Arquivos:** `models/users.py`, `migrations/`

**Problema:**
O model `User` não tem campo `role`. Sem ele, não é possível distinguir Admin de Viewer em nenhuma camada da aplicação.

**Ação:**
1. Adicionar enum `UserRole` com valores `"admin"` e `"viewer"`
2. Adicionar campo `role` no model `User` com default `"viewer"`
3. Gerar migration: `alembic revision --autogenerate -m "add_role_to_users"`
4. Aplicar migration: `alembic upgrade head`
5. Atualizar o usuário de teste para `admin` no banco
6. Rodar `task test`

**Critério de aceite:**
Tabela `users` tem coluna `role`. `task test` passa.

---

### BT-016 — Incluir `role` no payload do JWT
**Prioridade:** 🔴 Crítico
**Status:** ✅ Concluído
**Arquivos:** `core/security.py`, `routers/auth.py`

**Dependência:** BT-015 concluído.

**Problema:**
O token JWT carrega apenas o `email`. O `role` precisa estar no token para evitar consultas ao banco a cada requisição.

**Ação:**
1. Atualizar `routers/auth.py` para incluir `role` no `token_data`
2. Confirmar que `get_current_user` retorna o `User` completo com `role`
3. Rodar `task test`

**Critério de aceite:**
Token JWT contém os campos `sub` (email) e `role`. `task test` passa.

---

### BT-017 — Criar dependências `RequireAdmin` e `AdminUser`
**Prioridade:** 🟡 Médio
**Status:** ✅ Concluído
**Arquivos:** `core/dependencies.py`

**Dependência:** BT-016 concluído.

**Problema:**
Não existe mecanismo para bloquear endpoints por papel.

**Ação:**
1. Criar função `require_admin()` em `core/dependencies.py`
2. Criar alias `AdminUser = Annotated[User, Depends(require_admin)]`
3. Escrever testes: admin passa, viewer recebe 403, não autenticado recebe 401
4. Rodar `task test`

**Critério de aceite:**
`AdminUser` bloqueia viewers com 403. `CurrentUser` continua funcionando. `task test` passa.

---

### BT-018 — Proteger endpoints de escrita com `AdminUser`
**Prioridade:** 🟡 Médio
**Status:** ✅ Concluído
**Arquivos:** todos os routers

**Dependência:** BT-017 concluído.

**Problema:**
Todos os endpoints de escrita estão acessíveis a qualquer usuário autenticado.

**Ação:**
1. Substituir `CurrentUser` por `AdminUser` em todos os POST, PUT e DELETE:
   - `routers/books.py`, `routers/readings.py`, `routers/authors.py`
   - `routers/categories.py`, `routers/properties.py`
2. Manter `CurrentUser` em todos os GET
3. Rodar `task test`

**Critério de aceite:**
GET funciona para Admin e Viewer. POST/PUT/DELETE retornam 403 para Viewer.

---

### BT-019 — Escrever testes de integração para RBAC
**Prioridade:** 🟡 Médio
**Status:** ✅ Concluído
**Arquivos:** `tests/test_rbac.py` (novo), `tests/conftest.py`

**Dependência:** BT-018 concluído.

**Problema:**
Sem testes de integração, não há garantia de que o RBAC funciona corretamente.

**Ação:**
1. Criar fixtures `admin_token` e `viewer_token` no `conftest.py`
2. Criar `tests/test_rbac.py` cobrindo todos os cenários de acesso por papel
3. Rodar `task test`

**Critério de aceite:**
Todos os cenários de RBAC cobertos. `task test` passa com cobertura mantida.

---

### BT-020 — Atualizar `scripts/create_user.py` para suportar `--role`
**Prioridade:** 🟢 Baixo
**Status:** ⬜ Não iniciado
**Arquivos:** `scripts/create_user.py`

**Dependência:** BT-015 concluído.

**Problema:**
O script não permite definir o papel do usuário na criação.

**Ação:**
1. Adicionar argumento `--role` com choices `["admin", "viewer"]` e default `"viewer"`
2. Passar o `role` na criação do usuário
3. Exibir o papel na mensagem de sucesso

**Uso esperado:**
```bash
python scripts/create_user.py \
  --email admin@booktrack.com \
  --password minhasenha123 \
  --role admin
```

**Critério de aceite:**
Script aceita `--role`. Usuário criado tem o papel correto no banco.

---

### BT-021 — Adicionar Redis ao docker-compose e variáveis de ambiente
**Prioridade:** 🔴 Crítico
**Status:** ⬜ Não iniciado
**Arquivos:** `docker-compose.yml`, `.env`, `.env.example`, `booktrack_fastapi/core/settings.py`

**Dependência:** BT-016 concluído.

**Problema:**
O rate limiting com Redis requer o serviço disponível como container. Sem ele, os contadores não têm onde ser armazenados de forma compartilhada.

**Ação:**
1. Adicionar serviço `redis` ao `docker-compose.yml`:
   - Image: `redis:7-alpine`
   - Porta: `6379:6379`
   - Volume persistente `redis_data`
   - Healthcheck: `redis-cli ping` (interval 5s, retries 5)
2. Atualizar serviço `api` para depender do `redis` com `condition: service_healthy`
3. Adicionar `redis_data` na seção `volumes`
4. Adicionar ao `.env` e `.env.example`:
   ```
   REDIS_URL=redis://localhost:6379/0
   ```
5. Adicionar `REDIS_URL` em `core/settings.py` via pydantic-settings
6. Validar: `docker-compose up -d redis && docker-compose exec redis redis-cli ping`

**Critério de aceite:**
Serviço `redis` rodando e `healthy`. `Settings().REDIS_URL` disponível. `task test` passa.

---

### BT-022 — Instalar slowapi e configurar com Redis
**Prioridade:** 🟡 Médio
**Status:** ⬜ Não iniciado
**Arquivos:** `main.py`, `booktrack_fastapi/core/rate_limit.py` (novo)

**Dependência:** BT-021 concluído.

**Problema:**
Sem slowapi configurado com Redis, não há rate limiting funcionando.

**Ação:**
1. Instalar dependências:
   ```bash
   poetry add slowapi redis[asyncio]
   ```
2. Criar `booktrack_fastapi/core/rate_limit.py` com:
   - Função `get_user_identifier()` — identifica por email do JWT ou IP como fallback
   - Instância do `Limiter` usando `Settings().REDIS_URL` como storage
3. Registrar o `Limiter` e handler de `429` no `main.py`
4. Aplicar limite global de `200/minute` como proteção base
5. Rodar `task test`

**Critério de aceite:**
`slowapi` configurado com Redis. Limite global retorna `429` com header `Retry-After`. `task test` passa.

---

### BT-023 — Aplicar limites específicos por endpoint
**Prioridade:** 🟡 Médio
**Status:** ⬜ Não iniciado
**Arquivos:** todos os routers

**Dependência:** BT-022 concluído.

**Problema:**
O limite global não é suficiente. Endpoints críticos precisam de limites mais restritivos.

**Ação:**
1. Adicionar `request: Request` como parâmetro nos endpoints que receberão limite
2. Aplicar `@limiter.limit()` conforme a tabela:

| Grupo | Endpoints | Limite | Identificação |
|---|---|---|---|
| Auth | `POST /auth/token`, `POST /auth/refresh` | 10/minuto | Por IP |
| Leitura | Todos os GET autenticados | 100/minuto | Por usuário |
| Escrita | Todos os POST, PUT, DELETE | 30/minuto | Por usuário |
| Health | `GET /health`, `GET /health/ready` | 20/minuto | Por IP |

3. Rodar `task test`

**Critério de aceite:**
Cada grupo de endpoints tem seu limite aplicado. Ao exceder, retorna `429` com `Retry-After`. `task test` passa.

---

### BT-024 — Escrever testes de rate limiting
**Prioridade:** 🟢 Baixo
**Status:** ⬜ Não iniciado
**Arquivos:** `tests/test_rate_limit.py` (novo), `tests/conftest.py`

**Dependência:** BT-023 concluído.

**Problema:**
Sem testes, não há garantia de que o rate limiting funciona e não será quebrado por alterações futuras.

**Ação:**
1. Adicionar fixture `clear_redis` no `conftest.py` para limpar contadores entre testes
2. Criar `tests/test_rate_limit.py` cobrindo:
   - Requisições dentro do limite retornam 200
   - Ao exceder o limite, retorna 429
   - Response do 429 contém header `Retry-After`
   - Login bloqueado após 10 tentativas por IP
   - Contadores independentes por usuário (usuário A não afeta usuário B)
3. Rodar `task test`

**Critério de aceite:**
Todos os cenários cobertos. `task test` passa com cobertura mantida.

---

## Resumo

| ID | Título | Prioridade | Sprint | Status |
|---|---|---|---|---|
| BT-001 | Mover SECRET_KEY para variável de ambiente | 🔴 Crítico | 1 | ✅ |
| BT-002 | Corrigir inconsistência no campo de login | 🟡 Médio | 1 | ✅ |
| BT-003 | Corrigir fixtures async em test_readings.py | 🟡 Médio | 1 | ✅ |
| BT-004 | Implementar categories_service.list_by_filter() | 🟡 Médio | 2 | ✅ |
| BT-005 | Implementar endpoint POST /readings | 🟡 Médio | 2 | ✅ |
| BT-006 | Implementar filtro shelve_id em books_repo.py | 🟡 Médio | 2 | ✅ |
| BT-007 | Implementar Dockerfile | 🟠 Médio-baixo | 3 | ✅ |
| BT-008 | Migrar ambiente de dev para PostgreSQL | 🟠 Médio-baixo | 3 | ✅ |
| BT-009 | Avaliar e remover Views não utilizadas | 🟢 Baixo | 4 | ✅ |
| BT-010 | Remover arquivos de exemplo e arquivos soltos | 🟢 Baixo | 4 | ✅ |
| BT-011 | Adicionar docstrings em services e repositories | 🟢 Baixo | 4 | ✅ |
| BT-012 | Analisar e mapear CSV para os models | 🔴 Crítico | 5 | ✅ |
| BT-013 | Implementar script de importação CSV | 🔴 Crítico | 5 | ✅ |
| BT-014 | Validar dados importados via API | 🟡 Médio | 5 | ✅ |
| BT-015 | Adicionar campo role ao model User e migration | 🔴 Crítico | 6 | ✅ |
| BT-016 | Incluir role no payload do JWT | 🔴 Crítico | 6 | ✅ |
| BT-017 | Criar dependências RequireAdmin e AdminUser | 🟡 Médio | 6 | ✅ |
| BT-018 | Proteger endpoints de escrita com AdminUser | 🟡 Médio | 6 | ⬜ |
| BT-019 | Escrever testes de integração para RBAC | 🟡 Médio | 6 | ⬜ |
| BT-020 | Atualizar create_user.py para suportar --role | 🟢 Baixo | 6 | ⬜ |
| BT-021 | Adicionar Redis ao docker-compose e variáveis | 🔴 Crítico | 6 | ⬜ |
| BT-022 | Instalar slowapi e configurar com Redis | 🟡 Médio | 6 | ⬜ |
| BT-023 | Aplicar limites específicos por endpoint | 🟡 Médio | 6 | ⬜ |
| BT-024 | Escrever testes de rate limiting | 🟢 Baixo | 6 | ⬜ |