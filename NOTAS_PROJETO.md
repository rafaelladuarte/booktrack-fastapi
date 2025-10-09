# 🧠 Anotações e Observações de Desenvolvimento

## 📚 Contexto

Este projeto foi desenvolvido com base no curso **[FastAPI do Zero](https://fastapidozero.dunossauro.com/estavel/)**, ministrado por [Dunossauro (Eduardo Mendes)](https://github.com/dunossauro).

O curso serviu como referência principal para compreender os fundamentos de **FastAPI**, **organização de rotas**, **boas práticas de autenticação**, **modelagem de dados com SQLAlchemy** e **estruturação modular de projetos**.

A partir do projeto final apresentado no curso — o **MADR (Meu Acervo de Romancistas)** — este repositório foi **personalizado e expandido** para se tornar algo mais pessoal: um **gerenciador de biblioteca e leituras pessoais**, integrando conceitos de **engenharia de dados**, **modelagem analítica (Star Schema)** e **deploy em nuvem**.

---

## 🧩 Tabela Comparativa — Mapa de Endpoints

| Categoria | Endpoints no Projeto MADR *(curso)* | Endpoints no Projeto BookTrack API *(pessoal)* | Comparativo e observações |
|------------|--------------------------------------|--------------------------------------------------|----------------------------|
| **Autenticação e Usuário** | `/conta`, `/token`, `/refresh-token`, `/me` | `/conta`, `/token`, `/refresh-token`, `/me` | ⚖️ Mesma estrutura — mantido o fluxo de autenticação JWT e refresh token. |
| **Usuário (CRUD)** | Criar, atualizar e deletar conta | Criar, atualizar, deletar conta + flag pública (`perfil_publico`) | 🔧 Expansão: adição de campo “perfil público” para habilitar view pública. |
| **Autores / Romancistas** | `/romancistas` (CRUD) | `/autores` (dim_autor — CRUD simples) | 🧠 Adaptação: foco em autores genéricos, com país e gênero. |
| **Livros** | `/livros` (CRUD com relacionamento a romancistas) | `/livros` (CRUD completo + upload CSV + status + formato) | 🚀 Expansão: novos campos, filtros e importação via CSV. |
| **Coleções** | `/colecoes` (CRUD) | `/colecoes` (dim_colecao — CRUD ou catálogo fixo) | ⚙️ Mantém o conceito, mas estruturado como dimensão referencial. |
| **Gêneros** | `/generos` (CRUD) | `/generos` e `/subgeneros` (dim_genero e dim_subgenero) | 🧩 Expansão da granularidade — gênero e subgênero separados. |
| **Grupos** | `/grupos` (CRUD) | `/grupos` (ex: “Ficção”, “Não Ficção”) | ✅ Mesmo propósito, mas redefinido como categoria ampla. |
| **Biblioteca / Livros do Usuário** | `/biblioteca` (lista livros do usuário autenticado) | `/livros` (lista principal com filtros) | 🔄 Similar, porém com query params mais flexíveis. |
| **Uploads** | — | `/livros/upload-csv` | 🆕 Novo recurso: importação de biblioteca pessoal via CSV. |
| **Status de Leitura** | campo interno (não há endpoint dedicado) | `/livros/{id}` via `PATCH` para status/meta | 🧠 Melhoria: controle granular do progresso de leitura. |
| **View Pública / Biblioteca Pública** | — | `/public/livros`, `/public/livros/{id}` | 🌐 Novo: acesso público parcial ao acervo. |
| **Relatórios / Estatísticas** | `/relatorios` (simples, número de livros) | `/analise/...` (vários endpoints analíticos) | 📊 Expansão: endpoints para consultas analíticas (gênero, ano, status). |
| **Tempo / Datas** | — | `dim_tempo` (usada internamente na modelagem) | 🧮 Inclusão de dimensão temporal — recurso típico de engenharia de dados. |
| **Etiquetas / Tags** | campo dentro de livro | campo `etiqueta` (possível filtro) | ✅ Mantido, com potencial para tags dinâmicas. |
| **Imagens / Capa** | — | campo `capa_url` no livro | 🖼️ Novo campo visual para o frontend. |
| **Frontend** | - | Streamlit App conectado via API | 🎨 Expansão de escopo: integração com frontend interativo. |
| **Banco de Dados** | SQLite (SQLModel) | PostgreSQL (SQLAlchemy) | 🧱 Evolução para banco robusto e normalizado. |
| **Deploy** | Local ou Docker simples | Render + Neon/Supabase + .env | ☁️ Deploy em nuvem, gratuito e documentado. |

---

## 🧠 Resumo Comparativo — Nível de Desafio

| Aspecto | Curso MADR | Projeto BookTrack API |
|----------|-------------|------------------------|
| **Escopo funcional** | 3 entidades (usuário, livro, romancista) | 8 entidades (usuário, livro, autor, gênero, subgênero, coleção, tempo, estante) |
| **Modelo de dados** | Relacional simples | Star Schema (fato + dimensões normalizadas) |
| **Foco** | CRUD literário | Gestão pessoal + análise de leitura |
| **Armazenamento** | SQLite local | PostgreSQL remoto (Neon) | 
| **Deploy** | Local/Docker | Cloud (Render) |
| **Frontend** | - | Streamlit App conectado via API |
| **Engenharia de dados** | - | Importação CSV + modelo analítico |

---

## 💬 Observações Pessoais

Durante o desenvolvimento, optei por expandir o projeto original com:
- **Modelagem em Star Schema**, permitindo análises literárias e agregações por tempo e gênero.  
- **Importação via CSV**, automatizando o carregamento do meu acervo pessoal.  
- **Camada pública**, para que visitantes possam explorar parte da biblioteca sem autenticação.  
- **Integração futura com Streamlit**, criando um painel visual para acompanhar leituras e estatísticas.  

O projeto segue sendo uma oportunidade de **praticar POO, FastAPI e engenharia de dados aplicada**, com foco em **organização, escalabilidade e clareza de código**.
