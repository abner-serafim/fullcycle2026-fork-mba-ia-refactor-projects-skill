# code-smells-project

API de E-commerce em Python/Flask usada como entrada do desafio `refactor-arch`.

## Como rodar

```bash
pip install -r requirements.txt
python app.py
```

A aplicação sobe em `http://localhost:5000`. O banco SQLite (`loja.db`) é criado automaticamente no primeiro boot, já com produtos e usuários de exemplo.

---

### 📄 Análise Manual - Projeto

  * **Problema 1: SQL Injection Generalizado e Vulnerabilidade Crítica de Segurança**
    * **Severidade:** `CRITICAL`
    * **Localização:** `models.py:28` (e repetido nas linhas 37, 49, 78, 91, 108, 122, 137, 187, 194)
    * **Justificativa:** O código realiza concatenação direta de strings recebidas diretamente das requisições HTTP (como o termo de busca `q`, `email`, `senha` e `id`) diretamente dentro das instruções SQL (`WHERE id = " + str(id)` ou `LIKE '%" + termo + "%'`). Isso permite o desvio completo de autenticação e a extração ilícita/destruição de dados de qualquer tabela através de ataques de SQL Injection.


  * **Problema 2: Credenciais e Dados Sensíveis Hardcoded (Exposição de Segredos)**
    * **Severidade:** `CRITICAL`
    * **Localização:** `app.py:7` e `controllers.py:230`
    * **Justificativa:** A chave criptográfica `SECRET_KEY` está explicitada no código fonte como `"minha-chave-super-secreta-123"`. Além disso, o endpoint de `health_check` expõe essa chave e o caminho físico do banco de dados na resposta JSON pública, facilitando ataques direcionados ao ambiente de produção.


  * **Problema 3: Backdoor / Execução Remota de SQL Arbitrário**
    * **Severidade:** `CRITICAL`
    * **Localização:** `app.py:53-73`
    * **Justificativa:** A rota `/admin/query` aceita qualquer código SQL vindo em uma requisição POST e o executa diretamente no banco de dados sem nenhuma validação, barreira de autenticação ou nível de permissão. Funciona efetivamente como um backdoor que permite a qualquer utilizador apagar, ler ou alterar todo o banco de dados de forma arbitrária.


  * **Problema 4: Violação de SOLID e Acoplamento de Infraestrutura (Gargalo N+1)**
    * **Severidade:** `HIGH`
    * **Localização:** `models.py:129-152` (dentro de `get_pedidos_usuario`)
    * **Justificativa:** O método executa novas queries SQL dentro de loops iterativos (`for`) para trazer os itens do pedido e o nome de cada produto, instanciando novos cursores repetidas vezes. Isso configura o anti-pattern de consulta N+1, gerando uma degradação severa de performance que impede o escalonamento do sistema sob carga real.


  * **Problema 5: Armazenamento Inseguro de Senhas (Plain Text)**
    * **Severidade:** `HIGH`
    * **Localização:** `database.py:59-63` e `models.py:91`
    * **Justificativa:** As senhas dos utilizadores são inseridas e comparadas no banco de dados como texto puro (ex: `"admin123"`, `"senha123"`) sem passar por qualquer algoritmo de hashing ou criptografia (como bcrypt ou argon2). Um vazamento básico expõe instantaneamente as credenciais de todas as contas do sistema.


  * **Problema 6: Mistura de Responsabilidades Arquiteturais (God Methods com Regras de Negócio e I/O)**
    * **Severidade:** `MEDIUM`
    * **Localização:** `controllers.py:167-170`
    * **Justificativa:** A camada de controller está a assumir responsabilidades de efeitos colaterais de infraestrutura externa e simulação de serviços, disparando comandos manuais no meio do fluxo como `print("ENVIANDO EMAIL...")`, `print("ENVIANDO SMS...")`. Estes acoplamentos deveriam estar abstraídos em serviços de notificação dedicados.


  * **Problema 7: Falta de Tratamento de Erros Estruturado e Vazamento de Exceções**
    * **Severidade:** `MEDIUM`
    * **Localização:** `controllers.py` (Múltiplos blocos `except Exception as e`)
    * **Justificativa:** Todos os erros capturados são devolvidos diretamente na resposta HTTP com `jsonify({"erro": str(e)})`. Retornar a string bruta de exceções internas do sistema operacional ou banco de dados expõe as entranhas da nossa infraestrutura para atacantes.


  * **Problema 8: Magic Numbers e Lógica de Negócio Acoplada no Model**
    * **Severidade:** `LOW`
    * **Localização:** `models.py:175-181` (Cálculo de descontos dentro do relatório)
    * **Justificativa:** O modelo possui uma série de regras condicionais de desconto com valores fixos e inexplicados (`10000`, `5000`, `1000`, `0.1`, `0.05`, `0.02`) diretamente no código. Viola o princípio de responsabilidade única e dificulta a parametrização do faturamento comercial.

