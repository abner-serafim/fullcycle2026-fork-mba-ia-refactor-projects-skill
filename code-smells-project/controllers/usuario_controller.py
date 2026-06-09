from flask import request, jsonify
from models import usuario as usuario_model

def listar_usuarios():
    try:
        usuarios = usuario_model.get_todos_usuarios()
        # Remove a senha hash dos retornos da API por questões de segurança
        for u in usuarios:
            u.pop("senha", None)
        return jsonify({"dados": usuarios, "sucesso": True}), 200
    except Exception as e:
        print(f"ERRO listar_usuarios: {e}")
        return jsonify({"erro": "Erro interno do servidor ao obter usuários", "sucesso": False}), 500

def buscar_usuario(id):
    try:
        usuario = usuario_model.get_usuario_por_id(id)
        if usuario:
            usuario.pop("senha", None)
            return jsonify({"dados": usuario, "sucesso": True}), 200
        return jsonify({"erro": "Usuário não encontrado", "sucesso": False}), 404
    except Exception as e:
        print(f"ERRO buscar_usuario: {e}")
        return jsonify({"erro": "Erro interno do servidor ao buscar usuário", "sucesso": False}), 500

def criar_usuario():
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Dados inválidos", "sucesso": False}), 400

        nome = dados.get("nome", "")
        email = dados.get("email", "")
        senha = dados.get("senha", "")
        tipo = dados.get("tipo", "cliente")

        if not nome or not email or not senha:
            return jsonify({"erro": "Nome, email e senha são obrigatórios", "sucesso": False}), 400

        user_id = usuario_model.criar_usuario(nome, email, senha, tipo)
        return jsonify({"dados": {"id": user_id}, "sucesso": True, "mensagem": "Usuário criado com sucesso"}), 201
    except Exception as e:
        print(f"ERRO criar_usuario: {e}")
        return jsonify({"erro": "Erro interno do servidor ao criar usuário", "sucesso": False}), 500

def login():
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Dados inválidos", "sucesso": False}), 400
            
        email = dados.get("email", "")
        senha = dados.get("senha", "")

        if not email or not senha:
            return jsonify({"erro": "Email e senha são obrigatórios", "sucesso": False}), 400

        usuario = usuario_model.login_usuario(email, senha)
        if usuario:
            return jsonify({"dados": usuario, "sucesso": True, "mensagem": "Login realizado com sucesso"}), 200
        return jsonify({"erro": "Credenciais inválidas", "sucesso": False}), 401
    except Exception as e:
        print(f"ERRO login: {e}")
        return jsonify({"erro": "Erro interno do servidor ao realizar login", "sucesso": False}), 500
