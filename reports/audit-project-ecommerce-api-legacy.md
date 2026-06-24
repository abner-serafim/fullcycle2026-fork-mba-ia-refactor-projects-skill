# Relatório de Auditoria: ecommerce-api-legacy

## Resumo Executivo
- Total de Vulnerabilidades: 10
- Severidade Média: HIGH

## Lista de Problemas
| ID | Severidade | Problema | Localização |
|---|---|---|---|
| 01 | CRITICAL | Hardcoded Secrets (Credenciais expostas no código) | [utils.js:2-5](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/utils.js#L2-L5) |
| 02 | HIGH | N+1 Query Problem (Queries em loops aninhados no relatório financeiro) | [AppManager.js:80-129](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/AppManager.js#L80-L129) |
| 03 | HIGH | God Class (Mistura de rotas, inicialização de DB, queries e lógica de negócio) | [AppManager.js:1-139](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/AppManager.js) |
| 04 | HIGH | Senha em texto plano e Hashing fraco (Seed com senha '123' e criptografia base64 customizada) | [AppManager.js:18](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/AppManager.js#L18), [utils.js:17-23](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/utils.js#L17-L23) |
| 05 | MEDIUM | Callback Hell (Alto nível de aninhamento de callbacks assíncronos) | [AppManager.js:28-78](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/AppManager.js#L28-L78), [AppManager.js:80-129](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/AppManager.js#L80-L129) |
| 06 | MEDIUM | Inconsistência de Dados no Delete (Usuário deletado deixa registros órfãos em matrículas/pagamentos) | [AppManager.js:131-137](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/AppManager.js#L131-L137) |
| 07 | MEDIUM | Memory Leak (Vazamento de Memória por Cache Incondicional) | [utils.js:9](file:///home/abneradekz/projetos/estudo/fullcycle-2026/fullcycle2026-fork-mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/utils.js#L9) |
| 08 | MEDIUM | Deprecated / Obsolete APIs (Criptografia Customizada Fraca/Obsoleta) | [utils.js:17-23](file:///home/abneradekz/projetos/estudo/fullcycle-2026/fullcycle2026-fork-mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/utils.js#L17-L23) |
| 09 | LOW | Magic Numbers (Valores numéricos/strings fixos soltos na regra de negócio) | [CheckoutService.js:23](file:///home/abneradekz/projetos/estudo/fullcycle-2026/fullcycle2026-fork-mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/services/CheckoutService.js#L23), [CheckoutService.js:30](file:///home/abneradekz/projetos/estudo/fullcycle-2026/fullcycle2026-fork-mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/services/CheckoutService.js#L30) |
| 10 | MEDIUM | Error Leaking (Vazamento de Mensagem de Exceção Interna) | [CheckoutController.js:22](file:///home/abneradekz/projetos/estudo/fullcycle-2026/fullcycle2026-fork-mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/controllers/CheckoutController.js#L22) |

## Sugestão de Plano de Ação
- [ ] Fase 1: Segregação de Responsabilidades (Extrair lógica de rotas/db/checkout do `AppManager` para arquitetura MVC).
- [ ] Fase 2: Mitigação de Riscos de Segurança (Isolar segredos com dotenv e introduzir hashing seguro com bcrypt para senhas).
- [ ] Fase 3: Resolução de N+1 (Reescrever o relatório financeiro para utilizar um JOIN único simplificado).
- [ ] Fase 4: Tratamento de Integridade e Remoção de Callback Hell (Utilizar Promises/async-await e chaves estrangeiras com cascata ou soft deletes).
- [ ] Fase 5: Prevenção de Memory Leaks e Remoção de APIs Obsoletas (Limitar tamanho do cache global e remover a função descontinuada `badCrypto`).
- [ ] Fase 6: Higienização de Respostas e Nomeação de Constantes (Substituir magic numbers no fluxo de checkout e filtrar mensagens de erro 500 no controller).
