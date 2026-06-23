# Playbook de Refatoração Técnica (Exemplos Antes / Depois)

Este guia prático fornece ao agente os padrões exatos de transformação estrutural e de segurança com exemplos de código limpo antes e depois.

---

### 1. Prevenção de SQL Injection (Consultas Parametrizadas)
* Antes (Vulnerável):
query = f"SELECT * FROM usuarios WHERE email = '{email}' AND password = '{password}'"
cursor.execute(query)

* Depois (Refatorado):
query = "SELECT * FROM usuarios WHERE email = %s AND password = %s"
cursor.execute(query, (email, password))

---

### 2. Substituição de Algoritmos Criptográficos Obsoletos / Deprecated (MD5 para Bcrypt)
* Antes (Vulnerável/Obsoleto):
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()

* Depois (Seguro/Atualizado):
import bcrypt
salt = bcrypt.gensalt()
password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

---

### 3. Extração de Credenciais Hardcoded para Variáveis de Ambiente (.env)
* Antes (Vulnerável):
const GATEWAY_TOKEN = "live_pk_958102384021384091238";
const DB_PASSWORD = "super_secret_db_pass_123";

* Depois (Seguro):
require('dotenv').config();
const GATEWAY_TOKEN = process.env.GATEWAY_TOKEN;
const DB_PASSWORD = process.env.DB_PASSWORD;

---

### 4. Otimização de Performance N+1 (Uso de JOINs / Agrupamentos)
* Antes (Ineficiente - I/O pesado em loop):
for pedido in pedidos:
    produto = db.execute("SELECT nome FROM produtos WHERE id = %s", (pedido['produto_id'],)).fetchone()
    pedido['produto_nome'] = produto['nome']

* Depois (Eficiente):
query = "SELECT pedidos.*, produtos.nome as produto_nome FROM pedidos JOIN produtos ON pedidos.produto_id = produtos.id"
pedidos_com_produtos = db.execute(query).fetchall()

---

### 5. Desacoplamento Arquitetural de Rotas para Controllers (Padrão MVC)
* Antes (God Class / Lógica na Rota):
@app.route('/produtos', methods=['POST'])
def criar_produto():
    dados = request.json
    if not dados.get('nome'): return jsonify({"erro": "Nome obrigatorio"}), 400
    db.execute("INSERT INTO produtos (nome) VALUES (%s)", (dados['nome'],))
    return jsonify({"status": "sucesso"}), 201

* Depois (Isolamento de Camadas):
# No arquivo de rotas:
@produto_blueprint.route('/produtos', methods=['POST'])
def criar_produto(): return ProdutoController.criar(request)

# No arquivo de controller:
class ProdutoController:
    @staticmethod
    def criar(request):
        dados = request.json
        if not dados.get('nome'): return jsonify({"erro": "Nome obrigatorio"}), 400
        ProdutoModel.salvar(dados['nome'])
        return jsonify({"status": "sucesso"}), 201

---

### 6. Higienização de Mensagens e Tratamento Centralizado de Erros (Error Leaking)
* Antes (Vulnerável - Exposição de Detalhes):
except Exception as e:
    return jsonify({"error": str(e), "trace": sys.exc_info()}), 500

* Depois (Seguro):
except Exception as e:
    logger.error(f"Erro interno de infraestrutura: {str(e)}")
    return jsonify({"error": "Ocorreu um erro interno no servidor. Por favor, tente novamente mais tarde."}), 500

---

### 7. Migração de Callback Hell para Async/Await
* Antes (Gargalo síncrono/aninhado):
fs.readFile('relatorio.json', (err, data) => {
    db.query('SELECT * FROM config', (err, rows) => {
        gateway.send(rows, (err, response) => {
            res.send("Pronto");
        });
    });
});

* Depois (Linear e Seguro):
try {
    const data = await fs.promises.readFile('relatorio.json');
    const rows = await db.queryAsync('SELECT * FROM config');
    const response = await gateway.sendAsync(rows);
    res.send("Pronto");
} catch (error) {
    next(error);
}

---

### 8. Substituição de Magic Numbers por Constantes Nomeadas (Legibilidade)
* Antes (Código confuso):
if usuario.tipo == 3:
    calcular_desconto(pedido, 0.15)

* Depois (Código Semântico):
ROLE_ADMINISTRADOR = 3
PERCENTUAL_DESCONTO_MASTER = 0.15

if usuario.tipo == ROLE_ADMINISTRADOR:
    calcular_desconto(pedido, PERCENTUAL_DESCONTO_MASTER)