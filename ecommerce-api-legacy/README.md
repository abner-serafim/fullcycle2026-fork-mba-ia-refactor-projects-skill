# ecommerce-api-legacy

LMS API (com fluxo de checkout) em Node.js/Express usada como entrada do desafio `refactor-arch`.

## Como rodar

```bash
npm install
npm start
```

A aplicação sobe em `http://localhost:3000`. O banco SQLite é em memória e já carrega seeds automaticamente no boot.

Exemplos de requisições estão em `api.http`.


---

### 📄 Análise Manual - Projeto

  * **Problema 1: Exposição Crítica de Segredos de Produção (Hardcoded Credentials)**
    * **Severidade:** `CRITICAL`
    * **Localização:** `utils.js:2-5`
    * **Justificativa:** Credenciais de alta sensibilidade de infraestrutura e produção estão expostas diretamente em texto puro no código fonte do ficheiro de utilitários, incluindo o utilizador administrador do banco de dados (`dbUser`), a palavra-passe principal (`dbPass`) e o token privado real da gateway de pagamentos (`paymentGatewayKey`). Isto viola qualquer conformidade mínima de segurança, permitindo o comprometimento do negócio caso o código seja publicado.


  * **Problema 2: Criptografia Fraca / Vulnerabilidade de Algoritmo de Hash Caseiro**
    * **Severidade:** `CRITICAL`
    * **Localização:** `utils.js:18-24` (invocado em `AppManager.js:84`)
    * **Justificativa:** A função `badCrypto` implementa um algoritmo personalizado de hashing baseado na conversão contínua para Base64 truncada. Base64 é um método de codificação, não de hashing. A truncagem e a falta de salgamento (*salt*) produzem colisões altíssimas e extrema facilidade de engenharia reversa por ataques de dicionário ou força bruta. Além disso, a semente padrão `"123"` para o utilizador inicial (`initDb`) agrava a falha.


  * **Problema 3: Anti-Pattern de Arquitetura Monolítica Acoplada (God Class / Callback Hell)**
    * **Severidade:** `HIGH`
    * **Localização:** `AppManager.js` (Especialmente o endpoint `/api/checkout` nas linhas 32-94)
    * **Justificativa:** A classe `AppManager` viola inteiramente o Princípio da Responsabilidade Única (SOLID) e o padrão MVC. Ela é responsável por inicializar a infraestrutura do banco de dados, configurar o roteamento do Express, gerir regras complexas de negócio (como o fluxo transacional de checkout), interagir com I/O de terceiros e manipular logs locais dentro de um encadeamento profundo de funções de retorno (*callbacks*) aninhadas. Isso torna a escrita de testes unitários isolados impossível.


  * **Problema 4: Grave Ineficiência de Desempenho (Query N+1 em Cascata Aninhada)**
    * **Severidade:** `HIGH`
    * **Localização:** `AppManager.js:96-141` (no endpoint `/api/admin/financial-report`)
    * **Justificativa:** Para gerar um relatório financeiro, o sistema executa um loop (`forEach`) que faz chamadas assíncronas ao banco de dados para cada curso; dentro desse loop, faz outro para as matrículas; e dentro deste último, faz mais duas consultas individuais para obter o utilizador e o pagamento correspondente. Este encadeamento exponencial de I/O bloqueia o loop de eventos do Node.js sob volumetria de dados e degrada severamente o servidor. Deveria ser mitigado por uma instrução SQL unificada com `JOIN`.


  * **Problema 5: Inconsistência de Dados e Violação de Chave Estrangeira (Registos Órfãos)**
    * **Severidade:** `MEDIUM`
    * **Localização:** `AppManager.js:143-149` (no endpoint `/api/users/:id`)
    * **Justificativa:** O endpoint executa uma deleção física direta da tabela `users` baseada no ID fornecido. Contudo, não limpa em cascata e nem valida de forma lógica as tabelas dependentes (`enrollments` e `payments`), mantendo registos órfãos corrompidos que gerarão erros fatais de referência nula nas listagens de relatórios subsequentes (como já evidenciado pelo tratamento paliativo `student: user ? user.name : 'Unknown'` na linha 125).


  * **Problema 6: Vazamento de Memória (Memory Leak) por Cache Incondicional**
    * **Severidade:** `MEDIUM`
    * **Localização:** `utils.js:8` e `utils.js:13-16`
    * **Justificativa:** A função `logAndCache` insere indefinidamente entradas no objeto em memória `globalCache` sempre que um checkout ocorre. Como este objeto nunca possui uma política de expiração (TTL), limpeza ou tamanho máximo limitado (LRU), a memória consumida pela aplicação crescerá indefinidamente de forma linear com o uso da API, levando à indisponibilidade por esgotamento de memória (*Out Of Memory*).


  * **Problema 7: Nomenclatura de Variáveis Abstrata e Ofuscada**
    * **Severidade:** `LOW`
    * **Localização:** `AppManager.js:33-37`
    * **Justificativa:** O desestruturamento de dados recebidos no corpo da requisição HTTP foi implementado utilizando variáveis com nomes genéricos e de única letra (`u`, `e`, `p`, `cid`, `cc`). Reduz significativamente a legibilidade e a manutenibilidade do código para o ecossistema de engenharia.


