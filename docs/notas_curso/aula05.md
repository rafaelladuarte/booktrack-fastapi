# FastAPI do Zero

## Integrando banco de dados à API

### Integrando SQLAlchemy à Nossa Aplicação FastAPI

As interações do SQLAlchemy no Banco de Dados, acontece por meio de sessões, que funciona de forma semelhante ao commit dos Banco de Dados para confirmar as alterações feitas.

A sessão no SQLAlchemy possui três padrões de arquitetura:

* Mapa de Identidade: é o que garante que cada objeto na sessão seja único e facilmente identificável.
* Repositório: é o que controla todas as comunicações entre o código Python e o Banco de Dados.
* Unidade de Trabalho: é o que controla todas as alterações que queremos fazer no Banco de Dados.

### Gerenciando Dependências com FastAPI

* Injeção de Dependência

É um padrão arquiteturial que permite que mantenhamos um baixo nível de acoplamente entre diferentes módulos de um sistema.As dependências entre os módulos não são definidas no código, mas sim pela configuração de uma infraestrutura de software (container) responsável por "injetar" em cada componente suas dependências declaradas.

Ou seja, em vez de cada parte do nosso código ter que criar suas próprias instâncias de classes ou serviços de que depende, essas instâncias são criadas uma vez e depois injetadas onde são necessárias.

* Função `Depends` do FastAPI

O FastAPI para gerencias as dependências, forneceu a função `Depends` onde podemos declara-la para que antes de executarmos uma função especifica, executamos primero outra função que é chamada pelo `Depends`.