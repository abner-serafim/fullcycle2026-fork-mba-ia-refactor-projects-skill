# Playbook de Refatoração

1. **Segregação:** Se encontrar lógica em `routes/`, crie um `controllers/` correspondente. Mova a lógica para funções no controller e chame-as na rota.
2. **Segurança:** Substitua toda string de segredo por `os.getenv('VAR_NAME')` ou `process.env.VAR_NAME`.
3. **Performance:** Sempre que encontrar um loop com consulta ao banco, substitua por uma query única usando `JOIN` ou `IN` clauses.
4. **Hashing:** Sempre substitua algoritmos antigos (MD5/SHA1) por `bcrypt` (Node.js) ou `passlib/bcrypt` (Python).