from flask import request, jsonify
from models import produto as produto_model

def listar_produtos():
    try:
        produtos = produto_model.get_todos_produtos()
        return jsonify({"dados": produtos, "sucesso": True}), 200
    except Exception as e:
        # Registra o erro internamente e retorna resposta limpa
        print(f"ERRO listar_produtos: {e}")
        return jsonify({"erro": "Erro interno do servidor ao obter produtos", "sucesso": False}), 500

def buscar_produto(id):
    try:
        prod = produto_model.get_produto_por_id(id)
        if prod:
            return jsonify({"dados": prod, "sucesso": True}), 200
        return jsonify({"erro": "Produto não encontrado", "sucesso": False}), 404
    except Exception as e:
        print(f"ERRO buscar_produto: {e}")
        return jsonify({"erro": "Erro interno do servidor ao buscar produto", "sucesso": False}), 500

def criar_produto():
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Dados inválidos", "sucesso": False}), 400
        if "nome" not in dados or "preco" not in dados or "estoque" not in dados:
            return jsonify({"erro": "Nome, preço e estoque são obrigatórios", "sucesso": False}), 400

        nome = dados["nome"]
        descricao = dados.get("descricao", "")
        preco = dados["preco"]
        estoque = dados["estoque"]
        categoria = dados.get("categoria", "geral")

        if preco < 0 or estoque < 0:
            return jsonify({"erro": "Preço e estoque não podem ser negativos", "sucesso": False}), 400
        if len(nome) < 2 or len(nome) > 200:
            return jsonify({"erro": "Nome do produto deve ter entre 2 e 200 caracteres", "sucesso": False}), 400

        categorias_validas = ["informatica", "moveis", "vestuario", "geral", "eletronicos", "livros"]
        if categoria not in categorias_validas:
            return jsonify({"erro": f"Categoria inválida. Válidas: {categorias_validas}", "sucesso": False}), 400

        prod_id = produto_model.criar_produto(nome, descricao, preco, estoque, categoria)
        return jsonify({"dados": {"id": prod_id}, "sucesso": True, "mensagem": "Produto criado com sucesso"}), 201
    except Exception as e:
        print(f"ERRO criar_produto: {e}")
        return jsonify({"erro": "Erro interno do servidor ao criar produto", "sucesso": False}), 500

def atualizar_produto(id):
    try:
        dados = request.get_json()
        prod_existente = produto_model.get_produto_por_id(id)
        if not prod_existente:
            return jsonify({"erro": "Produto não encontrado", "sucesso": False}), 404

        if not dados:
            return jsonify({"erro": "Dados inválidos", "sucesso": False}), 400
        if "nome" not in dados or "preco" not in dados or "estoque" not in dados:
            return jsonify({"erro": "Nome, preço e estoque são obrigatórios", "sucesso": False}), 400

        nome = dados["nome"]
        descricao = dados.get("descricao", "")
        preco = dados["preco"]
        estoque = dados["estoque"]
        categoria = dados.get("categoria", "geral")

        if preco < 0 or estoque < 0:
            return jsonify({"erro": "Preço e estoque não podem ser negativos", "sucesso": False}), 400

        produto_model.atualizar_produto(id, nome, descricao, preco, estoque, categoria)
        return jsonify({"sucesso": True, "mensagem": "Produto atualizado com sucesso"}), 200
    except Exception as e:
        print(f"ERRO atualizar_produto: {e}")
        return jsonify({"erro": "Erro interno do servidor ao atualizar produto", "sucesso": False}), 500

def deletar_produto(id):
    try:
        prod = produto_model.get_produto_por_id(id)
        if not prod:
            return jsonify({"erro": "Produto não encontrado", "sucesso": False}), 404

        produto_model.deletar_produto(id)
        return jsonify({"sucesso": True, "mensagem": "Produto deletado com sucesso"}), 200
    except Exception as e:
        print(f"ERRO deletar_produto: {e}")
        return jsonify({"erro": "Erro interno do servidor ao deletar produto", "sucesso": False}), 500

def buscar_produtos():
    try:
        termo = request.args.get("q", "")
        categoria = request.args.get("categoria", None)
        preco_min = request.args.get("preco_min", None)
        preco_max = request.args.get("preco_max", None)

        if preco_min is not None:
            preco_min = float(preco_min)
        if preco_max is not None:
            preco_max = float(preco_max)

        resultados = produto_model.buscar_produtos(termo, categoria, preco_min, preco_max)
        return jsonify({"dados": resultados, "total": len(resultados), "sucesso": True}), 200
    except Exception as e:
        print(f"ERRO buscar_produtos: {e}")
        return jsonify({"erro": "Erro interno do servidor ao realizar a busca", "sucesso": False}), 500
