# Refatoração JWT - Access Token e Refresh Token

**Data:** 27 de novembro de 2025  
**Versão:** 2.0.0

---

## 📋 Resumo Executivo

A autenticação JWT foi completamente refatorada para implementar o padrão **Access Token + Refresh Token**, aumentando significativamente a segurança e a usabilidade da API. O sistema agora oferece tokens de curta duração para operações regulares e tokens de longa duração para renovação, seguindo as melhores práticas da indústria.

---

## 🎯 Objetivos Alcançados

✅ **Separação de responsabilidades**: Access Token para autenticação, Refresh Token para renovação  
✅ **Segurança aprimorada**: Tokens com tipos específicos e validação rigorosa  
✅ **Mensagens de erro claras**: Feedback específico para cada tipo de falha  
✅ **Código modular**: Funções separadas para cada responsabilidade  
✅ **Testes abrangentes**: 11 testes passando com 67% de cobertura  
✅ **Documentação completa**: Docstrings em todas as funções

---

## 🔄 Mudanças Principais

### 1. Estrutura de Tokens

#### Access Token
- **Duração**: 30 minutos
- **Uso**: Autenticação em rotas protegidas
- **Claim adicional**: `type: 'access'`
- **Renovação**: Via Refresh Token

#### Refresh Token
- **Duração**: 7 dias
- **Uso**: Renovação de Access Token
- **Claim adicional**: `type: 'refresh'`
- **Segurança**: Não pode ser usado para acessar rotas protegidas

### 2. Novas Rotas de Autenticação

#### `POST /auth/token` (Login)
**Substitui**: `POST /login`

**Request**:
```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=senha123"
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### `POST /auth/refresh` (Renovação)
**Nova funcionalidade**

**Request**:
```bash
curl -X POST "http://localhost:8000/auth/refresh" \
  -H "Authorization: Bearer <refresh_token>"
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Arquivos Modificados

#### `booktrack_fastapi/core/security.py`
**Funções adicionadas/modificadas**:

```python
def create_access_token(data: dict) -> str
    """Cria Access Token com 30 minutos de validade"""

def create_refresh_token(data: dict) -> str
    """Cria Refresh Token com 7 dias de validade"""

def verify_token(token: str, token_type: str = 'access') -> dict
    """Verifica e decodifica token com validação de tipo"""

def get_current_user(...) -> User
    """Dependency para validar Access Token"""
```

**Melhorias**:
- ✅ Importação de `ExpiredSignatureError` para tratamento específico
- ✅ Constante `REFRESH_TOKEN_EXPIRE_DAYS = 7`
- ✅ Validação de tipo de token (access vs refresh)
- ✅ Mensagens de erro específicas e em português
- ✅ Docstrings completas em todas as funções

#### `booktrack_fastapi/routers/auth.py` (NOVO)
**Arquivo criado** com 2 rotas:

1. **`POST /auth/token`**: Login com retorno de ambos os tokens
2. **`POST /auth/refresh`**: Renovação usando Refresh Token

**Características**:
- ✅ Validação de credenciais
- ✅ Verificação de tipo de token
- ✅ Geração de novos tokens a cada renovação
- ✅ Tratamento de erros HTTP 401

#### `booktrack_fastapi/schemas/users.py`
**Schema adicionado**:

```python
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
```

#### `booktrack_fastapi/routers/users.py`
**Removido**:
- ❌ Rota `POST /login` (migrada para `/auth/token`)
- ❌ Imports não utilizados: `OAuth2PasswordRequestForm`, `create_access_token`, `verify_password`, `Token`

**Mantido**:
- ✅ `POST /register`: Registro de usuários (pública)
- ✅ `GET /users`: Listagem (protegida)
- ✅ `PUT /users/{user_id}`: Atualização (protegida)
- ✅ `DELETE /users/{user_id}`: Exclusão (protegida)

#### `booktrack_fastapi/main.py`
**Adicionado**:
```python
from booktrack_fastapi.routers import auth
app.include_router(auth.router)
```

---

## 🔒 Segurança Aprimorada

### Validação de Tokens

#### 1. Verificação de Tipo
```python
if payload.get('type') != token_type:
    raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail=f'Token inválido: esperado tipo {token_type}',
    )
```

**Proteção**: Impede uso de Access Token na rota de refresh e vice-versa.

#### 2. Tratamento de Expiração
```python
except ExpiredSignatureError:
    raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Token expirado',
    )
```

**Benefício**: Mensagem clara quando o token expira.

#### 3. Validação de Formato
```python
except DecodeError:
    raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Token inválido ou malformado',
    )
```

**Proteção**: Detecta tokens corrompidos ou falsificados.

### Mensagens de Erro Específicas

| Cenário | Mensagem |
|---------|----------|
| Token expirado | `"Token expirado"` |
| Token malformado | `"Token inválido ou malformado"` |
| Tipo errado | `"Token inválido: esperado tipo {tipo}"` |
| Subject ausente | `"Token inválido: subject não encontrado"` |
| Usuário não existe | `"Usuário não encontrado"` |
| Credenciais inválidas | `"Email ou senha incorretos"` |

---

## 🧪 Testes Implementados

### Arquivo: `tests/test_auth.py` (NOVO)

#### 1. `test_auth_token_success`
- ✅ Login bem-sucedido
- ✅ Retorna access_token e refresh_token
- ✅ Valida estrutura dos tokens
- ✅ Verifica claims (sub, type, exp)

#### 2. `test_auth_token_invalid_credentials`
- ✅ Rejeita email inexistente
- ✅ Retorna HTTP 401

#### 3. `test_auth_token_wrong_password`
- ✅ Rejeita senha incorreta
- ✅ Retorna HTTP 401

#### 4. `test_auth_refresh_success`
- ✅ Aceita Refresh Token válido
- ✅ Retorna novos tokens
- ✅ Valida estrutura dos novos tokens

#### 5. `test_auth_refresh_with_access_token`
- ✅ Rejeita Access Token na rota de refresh
- ✅ Retorna erro específico

#### 6. `test_auth_refresh_invalid_token`
- ✅ Rejeita token malformado
- ✅ Retorna HTTP 401

### Arquivo: `tests/test_security.py` (ATUALIZADO)

#### Testes atualizados para novas mensagens:
- ✅ `test_jwt`: Valida criação de Access Token
- ✅ `test_jwt_invalid_token`: Nova mensagem de erro
- ✅ `test_get_current_user_not_found__exercicio`: Nova mensagem
- ✅ `test_get_current_user_does_not_exists__exercicio`: Nova mensagem

### Resultado dos Testes

```
================================== 11 passed in 1.14s ==================================
Coverage: 67%
```

---

## 📊 Fluxos de Autenticação

### Fluxo 1: Login Inicial

```
Cliente
  ↓
POST /auth/token {email, password}
  ↓
Validar credenciais
  ↓
Gerar Access Token (30min)
Gerar Refresh Token (7 dias)
  ↓
Retornar ambos os tokens
  ↓
Cliente armazena tokens
```

### Fluxo 2: Acesso a Rota Protegida

```
Cliente
  ↓
GET /users
Header: Authorization: Bearer <access_token>
  ↓
get_current_user dependency
  ↓
verify_token(token, type='access')
  ↓
Validar expiração e assinatura
  ↓
Buscar usuário no banco
  ↓
Executar lógica da rota
  ↓
Retornar resposta
```

### Fluxo 3: Renovação de Token

```
Cliente (Access Token expirado)
  ↓
POST /auth/refresh
Header: Authorization: Bearer <refresh_token>
  ↓
verify_token(token, type='refresh')
  ↓
Validar expiração e assinatura
  ↓
Verificar usuário ainda existe
  ↓
Gerar NOVO Access Token (30min)
Gerar NOVO Refresh Token (7 dias)
  ↓
Retornar novos tokens
  ↓
Cliente atualiza tokens armazenados
```

---

## 🎨 Boas Práticas Implementadas

### 1. Separação de Responsabilidades
- ✅ Funções específicas para cada tipo de token
- ✅ Validação centralizada em `verify_token`
- ✅ Router dedicado para autenticação

### 2. Type Hints
```python
def create_access_token(data: dict) -> str
def verify_token(token: str, token_type: str = 'access') -> dict
def get_current_user(...) -> User
```

### 3. Docstrings Completas
```python
"""
Cria um Access Token com curta duração (30 minutos).

Args:
    data: Dicionário com os dados a serem incluídos no token

Returns:
    Token JWT codificado como string
"""
```

### 4. Tratamento de Erros
- ✅ Exceções específicas para cada cenário
- ✅ Mensagens claras e em português
- ✅ Status codes HTTP apropriados

### 5. Dependency Injection
```python
def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
) -> User:
```

---

## 🔄 Migração da Versão Anterior

### Para Clientes da API

#### Antes (v1.0):
```bash
# Login
POST /login
Response: {"access_token": "...", "token_type": "bearer"}

# Uso
GET /users
Header: Authorization: Bearer <access_token>
```

#### Agora (v2.0):
```bash
# Login
POST /auth/token
Response: {
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer"
}

# Uso
GET /users
Header: Authorization: Bearer <access_token>

# Renovação (NOVO)
POST /auth/refresh
Header: Authorization: Bearer <refresh_token>
Response: {
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer"
}
```

### Mudanças Necessárias

1. **Atualizar endpoint de login**: `/login` → `/auth/token`
2. **Armazenar Refresh Token**: Guardar junto com Access Token
3. **Implementar lógica de renovação**: Quando Access Token expirar, usar Refresh Token
4. **Atualizar tratamento de erros**: Novas mensagens de erro

---

## 📈 Melhorias Futuras

### Curto Prazo
- [ ] Mover SECRET_KEY para variável de ambiente
- [ ] Implementar blacklist de tokens (logout)
- [ ] Adicionar rate limiting em `/auth/token`
- [ ] Implementar rotação automática de Refresh Tokens

### Médio Prazo
- [ ] Adicionar suporte a múltiplos dispositivos
- [ ] Implementar revogação de tokens por dispositivo
- [ ] Adicionar logs de autenticação
- [ ] Implementar 2FA (autenticação de dois fatores)

### Longo Prazo
- [ ] Implementar OAuth2 com providers externos (Google, GitHub)
- [ ] Adicionar suporte a scopes e permissões
- [ ] Implementar refresh token rotation
- [ ] Adicionar monitoramento de tentativas de login

---

## 🎓 Conceitos Implementados

### Access Token
- **Propósito**: Autenticação de curto prazo
- **Duração**: 30 minutos
- **Armazenamento**: Memória (não persistir)
- **Uso**: Todas as requisições autenticadas

### Refresh Token
- **Propósito**: Renovação de Access Token
- **Duração**: 7 dias
- **Armazenamento**: Seguro (httpOnly cookie ou secure storage)
- **Uso**: Apenas na rota de refresh

### Por que dois tokens?

1. **Segurança**: Access Token de curta duração limita janela de ataque
2. **Usabilidade**: Refresh Token evita login frequente
3. **Controle**: Possibilidade de revogar sessões específicas
4. **Performance**: Access Token leve para validação rápida

---

## 📝 Conclusão

A refatoração foi concluída com sucesso, implementando um sistema robusto de autenticação JWT com Access Token e Refresh Token. O código está:

✅ **Modular**: Funções separadas e bem definidas  
✅ **Seguro**: Validação rigorosa e mensagens claras  
✅ **Testado**: 11 testes passando com 67% de cobertura  
✅ **Documentado**: Docstrings e comentários completos  
✅ **Escalável**: Pronto para futuras melhorias  

O sistema agora segue as melhores práticas da indústria e está pronto para uso em produção (após configurar SECRET_KEY em variável de ambiente).

---

**Gerado em:** 27/11/2025 21:55  
**Versão do Documento:** 1.0  
**Autor:** Sistema de Refatoração Automatizada
