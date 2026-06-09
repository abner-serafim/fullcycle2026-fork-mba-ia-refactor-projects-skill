# Catálogo de Anti-patterns e Vulnerabilidades

1. **SQL Injection (Critical):** Concatenação direta de inputs em strings SQL. Detecção: Uso de operadores `+` ou f-strings em queries.
2. **Hardcoded Secrets (Critical):** Chaves, senhas ou tokens expostos. Detecção: Strings como "SECRET_KEY", "password", "token" atribuídas a constantes.
3. **N+1 Query Problem (High):** Queries dentro de loops. Detecção: `for` ou `map` contendo chamadas de banco de dados (`query.get`, `find`).
4. **God Class/Method (High):** Classes que fazem de tudo. Detecção: Arquivos com > 200 linhas misturando roteamento, regra de negócio e I/O.
5. **Plaintext Password (High):** Senhas sem hashing. Detecção: Armazenamento de campos `password` sem chamadas a bibliotecas de hash (bcrypt/argon2).
6. **Error Leaking (Medium):** Retorno de `str(e)` ou stack trace. Detecção: `except Exception as e: return jsonify(str(e))`.
7. **Callback Hell (Medium):** Aninhamento excessivo de funções assíncronas. Detecção: > 3 níveis de aninhamento em Node.js.
8. **Magic Numbers (Low):** Valores numéricos fixos em regras de negócio. Detecção: `if x > 1000:`.