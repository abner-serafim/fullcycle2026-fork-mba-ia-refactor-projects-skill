# Walkthrough de Refatoração: ecommerce-api-legacy

Refatoramos com sucesso a API legada do e-commerce/LMS seguindo os padrões arquiteturais MVC e corrigindo vulnerabilidades de segurança e performance encontradas.

## Mudanças Realizadas

### Configurações
- **[NEW] [db.js](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/config/db.js):** Inicializa a instância em memória do SQLite3 e exporta um wrapper Promise-based (`dbQuery`) para remover o Callback Hell.
- **[NEW] [dbInit.js](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/config/dbInit.js):** Define a criação de tabelas e insere dados iniciais de semente (seeding) utilizando hashes seguros.
- **[NEW] [env.js](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/config/env.js):** Isolamento de chaves secretas consumindo variáveis de ambiente com fallbacks e suporte a arquivo `.env` via `dotenv`.
- **[NEW] [.env](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/.env):** Arquivo de configuração de ambiente contendo as variáveis padrão (DB_USER, DB_PASS, etc.).

### Models (Camada de Acesso a Dados)
- **[NEW] [User.js](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/models/User.js):** Métodos assíncronos para criação, consulta e deleção na tabela `users`.
- **[NEW] [Course.js](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/models/Course.js):** Consultas referentes a `courses`.
- **[NEW] [Enrollment.js](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/models/Enrollment.js):** Operações da tabela `enrollments`.
- **[NEW] [Payment.js](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/models/Payment.js):** Operações da tabela `payments`.
- **[NEW] [AuditLog.js](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/models/AuditLog.js):** Criação de logs de auditoria.

### Services (Regras de Negócio)
- **[NEW] [AuthService.js](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/services/AuthService.js):** Encapsula a criptografia e hashing de senhas usando a biblioteca `bcryptjs`.
- **[NEW] [CheckoutService.js](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/services/CheckoutService.js):** Orquestra o fluxo de checkout de cursos, verificações de cartão de crédito e persistência de matrículas.
- **[NEW] [FinancialService.js](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/services/FinancialService.js):** Gera o relatório financeiro usando um único `LEFT JOIN` unificado (eliminando consultas N+1).
- **[NEW] [UserService.js](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/services/UserService.js):** Gerencia deleções de usuários garantindo a limpeza em cascata de suas matrículas e pagamentos.

### Controllers & Rotas
- **[NEW] [CheckoutController.js](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/controllers/CheckoutController.js):** Trata inputs de checkout e envia respostas JSON estruturadas.
- **[NEW] [AdminController.js](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/controllers/AdminController.js):** Exposição do endpoint administrativo de relatório financeiro.
- **[NEW] [UserController.js](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/controllers/UserController.js):** Trata requisição de deleção de usuários.
- **[NEW] [routes/index.js](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/routes/index.js):** Centralização e definição limpa das rotas no Express.

### Inicialização & Cleanup
- **[MODIFY] [app.js](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/app.js):** Simplificado para carregar a inicialização assíncrona do banco e montar os middlewares e rotas principais.
- **[DELETE] [AppManager.js](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/AppManager.js):** Removido, pois sua lógica foi distribuída de forma limpa nas camadas MVC.

## Validação Executada
Iniciamos a aplicação localmente utilizando Node 18 e realizamos as requisições especificadas em `api.http`:

1. **Relatório Financeiro Inicial:**
   - Retornou com sucesso a semente inicial:
     ```json
     [{"course":"Clean Architecture","revenue":997,"students":[{"student":"Leonan","paid":997}]},{"course":"Docker","revenue":0,"students":[]}]
     ```
2. **Checkout de Sucesso:**
   - Registrou "Guilherme" e retornou `{"msg":"Sucesso","enrollment_id":2}`.
3. **Checkout Recusado:**
   - Barrou cartões que não iniciam com `4` com status `400 Bad Request` e mensagem `Pagamento recusado`.
4. **Deleção do Usuário 1 (Leonan):**
   - Retornou sucesso e efetuou a remoção limpa de seus registros relacionados (matrículas e pagamentos).
5. **Relatório Financeiro Pós-Deleção:**
   - Confirmou a integridade dos dados, zerando a receita de "Clean Architecture" e listando apenas "Guilherme" em "Docker".
