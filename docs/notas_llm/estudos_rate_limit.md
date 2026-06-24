# Notas de Estudo: Rate Limiting com FastAPI + SlowAPI + Redis

Este documento consolida os aprendizados sobre a implementação de Rate Limiting (limitação de requisições) em uma API construída com FastAPI.

## 1. O que é e Por que usar?
**Rate Limiting** é um mecanismo de defesa essencial em APIs. Ele limita a quantidade de requisições que um cliente pode fazer em um determinado período (ex: `30/minute`). 
- **Objetivos:** Prevenir ataques de força-bruta (ex: ficar tentando senhas infinitamente na rota de login), evitar ataques de negação de serviço (DDoS) e garantir que clientes "fominhas" não esgotem os recursos do servidor (banco de dados, CPU), prejudicando os demais.

---

## 2. Identificação de Usuários (`get_user_identifier`)
Para que o servidor saiba quem está consumindo as cotas, implementamos uma função customizada de identificação. Ela possui uma abordagem híbrida:
1. **Para Usuários Logados:** Se a requisição contiver um Token JWT (Header `Authorization`), a função extrai o e-mail (campo `sub`). Isso garante que a cota seja vinculada à conta real. Se o usuário mudar de Wi-Fi para 4G (mudando de IP), a cota o acompanha, impedindo que ele burle o limite.
2. **Para Visitantes (Fallback):** Se não houver token (ex: na rota `/auth/token`), o sistema utiliza o IP do dispositivo (`get_remote_address`). Isso é vital para travar IPs maliciosos tentando quebrar senhas.

### Otimização: A Leitura "Cega" do JWT
Na função de identificação, utilizamos `verify_signature=False` para abrir o token. 
- **O Motivo:** Segurança é responsabilidade do FastAPI (`get_current_user`), enquanto a contagem é responsabilidade do SlowAPI. Validar criptografia consome muita CPU. Se validássemos o token ali, o servidor faria o trabalho pesado 2 vezes seguidas.
- **E se alguém mandar um token falso?** O SlowAPI "anota" a requisição pro token falso, deixa passar, e milissegundos depois, a barreira do FastAPI (`Depends`) bloqueia o invasor com o erro `401 Unauthorized` por assinatura inválida. Nenhuma vulnerabilidade é exposta, e economizamos recursos.

---

## 3. O que são Decorators (`@`) e o parâmetro `Request`
Usamos o decorator `@limiter.limit('30/minute')` nas rotas.
- **A Metáfora do "Segurança":** Um decorator no Python é uma função que "abraça" e monitora a sua rota. Ele age como um segurança de balada: fica na porta, confere a identidade (IP ou Token), olha no sistema (Redis) e, se a cota estourou, ele nem deixa a pessoa chegar na festa (o corpo da sua função com a lógica de banco de dados). Ele veta e devolve um erro imediato (`429 Too Many Requests`).
- **O parâmetro `request: Request`:** Para que o "segurança" faça o trabalho dele, ele precisa das credenciais de quem tenta entrar. O FastAPI não passa os Headers e IP automaticamente por motivos de performance. Precisamos declarar a variável `request` na assinatura da rota para que a biblioteca do SlowAPI consiga inspecionar a conexão.

---

## 4. Conflitos de Headers (O "Pulo do Gato" do SlowAPI)
O SlowAPI tem um recurso de injetar cabeçalhos nas requisições (como o `Retry-After`, que diz ao cliente quantos segundos esperar). Porém, ele tenta injetar isso no "objeto de retorno" da rota. 
- **O Problema:** No FastAPI, retornamos dados puros (como dicionários `{"detail": "Success"}`) e o próprio FastAPI converte isso em uma classe `Response` nos bastidores *depois* que a rota acaba. O SlowAPI tentava colocar os cabeçalhos em um dicionário, o que gerava um "Crash" (erro 500) na API.
- **A Solução:** Desligamos o `headers_enabled=False` no construtor do Limiter e criamos nosso próprio `custom_rate_limit_exceeded_handler`. Nele, sempre que a cota esgota, nós calculamos na mão o tempo restante usando as funções do Limiter e devolvemos a resposta HTTP `429` com o cabeçalho correto formatado, garantindo um código funcional e dentro dos padrões.

---

## 5. Como testar de forma segura (`pytest` + Infraestrutura)
Testes devem ser previsíveis, repetíveis e não devem sujar o ambiente de produção/desenvolvimento.

1. **Bancos "In-Memory" (SQLite):** Nossos testes utilizam URLs do tipo `sqlite+aiosqlite:///:memory:`. Isso significa que, ao rodar `pytest`, é erguido um banco inteiro e vazio na memória RAM do seu computador. Quando o teste acaba, ele some. Seu Postgres configurado no Docker fica totalmente intocado.
2. **Conflito de Cotas no Redis (`clear_redis`):** Como os testes rodavam muito rápido (frações de segundo), eles esgotavam rapidamente a cota minúscula de segurança da rota de Login (`10/minuto`). Para evitar isso, criamos a fixture assíncrona `clear_redis` configurada com `autouse=True`. 
   - **O que ela faz?** Antes de *todo* teste iniciar, ela conecta no Redis (onde as contagens do limitador são armazenadas) e dá um `flushdb()`, zerando a memória do Rate Limiter. Isso zera as estatísticas do servidor de desenvolvimento local, mas é completamente aceitável e garante que todo teste execute de forma limpa, justa e sem "falsos bloqueios".
