from flask import jsonify
from models import pedido as pedido_model

def relatorio_vendas():
    try:
        relatorio = pedido_model.relatorio_vendas()
        return jsonify({"dados": relatorio, "sucesso": True}), 200
    except Exception as e:
        print(f"ERRO relatorio_vendas: {e}")
        return jsonify({"erro": "Erro interno do servidor ao gerar relatório de vendas", "sucesso": False}), 500
