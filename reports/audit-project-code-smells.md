# Relatório de Auditoria: code-smells-project

## Resumo Executivo
- Total de Vulnerabilidades: 6
- Severidade Média: HIGH

## Lista de Problemas
| ID | Severidade | Problema | Localização |
|---|---|---|---|
| 01 | CRITICAL | SQL Injection via concatenação direta em queries SQL (risco de vazamento/destruição de dados) | [models.py](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/code-smells-project/models.py#L28) e múltiplas funções em `models.py` |
| 02 | CRITICAL | Endpoint de execução de SQL arbitrário (`/admin/query`) sem autenticação ou sanitização | [app.py](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/code-smells-project/app.py#L59) |
| 03 | CRITICAL | Hardcoded Secrets (chave secreta definida no código e vazada no endpoint de healthcheck) | [app.py](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/code-smells-project/app.py#L7) e [controllers.py](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/code-smells-project/controllers.py#L289) |
| 04 | HIGH | Plaintext Password (senhas de usuários armazenadas e validadas sem algoritmo de hash) | [models.py](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/code-smells-project/models.py#L122) |
| 05 | HIGH | N+1 Query Problem (consultas em loops em loops nos métodos de listagem de pedidos e itens) | [models.py](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/code-smells-project/models.py#L174-L201) e [models.py](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/code-smells-project/models.py#L203-L233) |
| 06 | MEDIUM | Error Leaking (exposição de mensagens de exceção internas e caminhos nos retornos de API) | [controllers.py](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/code-smells-project/controllers.py#L12) e outras funções |

## Sugestão de Plano de Ação
- [x] Fase 1: Segregação de Responsabilidades (Extrair rotas inline de `app.py` e reorganizar em roteador MVC limpo).
- [x] Fase 2: Mitigação de Riscos de Segurança (Hashing e Variáveis de Ambiente).
- [x] Fase 3: Otimização de Performance (Remover queries N+1 usando JOINs SQL apropriados).
