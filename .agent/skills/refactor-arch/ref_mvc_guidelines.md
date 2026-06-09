# Diretrizes para MVC

- **Models (`models/`):** Apenas definição de schemas, tipos e métodos de acesso a dados. Zero lógica de I/O ou roteamento.
- **Controllers (`controllers/`):** Onde a mágica acontece. Recebe a requisição (sanitizada), orquestra o serviço e decide a resposta.
- **Routes (`routes/`):** Apenas definição de endpoints e mapeamento para controllers.
- **Services (`services/`):** Lógica pesada, envio de e-mail, integração com terceiros.
- **Config (`config/`):** Leitura de variáveis de ambiente (`process.env` ou `os.getenv`).