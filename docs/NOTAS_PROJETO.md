# 🧠 Anotações e Observações de Desenvolvimento

## 📚 Contexto

Este projeto foi desenvolvido com base no curso **[FastAPI do Zero](https://fastapidozero.dunossauro.com/estavel/)**, ministrado por [Dunossauro (Eduardo Mendes)](https://github.com/dunossauro).

O curso serviu como referência principal para compreender os fundamentos de **FastAPI**, **organização de rotas**, **boas práticas de autenticação**, **modelagem de dados com SQLAlchemy** e **estruturação modular de projetos**.

A partir do projeto final apresentado no curso, o **MADR (Meu Acervo de Romancistas)**, este repositório foi **personalizado e expandido** para se tornar algo mais pessoal: um **gerenciador de biblioteca e leituras pessoais**, integrando conceitos de **engenharia de dados**, **modelagem analítica (Star Schema)** e **deploy em nuvem**.


## 🧩 Tabela Comparativa - Mapa de Endpoints

| Categoria                             | Endpoints no Projeto MADR        | Endpoints no Projeto BookTrack API    | Comparativo e observações                                             |
| ------------------------------------- | ------------------------------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **Autenticação e Usuário**            | `/conta`, `/token`, `/refresh-token`, `/me` | `/api/v1/conta`, `/api/v1/token`, `/api/v1/refresh-token`, `/api/v1/me` | ⚖️ Mantém o fluxo de autenticação JWT.                                |
| **Usuário (CRUD)**                    | Criar, atualizar e deletar conta            | Mesmo conjunto + flag `perfil_publico`                                  | 🔧 Expansão para controle de visibilidade pública.                    |
| **Autores**                           | `/romancistas` (CRUD)                       | `/api/v1/autores` (GET, POST, PATCH)                                    | 🧠 Adaptação para autores genéricos com país/gênero.                  |
| **Editoras**                          | —                                           | `/api/v1/editoras` (GET, POST, PATCH)                                   | 🆕 Novo catálogo mestre.                                              |
| **Livros**                            | `/livros` (CRUD)                            | `/api/v1/livros` (GET, POST, PATCH, DELETE) + upload CSV opcional       | 📚 Recurso principal — CRUD completo, filtros e importação.           |
| **Leituras**                          | `/biblioteca` (lista livros do usuário)     | `/api/v1/livros/{livro_id}/leituras` e `/api/v1/leituras/{leitura_id}`  | 🔄 Reorganizado: leitura é um recurso independente vinculado a livro. |
| **Etiquetas (catálogo)**              | campo dentro de livro                       | `/api/v1/etiquetas` (GET, POST, PATCH)                                  | 🏷️ Agora entidade de catálogo mestre.                                |
| **Etiquetas ↔ Leituras (N:N)**        | —                                           | `/api/v1/leituras/{leitura_id}/etiquetas` (GET, POST, DELETE)           | 🔗 Novo relacionamento N:N contextualizado por leitura.               |
| **Estantes (catálogo)**               | —                                           | `/api/v1/estantes` (GET, POST, PATCH)                                   | 📚 Novo catálogo mestre.                                              |
| **Estantes ↔ Leituras (N:N)**         | —                                           | `/api/v1/leituras/{leitura_id}/estantes` (GET, POST, DELETE)            | 🔗 Associação de leituras a estantes.                                 |
| **Categorias**                        | `/generos`                                  | `/api/v1/categorias` (GET, POST, PATCH)                                 | 🧩 Expansão: categorias hierárquicas.                                 |
| **Formatos**                          | —                                           | `/api/v1/formatos` (GET)                                                | 🧱 Lista fixa de formatos de leitura.                                 |
| **Status de Leitura**                 | campo interno                               | `/api/v1/status` (GET)                                                  | ✅ Catálogo fixo de status (“Lendo”, “Concluído” etc.).                |
| **View Pública / Biblioteca Pública** | —                                           | `/api/v1/public/livros`, `/api/v1/public/livros/{id}`                   | 🌐 Acesso público opcional a perfis com `perfil_publico = true`.      |
| **Recomendações (Cadeia de Markov)**  | —                                           | `/api/v1/recommendations/{user_id}`                                     | 🧠 Novo endpoint: recomenda livros com base em histórico (Markov).    |
| **Relatórios / Estatísticas**         | `/relatorios`                               | `/api/v1/analise/...` (por gênero, status, ano etc.)                    | 📊 Expansão com endpoints analíticos.                                 |
| **Tempo / Datas (dimensão interna)**  | —                                           | `dim_tempo` (uso interno no modelo)                                     | 🧮 Mantido como referência analítica.                                 |
| **Uploads**                           | —                                           | `/api/v1/livros/upload-csv`                                             | 🆕 Importação rápida da biblioteca pessoal.                           |

## 🧠 Resumo Comparativo — Nível de Desafio

| Aspecto                 | Curso MADR                               | Projeto BookTrack API                                                               |
| ----------------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Escopo funcional**    | 3 entidades (usuário, livro, romancista) | 10+ entidades (usuário, livro, leitura, autor, editora, categoria, etiqueta, estante, formato, status) |
| **Modelo de dados**     | Relacional simples                       | Star Schema (tabela fato `leituras` + dimensões normalizadas)                                          |
| **Foco**                | CRUD literário básico                    | Gestão pessoal de leitura + análise + recomendação inteligente                                         |
| **Armazenamento**       | SQLite local                             | PostgreSQL remoto (Neon/Supabase)                                                                      |
| **Deploy**              | Local/Docker                             | Cloud (Render) com variáveis `.env`                                                                    |
| **Frontend**            | —                                        | Streamlit App conectado à API REST                                                                     |
| **Engenharia de dados** | —                                        | Importação via CSV, modelo analítico (dimensões) e recomendação via Cadeia de Markov                   |
| **Complexidade geral**  | Baixa — CRUD e autenticação básica       | Alta — múltiplas relações N:N, análise estatística e lógica de recomendação probabilística             |

