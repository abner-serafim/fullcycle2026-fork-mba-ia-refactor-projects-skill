# Walkthrough - Refatoração do code-smells-project

Concluímos a reestruturação arquitetural completa do projeto `code-smells-project` aplicando o padrão Model-View-Controller (MVC) e mitigando todos os problemas de segurança e performance mapeados na auditoria.

## Mudanças Realizadas

1. **Separação de Responsabilidades (MVC)**:
   - Dividimos a lógica que estava misturada em `models.py`, `controllers.py` e rotas inline do `app.py` em subpastas estruturadas:
     - `config/settings.py`: Gerenciamento centralizado de configurações e carregamento de variáveis de ambiente.
     - `models/`: Contém os acessos estruturados ao banco de dados para `produto`, `usuario` e `pedido`.
     - `controllers/`: Recebe as requisições HTTP, valida os parâmetros e delega para as entidades de dados e serviços correspondentes.
     - `routes/`: Define endpoints de forma limpa usando Blueprints do Flask.
     - `services/`: Criado `notification_service.py` para isolar efeitos colaterais de mensagens e notificações.

2. **Segurança Mitigada**:
   - **SQL Injection**: Reescrevemos todas as queries brutas concatenadas para usar consultas parametrizadas do SQLite com tuplas de parâmetros (`?`), blindando a aplicação contra injeção SQL.
   - **Backdoor `/admin/query`**: Desabilitado por padrão e controlado via flag `ENABLE_ADMIN_QUERY` configurável de forma segura via variáveis de ambiente.
   - **Senhas em texto plano**: Implementamos criptografia bcrypt para senhas de usuários. Toda senha criada no cadastro ou na migração do seed é hasheada, e o login valida os hashes usando `bcrypt.checkpw`.
   - **Exposição de Segredos**: O segredo (`SECRET_KEY`) agora é extraído do `.env`. O endpoint `/health` foi limpo para não mais vazar informações internas ou chaves.
   - **Vazamento de Erros**: Os controllers tratam exceções internamente, registrando no terminal/log a stack real e retornando uma mensagem genérica limpa e segura nas respostas da API.

3. **Performance Otimizada**:
   - **N+1 Query Loop**: Reescrevemos as buscas de pedidos (`get_pedidos_usuario` e `get_todos_pedidos`) para consultar a tabela de itens e produtos usando um único `LEFT JOIN` com uma cláusula `IN`. Isso reduziu o tráfego e acesso I/O de O(N) queries consecutivas para O(1) query agregada.

## Verificação e Testes

- Criamos uma suite de testes unitários automatizados em `test_api.py` cobrindo todos os fluxos da API:
  - Verificação de `/health` segura.
  - Listagem e busca parametrizada de produtos.
  - Cadastro de usuários e login com hash bcrypt.
  - Criação de pedidos e validação da resolução de N+1.
  - Bloqueio de segurança da rota `/admin/query`.
- Removemos os arquivos obsoletos `controllers.py` e `models.py`.
