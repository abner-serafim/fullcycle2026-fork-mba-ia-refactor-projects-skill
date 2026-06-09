def enviar_notificacoes_pedido_criado(pedido_id: int, usuario_id: int):
    # Simula o disparo de notificações de forma centralizada e desacoplada do fluxo HTTP principal
    print(f"ENVIANDO EMAIL: Pedido {pedido_id} criado para usuario {usuario_id}")
    print("ENVIANDO SMS: Seu pedido foi recebido!")
    print("ENVIANDO PUSH: Novo pedido recebido pelo sistema")

def enviar_notificacao_pedido_aprovado(pedido_id: int):
    print(f"NOTIFICAÇÃO: Pedido {pedido_id} foi aprovado! Preparar envio.")

def enviar_notificacao_pedido_cancelado(pedido_id: int):
    print(f"NOTIFICAÇÃO: Pedido {pedido_id} cancelado. Devolver estoque.")
