# FastAPI do Zero

## Aula 3 - Estruturando o projeto e criando rotas CRUD


### CRUD

* C = CREATE
* R = READ
* U = UPDATE
* D = DELETE

### HTTP

#### Verbos

POST: é usado para solicitar que o servidor aceite um dado (recurso) enviado pelo cliente.
GET: é usado para quando o cliente deseja requisitar uma informação do servidor.
PUT: é usando no momento em que o cliente deseja informar alguma alteração nos dados para o servidor.
DELETE: usado para dizer ao servidor que delete determinado recurso.

#### Respostas

* 200 OK: Indica sucesso na requisição.
    * GET: Quando um dado é solicitado e retornado com sucesso.
    * PUT: Quando dados são alterados com sucesso.
* 201 CREATED: Significa que a solicitação resultou na criação de um novo recurso.
    * POST: Aplicável quando um dado é enviado e criado com sucesso.    
    * PUT: Usado quando uma alteração resulta na criação de um novo recurso.
* 204 NO CONTENT: Retorno do servidor sem conteúdo na mensagem.
    * PUT: Aplicável se a alteração não gerar um retorno.
    * DELETE: Usado quando a ação de deletar não gera um retorno.
* 404 NOT FOUND: O recurso solicitado não pôde ser encontrado.
* 422 UNPROCESSABLE ENTITY: o pedido foi bem formado (ou seja, sintaticamente correto), mas não pôde ser processado.
* 500 INTERNAL SERVER ERROR: Uma mensagem de erro genérica, dada quando uma condição inesperada foi encontrada. Geralmente ocorre quando nossa aplicação apresenta um erro.


### Aprofundamento nos estudos

* [Pytest Fixtures - Live de Python #168](https://youtu.be/sidi9Z_IkLU)
* [SQLAlchemy: conceitos básicos, uma introdução a versão 2 | Live de Python #258](https://www.youtube.com/watch?v=t4C1c62Z4Ag)
* [Migrações, bancos de dados evolutivos (Alembic e SQLAlchemy) | Live de Python #211](https://www.youtube.com/watch?v=yQtqkq9UkDA)
* [Variáveis de ambiente, dotenv, constantes e configurações | Live de Python #207](https://www.youtube.com/watch?v=DiiKff1z2Yw)
