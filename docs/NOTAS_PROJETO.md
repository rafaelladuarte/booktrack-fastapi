# 🧠 Anotações e Observações de Desenvolvimento

## 📚 Contexto

Este projeto foi desenvolvido com base no curso **[FastAPI do Zero](https://fastapidozero.dunossauro.com/estavel/)**, ministrado por [Dunossauro (Eduardo Mendes)](https://github.com/dunossauro).

O curso serviu como referência principal para compreender os fundamentos de **FastAPI**, **organização de rotas**, **boas práticas de autenticação**, **modelagem de dados com SQLAlchemy** e **estruturação modular de projetos**.

A partir do projeto final apresentado no curso, o **MADR (Meu Acervo de Romancistas)**, este repositório foi **personalizado e expandido** para se tornar algo mais pessoal: um **gerenciador de biblioteca e leituras pessoais**, integrando conceitos de **engenharia de dados**, **modelagem analítica (Star Schema)** e **deploy em nuvem**.


## 🧩 Tabela Comparativa - Mapa de Endpoints

Perfeito 👍 Aqui está a **versão condensada da tabela comparativa**, mostrando apenas as colunas: **Categoria**, **Projeto MADR**, e **Proposta Simplificada (BookTrack API)** — ideal para documentação técnica mais direta 👇


| **Category**                    | **MADR Project (old)**                      | ✅ **Simplified Proposal (BookTrack API)** |
| ------------------------------- | ------------------------------------------- | ----------------------------------------- |
| **Authentication**              | `/conta`, `/token`, `/refresh-token`, `/me` | `/token`, `/refresh-token`                |
| **User**                        | —                                           | `/account`, `/me`                         |
| **Properties**                  | `/romancistas`                              | `/properties`, `/properties/{name}`       |
| **Categories**                  | —                                           | `/categories/{parent_id}`                 |
| **Books**                       | `/livros`                                   | `/books`, `/books/{id}`, `/books/public`  |
| **Readings**                    | `/biblioteca`                               | `/readings`, `/readings/{id}`             |
| **Recommendations (AI/Markov)** | —                                           | `/recommendations`                        |
| **Reports / Analytics**         | `/relatorios`                               | `/analytics`                              |
| **Upload**                      | —                                           | `/books/upload-csv`                       |
---


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

