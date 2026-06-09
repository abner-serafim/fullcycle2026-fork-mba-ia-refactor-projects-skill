# task-manager-api

API de Task Manager em Python/Flask usada como entrada do desafio `refactor-arch`. Diferente dos outros projetos, este já possui alguma separação de camadas (`models/`, `routes/`, `services/`, `utils/`), mas ainda contém problemas arquiteturais e de qualidade.

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python seed.py
python app.py
```

A aplicação sobe em `http://localhost:5000`. O `seed.py` popula o banco SQLite (`tasks.db`) com usuários, categorias e tasks de exemplo — **rode-o antes do primeiro boot**, caso contrário os endpoints vão retornar listas vazias.

---

### 📄 Análise Manual - Projeto

* **Problema 1: Exposição de Credenciais e Palavras-passe Hardcoded em Serviços**
  * **Severidade:** `CRITICAL`
  * **Localização:** `services/notification_service.py:11-12` e `app.py:14`
  * **Justificativa:** O serviço de notificações expõe de forma estática o utilizador (`taskmanager@gmail.com`) e a palavra-passe real de autenticação (`senha123`) do servidor SMTP do Gmail. Adicionalmente, a `SECRET_KEY` da aplicação está embutida diretamente no ponto de entrada (`app.py`). Segredos de infraestrutura devem ser obrigatoriamente injetados via variáveis de ambiente (`.env`) para mitigar o roubo de credenciais em repositórios.


* **Problema 2: Criptografia Obsoleta e Vulnerável (Uso de MD5 para Hashing de Senhas)**
  * **Severidade:** `CRITICAL`
  * **Localização:** `models/user.py:27` e `models/user.py:30`
  * **Justificativa:** O método `set_password` utiliza o algoritmo `hashlib.md5()` para cifrar as credenciais de acesso dos utilizadores. O MD5 é uma função de hash obsoleta e criptograficamente quebrada, suscetível a ataques rápidos de colisão e tabelas de busca pré-computadas (*Rainbow Tables*). Além disso, não é utilizado nenhum mecanismo de *salt* (salgamento). Deve ser atualizado para `bcrypt` ou `argon2`.


* **Problema 3: Vazamento Crítico de Dados de Autenticação (Exposição de Password na Resposta)**
  * **Severidade:** `HIGH`
  * **Localização:** `models/user.py:16` (invocado em `routes/user_routes.py:31` e `routes/user_routes.py:146`)
  * **Justificativa:** O método de serialização do modelo `to_dict()` inclui explicitamente o campo `'password'` no dicionário de retorno. Ao consultar os detalhes de um perfil ou efetuar o login com sucesso, a aplicação envia o hash MD5 da palavra-passe diretamente na resposta JSON pública exposta à rede. Dados de credenciais nunca devem transitar nas respostas da API.


* **Problema 4: Degradação de Performance por Ineficiência em Loop (Problema N+1 com ORM)**
  * **Severidade:** `HIGH`
  * **Localização:** `routes/task_routes.py:27` e `routes/task_routes.py:35`
  * **Justificativa:** Ao listar as tarefas no endpoint `/tasks`, o código itera sobre cada registo e executa consultas adicionais síncronas de forma explícita (`User.query.get(t.user_id)` e `Category.query.get(t.category_id)`) para injetar os nomes do utilizador e da categoria. Isso gera uma ineficiência clássica de I/O de padrão N+1 que anula os benefícios de carregamento otimizado do SQLAlchemy, multiplicando as requisições ao banco concorrentemente.


* **Problema 5: Violação das Camadas do MVC (Regras de Apresentação e Mapeamento Incorretas)**
  * **Severidade:** `MEDIUM`
  * **Localização:** `routes/task_routes.py:19-25` e `routes/report_routes.py:35-43`
  * **Justificativa:** A camada de roteamento (`routes`) está a assumir responsabilidades de cálculo lógico de atraso de tarefas (`overdue`) com comparações diretas de timestamps (`datetime.utcnow()`), além de montar manualmente estruturas de mapeamento complexas e cálculos estatísticos que deveriam estar encapsulados na camada Controller.


* **Problema 6: Captura de Exceções Oculta com Retorno Genérico (Mascaramento de Falhas)**
  * **Severidade:** `LOW`
  * **Localização:** `routes/task_routes.py:53-54`
  * **Justificativa:** O bloco try/except captura qualquer erro de forma genérica (`except:`) sem realizar nenhum tipo de registo de log interno (como `logging.error`), devolvendo simplesmente uma mensagem estática de `'Erro interno'`. Isso oculta falhas reais da base de dados e dificulta imenso a rastreabilidade e a depuração de problemas em ambiente produtivo.
