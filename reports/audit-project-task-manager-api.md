# Relatório de Auditoria: task-manager-api

## Resumo Executivo
- Total de Vulnerabilidades: 8
- Severidade Média: HIGH

## Lista de Problemas
| ID | Severidade | Problema | Localização |
|---|---|---|---|
| 01 | CRITICAL | Hardcoded Secret: SECRET_KEY exposto diretamente no código. | [app.py:13](file:///home/abneradekz/projetos/estudo/fullcycle-2026/fullcycle2026-fork-mba-ia-refactor-projects-skill/task-manager-api/app.py#L13) |
| 02 | CRITICAL | Hardcoded Credentials: Usuário e senha de e-mail expostos diretamente no serviço de notificação. | [notification_service.py:9-10](file:///home/abneradekz/projetos/estudo/fullcycle-2026/fullcycle2026-fork-mba-ia-refactor-projects-skill/task-manager-api/services/notification_service.py#L9-L10) |
| 03 | HIGH | Plaintext/Weak Password Hashing: Uso de MD5 para salvar e checar senhas de usuários. | [user.py:29-32](file:///home/abneradekz/projetos/estudo/fullcycle-2026/fullcycle2026-fork-mba-ia-refactor-projects-skill/task-manager-api/models/user.py#L29-L32) |
| 04 | HIGH | N+1 Query Problem: Consultas repetitivas ao banco de dados dentro de loops ao retornar a lista de tasks e gerar relatórios. | [task_routes.py:41-57](file:///home/abneradekz/projetos/estudo/fullcycle-2026/fullcycle2026-fork-mba-ia-refactor-projects-skill/task-manager-api/routes/task_routes.py#L41-L57), [report_routes.py:55-68](file:///home/abneradekz/projetos/estudo/fullcycle-2026/fullcycle2026-fork-mba-ia-refactor-projects-skill/task-manager-api/routes/report_routes.py#L55-L68) |
| 05 | HIGH | God Class/Methods (Falta de MVC): Lógica de persistência, negócio e validação misturadas diretamente nos arquivos de rota. | [task_routes.py:11-300](file:///home/abneradekz/projetos/estudo/fullcycle-2026/fullcycle2026-fork-mba-ia-refactor-projects-skill/task-manager-api/routes/task_routes.py#L11-L300), [user_routes.py:10-212](file:///home/abneradekz/projetos/estudo/fullcycle-2026/fullcycle2026-fork-mba-ia-refactor-projects-skill/task-manager-api/routes/user_routes.py#L10-L212), [report_routes.py:12-224](file:///home/abneradekz/projetos/estudo/fullcycle-2026/fullcycle2026-fork-mba-ia-refactor-projects-skill/task-manager-api/routes/report_routes.py#L12-L224) |
| 06 | HIGH | Exposição de Credenciais: Serialização de senha ativa no método to_dict. | [models/user.py:21](file:///home/abneradekz/projetos/estudo/fullcycle-2026/fullcycle2026-fork-mba-ia-refactor-projects-skill/task-manager-api/models/user.py#L21) |
| 07 | MEDIUM | Deprecated / Obsolete APIs: Fallback MD5 de verificação de senhas. | [models/user.py:35-38](file:///home/abneradekz/projetos/estudo/fullcycle-2026/fullcycle2026-fork-mba-ia-refactor-projects-skill/task-manager-api/models/user.py#L35-L38) |
| 08 | LOW | Magic Numbers: Constantes numéricas de prioridade e validação de senhas sem nomeação clara. | [controllers/task_controller.py:89](file:///home/abneradekz/projetos/estudo/fullcycle-2026/fullcycle2026-fork-mba-ia-refactor-projects-skill/task-manager-api/controllers/task_controller.py#L89), [controllers/user_controller.py:59](file:///home/abneradekz/projetos/estudo/fullcycle-2026/fullcycle2026-fork-mba-ia-refactor-projects-skill/task-manager-api/controllers/user_controller.py#L59) |

## Sugestão de Plano de Ação
- [ ] Fase 1: Segregação de Responsabilidades (Extrair lógica de Routes para Controllers).
- [ ] Fase 2: Mitigação de Riscos de Segurança (Hashing de senha com bcrypt e isolamento de segredos em Variáveis de Ambiente).
- [ ] Fase 3: Otimização de Performance (Uso de Eager Loading para evitar queries N+1).
- [ ] Fase 4: Higienização de Dados e Refatoração de Boas Práticas (Remover a chave 'password' da serialização de User, logs-warn/remover MD5, e definir constantes para Magic Numbers).
