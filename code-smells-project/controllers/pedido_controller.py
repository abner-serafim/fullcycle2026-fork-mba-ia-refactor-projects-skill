from flask import request, jsonify
from models import pedido as pedido_model
from services import notification_service

def criar_pedido():
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Dados inválidos", "sucesso": False}), 400

        usuario_id = dados.get("usuario_id")
        itens = dados.get("itens", [])

        if not usuario_id:
            return jsonify({"erro": "ID do usuário é obrigatório", "sucesso": False}), 400
        if not itens or len(itens) == 0:
            return jsonify({"erro": "Pedido deve conter pelo menos 1 item", "sucesso": False}), 400

        resultado = pedido_model.criar_pedido(usuario_id, itens)
        if "erro" in resultado:
            return jsonify({"erro": resultado["erro"], "sucesso": False}), 400

        # Dispara notificações de forma desacoplada
        notification_service.enviar_notificacoes_pedido_criado(resultado["pedido_id"], usuario_id)

        return jsonify({
            "dados": resultado,
            "sucesso": True,
            "mensagem": "Pedido criado com sucesso"
        }), 201
    except Exception as e:
        print(f"ERRO criar_pedido: {e}")
        return jsonify({"erro": "Erro interno do servidor ao criar pedido", "sucesso": False}), 500

def listar_pedidos_usuario(usuario_id):
    try:
        pedidos = pedido_model.get_pedidos_usuario(usuario_id)
        return jsonify({"dados": pedidos, "sucesso": True}), 200
    except Exception as e:
        print(f"ERRO listar_pedidos_usuario: {e}")
        return jsonify({"erro": "Erro interno do servidor ao listar pedidos", "sucesso": False}), 500

def listar_todos_pedidos():
    try:
        pedidos = pedido_model.get_todos_pedidos()
        return jsonify({"dados": pedidos, "sucesso": True}), 200
    except Exception as e:
        print(f"ERRO listar_todos_pedidos: {e}")
        return jsonify({"erro": "Erro interno do servidor ao listar todos os pedidos", "sucesso": False}), 500

def atualizar_status_pedido(pedido_id):
    try:
        dados = request.get_json()
        novo_status = dados.get("status", "")

        if novo_status not in ["pendente", "aprovado", "enviado", "entregue", "cancelado"]:
            return jsonify({"erro": "Status inválido", "sucesso": False}), 400

        pedido_model.atualizar_status_pedido(pedido_id, novo_status)

        # Dispara notificações de alteração de status
        if novo_status == "aprovado":
            notification_service.enviar_notificacao_pedido_aprovado(pedido_id)
        elif novo_status == "cancelado":
            notification_service.enviar_notificacao_pedido_cancelado(pedido_id)

        return jsonify({"sucesso": True, "mensagem": f"Status do pedido atualizado para '{novo_status}'"}), 200
    except Exception as e:
        print(f"ERRO atualizar_status_pedido: {e}")
        return jsonify({"erro": "Erro interno do servidor ao atualizar status do pedido", "sucesso": False}), 500
