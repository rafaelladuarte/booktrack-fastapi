# FastAPI do Zero

## Configurando o banco de dados e gerenciando migrações com Alembic

### Conceitos

* **ORM**

Significa Object-Relational Mapping, é uma técnica de programação que mapeia objetos de banco de dados em objetos de alguma linguagem de programação, no nosso caso é para objetos Python.

É importante utilizar um ORM na aplicação, pois ela abstrai o banco de dados, permitindo que mudemos o tipo de banco de dados para outro sem precisar alterar o codigo; garante maior segurança evitantdo injeções SQL; e permite maior eficiência no desenvolvimento, pois eles geram schemas de modelos de dados facilitando a migração.

* **12 FactorAPP**

É uma boa prática no desenvolvimento separar as configurações do códito, principalmente dados sensiveis como credenciais de banco de dado.
Essa prática busca aumentar a segurança da aplicação e facilitar a configuração de variaveis de ambientes quando o for necessário mudar a aplicação de ambiente, como por exemplo, do ambiente de desenvolvimento para o de produção.

### SQLalchemy

É um ORM do Python, que permite trabalhar com bancos de dados SQL com métodos e atributos Python.

### Alembic

O Alembic é uma ferramenta de migração de banco de dados para o SQLAlchemy.

* Iniciar projeto de migração

```
alembic init migrations
```

* Criar a migração

```
alembic revision --autogenerate -m "create users table"
```

### SQLite

* Abrir console do SQLite no terminal

```
python -m sqlite3 database.db 
```

![alt text](/docs/images/image-5.png)

### Aprofundamento nos estudos
* [Aplicação doze-fatores 12FactorApp | Live de Python #104](https://youtu.be/DA-hOskxOxE)
* [SQLAlchemy: conceitos básicos, uma introdução a versão 2 | Live de Python #258](https://youtu.be/t4C1c62Z4Ag)
* [Migrações, bancos de dados evolutivos (Alembic e SQLAlchemy) | Live de Python #211](https://youtu.be/yQtqkq9UkDA)


