# 📖 BookTrack API – Gerenciador de Leitura Pessoal e Análises Literárias

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Em%20desenvolvimento-yellow?style=for-the-badge)



## 🧩 Descrição

**BookTrack API** é uma aplicação backend desenvolvida em **FastAPI** para o gerenciamento e análise de uma biblioteca pessoal.  
O sistema permite cadastrar livros, acompanhar o progresso de leitura, importar coleções via **CSV** e gerar análises literárias por gênero, autor e status de leitura.  

Além de servir como ferramenta pessoal, o projeto oferece uma **view pública limitada**, possibilitando que terceiros explorem parte do acervo de forma segura.

A modelagem segue o padrão **Star Schema**, integrando conceitos de **engenharia de dados** e **boas práticas de APIs REST**.  
Este projeto foi idealizado como um estudo prático de **POO em Python**, **FastAPI**, **modelagem de dados** e **deploy em nuvem**.

---

## 🗂️ Estrutura do Projeto

```

booktrack_api/
├── .gitignore
└── README.md

````

---

## 🚀 Funcionalidades

| Categoria | Descrição |
|------------|------------|
| **Usuários** | Cadastro, autenticação (JWT), atualização de perfil e controle de acesso. |
| **Livros** | CRUD completo com campos como título, autor, gênero, status, formato, e capa. |
| **Importação CSV** | Upload de coleções pessoais para importação automática de livros. |
| **Autores** | Cadastro e listagem de autores com país e gênero. |
| **Coleções / Gêneros** | CRUD e categorização de obras. |
| **Status de leitura** | Controle de leitura (Fila, Em andamento, Concluído). |
| **Análises e Relatórios** | Endpoints para análise por gênero, origem, status e ano de publicação. |
| **View pública** | Permite o acesso limitado de terceiros à biblioteca (sem autenticação). |

---

## 🧠 Modelagem de Dados (Star Schema)

**Tabela Fato:**  
`fato_leitura` — contém os registros principais dos livros e progresso de leitura.

**Tabelas Dimensão:**
- `dim_autor`
- `dim_genero`
- `dim_subgenero`
- `dim_colecao`
- `dim_tempo`
- `dim_editora`
- `dim_usuario`

Essa modelagem facilita análises de leitura por tempo, gênero, origem e formato, aproximando o projeto de um **modelo analítico** (OLAP).

---

## 🛠️ Ferramentas e Tecnologias

- **Linguagem:** Python 3.12+
- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Banco de Dados:** PostgreSQL (Neon)
- **Deploy:** Render (API) + Neon (DB)
- **Contêineres:** Docker & Docker Compose
- **Autenticação:** JWT (via OAuth2)
- **Validação:** Pydantic
- **Testes:** Pytest
- **Documentação:** Swagger UI / Redoc

---

## ⚙️ Como Executar Localmente

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/rafaelladuarte/booktrack_api.git
cd booktrack_api
````

### 2️⃣ Criar e configurar o arquivo `.env`

```bash
cp .env.example .env
```

Preencha com suas credenciais do banco de dados PostgreSQL e outras variáveis sensíveis.

### 3️⃣ Subir com Docker

```bash
docker compose up --build
```

A API estará disponível em:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🌐 Deploy Gratuito

**API:** [Render.com](https://render.com)
**Banco de Dados:** [Neon.tech](https://neon.tech)
**Armazenamento de mídia (futuro):** Cloudinary ou Supabase Storage

---

## 🧩 Próximos Passos

* [ ] Implementar importação de CSV com validação automática
* [ ] Criar endpoints analíticos (agregações e filtros)
* [ ] Adicionar testes unitários e de integração
* [ ] Deploy completo (Render + Neon)
* [ ] Integração com o app Streamlit (frontend do usuário)

---

## 💡 Objetivo do Projeto

Consolidar conhecimentos em:

* Programação Orientada a Objetos em Python
* Desenvolvimento de APIs REST com FastAPI
* Modelagem relacional e analítica (Star Schema)
* Boas práticas de deploy e organização de código
* Construção de portfólio técnico voltado à engenharia de dados

---

## 👩‍💻 Autora

**Rafaella Duarte**
[GitHub](https://github.com/rafaelladuarte) • [LinkedIn](https://linkedin.com/in/rafaelladuarte)

---

> *"Build systems that tell stories — each dataset is a bookshelf waiting to be explored."* ✨

```

---

Se quiser, posso gerar a **versão com emojis e ícones otimizados para README do GitHub (com links clicáveis, seções recolhíveis e badges de status)** — ideal para deixar o repositório mais chamativo visualmente.  

Quer que eu monte essa **versão aprimorada visualmente** do README?
```
