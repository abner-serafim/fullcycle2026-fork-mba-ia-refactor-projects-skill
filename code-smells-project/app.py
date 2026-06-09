from flask import Flask, jsonify, request
from flask_cors import CORS
from config import settings
from database import get_db

# Importação dos Blueprints de Rotas
from routes.produto_routes import produto_bp
from routes.usuario_routes import usuario_bp
from routes.pedido_routes import pedido_bp
from routes.relatorio_routes import relatorio_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = settings.SECRET_KEY
app.config["DEBUG"] = settings.DEBUG
CORS(app)

# Registro dos Blueprints
app.register_blueprint(produto_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(pedido_bp)
app.register_blueprint(relatorio_bp)

@app.route("/")
def index():
    return jsonify({
        "mensagem": "Bem-vindo à API da Loja",
        "versao": "1.0.0",
        "endpoints": {
            "produtos": "/produtos",
            "usuarios": "/usuarios",
            "pedidos": "/pedidos",
            "login": "/login",
            "relatorios": "/relatorios/vendas",
            "health": "/health"
        }
    })

# Rota de health check limpa e sem vazamento de chave secreta
@app.route("/health", methods=["GET"])
def health_check():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        
        cursor.execute("SELECT COUNT(*) FROM produtos")
        produtos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        usuarios = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM pedidos")
        pedidos = cursor.fetchone()[0]

        return jsonify({
            "status": "ok",
            "database": "connected",
            "counts": {
                "produtos": produtos,
                "usuarios": usuarios,
                "pedidos": pedidos
            },
            "versao": "1.0.0"
        }), 200
    except Exception as e:
        print(f"ERRO health_check: {e}")
        return jsonify({"status": "erro", "detalhes": "Banco de dados offline ou erro de conexão"}), 500

@app.route("/admin/reset-db", methods=["POST"])
def reset_database():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM itens_pedido")
        cursor.execute("DELETE FROM pedidos")
        cursor.execute("DELETE FROM produtos")
        cursor.execute("DELETE FROM usuarios")
        db.commit()
        print("!!! BANCO DE DADOS RESETADO !!!")
        return jsonify({"mensagem": "Banco de dados resetado", "sucesso": True}), 200
    except Exception as e:
        print(f"ERRO reset_database: {e}")
        return jsonify({"erro": "Erro interno ao resetar o banco de dados", "sucesso": False}), 500

@app.route("/admin/query", methods=["POST"])
def executar_query():
    # Bloqueio de Backdoor por padrão
    if not settings.ENABLE_ADMIN_QUERY:
        return jsonify({"erro": "Acesso negado: execução de consultas arbitrárias desabilitada.", "sucesso": False}), 403

    dados = request.get_json()
    query = dados.get("sql", "")
    if not query:
        return jsonify({"erro": "Query não informada"}), 400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(query)
        if query.strip().upper().startswith("SELECT"):
            rows = cursor.fetchall()
            result = [dict(row) for row in rows]
            return jsonify({"dados": result, "sucesso": True}), 200
        else:
            db.commit()
            return jsonify({"mensagem": "Query executada", "sucesso": True}), 200
    except Exception as e:
        print(f"ERRO executar_query: {e}")
        return jsonify({"erro": "Erro na execução da consulta SQL no banco de dados"}), 500

if __name__ == "__main__":
    # Garante que o banco seja criado/inicializado no boot
    get_db()
    print("=" * 50)
    print("SERVIDOR INICIADO")
    print(f"Rodando em http://localhost:{settings.PORT}")
    print("=" * 50)

    app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)
