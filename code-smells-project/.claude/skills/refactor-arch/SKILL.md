---
name: refactor-arch
description: Skill especializada e agnóstica de tecnologia projetada para analisar bases de código legadas (Python/Flask e Node.js/Express), auditar vulnerabilidades críticas, falhas de SOLID, APIs obsoletas e code smells, gerando um relatório estruturado e automatizando a reestruturação arquitetural completa para o padrão Model-View-Controller (MVC) sem quebrar a aplicação.
---

## Requirements & Constraints
- **Agnóstica de Tecnologia:** Deve funcionar perfeitamente em ecossistemas Python e Node.js, adaptando-se tanto a projetos totalmente desestruturados (monólitos em poucos arquivos) quanto a bases parcialmente organizadas.
- **Interrupção de Segurança:** É OBRIGATÓRIO pausar no final da Fase 2 para pedir autorização expressa do utilizador humano antes de efetuar qualquer alteração ou criação de arquivos.
- **Validação Pós-Refatoração:** Na Fase 3, deve validar se a aplicação compila/inicia sem erros e se os endpoints originais continuam operacionais.

---

## Execution Pipeline (Sequência de Fases)

### PHASE 1: PROJECT ANALYSIS
**Objetivo:** Mapear o estado atual da codebase sem fazer alterações.
1. Ler os arquivos de configuração, manifestos de dependências (`requirements.txt`, `package.json`) e o código-fonte para identificar a stack tecnológica (Linguagem, Framework, Banco de dados) e o domínio de negócio.
2. Identificar a volumetria (número de arquivos analisados e tabelas/entidades do banco de dados).
3. Imprimir no terminal um resumo estruturado exatamente no seguinte formato:

```

# ================================
PHASE 1: PROJECT ANALYSIS

# Language:      
Framework:     
Dependencies:  <Principais Dependências>
Domain:        <Domínio de Negócio da API>
Architecture:  <Descrição do estado arquitetural atual>
Source files:  
DB tables:     

```

### PHASE 2: ARCHITECTURE AUDIT
**Objetivo:** Detetar problemas e gerar o relatório formal de auditoria.
1. Cruzar todo o código-fonte contra as regras definidas em `ref_anti_patterns.md` (Catálogo de Anti-patterns).
2. Identificar obrigatoriamente no mínimo 5 problemas por projeto, classificando-os estritamente de acordo com a escala de severidade (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`) detalhada nas diretrizes, apontando o arquivo e intervalo de linhas exatos.
3. Verificar explicitamente se há uso de APIs Deprecated/obsoletas recomendando seus equivalentes modernos.
4. Gerar e salvar o relatório final padronizado em formato Markdown seguindo o template de `ref_report_template.md` na pasta `reports/audit-project-<X>.md`.
5. **BLOQUEIO DE SEGURANÇA (OBRIGATÓRIO):** Imprimir o resumo quantitativo de achados no terminal e exibir a seguinte mensagem de pausa, aguardando entrada explícita do utilizador:

```

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]

```
*Se o utilizador responder 'n', interromper a execução imediatamente de forma segura.*

### PHASE 3: REFACTORING & VALIDATION
**Objetivo:** Transformar o projeto e garantir resiliência.
1. Executar os padrões de transformação mapeados em `ref_refactoring_playbook.md` para mitigar todos os problemas encontrados na Fase 2.
2. Isolar segredos e chaves hardcoded extraindo-os para um módulo de configuração centralizado que consome variáveis de ambiente (`.env`).
3. Reestruturar a base de código dividindo as responsabilidades estritamente nas camadas MVC preconizadas em `ref_mvc_guidelines.md`:
- **Models:** Abstração e manipulação direta de dados/entidades.
- **Controllers:** Orquestração do fluxo da aplicação e lógica de negócio.
- **Views/Routes:** Definição limpa de roteamento e exposição de endpoints.
- **Middlewares/Config:** Centralização de erros e inicialização da infraestrutura.
4. Remover duplicações de código e consultas ineficientes (como loops N+1).
5. Validar o resultado:
- Simular ou executar o boot do servidor garantindo que a aplicação inicia com sucesso (código de saída 0).
- Verificar se todos os endpoints originais continuam respondendo corretamente.
6. Imprimir o sumário de conclusão da refatoração exibindo a nova estrutura de diretórios e o checklist de validação preenchido.

---

## Knowledge References (Arquivos de Suporte)
A IA consumirá o conhecimento contido nos arquivos de referência locais da pasta da skill para guiar suas decisões:
- `ref_analysis_heuristics.md`: Regras para identificação de stacks e mapeamento arquitetural.
- `ref_anti_patterns.md`: Catálogo com os 8 anti-patterns mínimos, sinais de detecção e criticidades.
- `ref_report_template.md`: Modelo markdown para estruturação das auditorias.
- `ref_mvc_guidelines.md`: Contratos de separação de responsabilidades e padrões de pastas.
- `ref_refactoring_playbook.md`: Guia de transformação estrutural com exemplos de código antes e depois.
