import unittest
import os
import json
import sqlite3
from app import app
from config import settings
from database import get_db

class TestStoreAPI(unittest.TestCase):
    def setUp(self):
        # Configura banco de dados em memória ou de testes
        self.db_path_backup = settings.DATABASE_PATH
        settings.DATABASE_PATH = "test_loja.db"
        
        # Remove arquivo de banco de dados de teste anterior, se existir
        if os.path.exists("test_loja.db"):
            os.remove("test_loja.db")
            
        self.app = app.test_client()
        self.app.testing = True
        
        # Inicializa o banco de dados de teste (chama get_db para criar as tabelas e popular seeds)
        with app.app_context():
            get_db()

    def tearDown(self):
        # Fecha a conexão e remove o banco de dados temporário de testes
        from database import db_connection
        import database
        if database.db_connection:
            database.db_connection.close()
            database.db_connection = None
        if os.path.exists("test_loja.db"):
            os.remove("test_loja.db")
        settings.DATABASE_PATH = self.db_path_backup

    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "ok")
        self.assertNotIn("secret_key", data) # Garante que não há vazamento do segredo

    def test_listar_produtos(self):
        response = self.app.get('/produtos')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["sucesso"])
        self.assertGreater(len(data["dados"]), 0)

    def test_buscar_produtos_com_filtro(self):
        response = self.app.get('/produtos/busca?q=Notebook')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["sucesso"])
        self.assertEqual(data["total"], 1)
        self.assertEqual(data["dados"][0]["nome"], "Notebook Gamer")

    def test_login_sucesso(self):
        payload = {
            "email": "admin@loja.com",
            "senha": "admin123"
        }
        response = self.app.post('/login', json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["sucesso"])
        self.assertEqual(data["dados"]["email"], "admin@loja.com")

    def test_login_falha(self):
        payload = {
            "email": "admin@loja.com",
            "senha": "senha-errada"
        }
        response = self.app.post('/login', json=payload)
        self.assertEqual(response.status_code, 401)

    def test_criar_pedido_e_listar(self):
        # Cria um novo pedido para o usuário João Silva (id=2)
        payload = {
            "usuario_id": 2,
            "itens": [
                {"produto_id": 1, "quantidade": 2}, # Notebook Gamer
                {"produto_id": 2, "quantidade": 1}  # Mouse Wireless
            ]
        }
        response = self.app.post('/pedidos', json=payload)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertTrue(data["sucesso"])
        pedido_id = data["dados"]["pedido_id"]

        # Busca pedidos do usuário
        response = self.app.get('/pedidos/usuario/2')
        self.assertEqual(response.status_code, 200)
        pedidos = json.loads(response.data)["dados"]
        self.assertGreater(len(pedidos), 0)
        
        # O último pedido deve conter os detalhes
        ultimo_pedido = pedidos[-1]
        self.assertEqual(ultimo_pedido["id"], pedido_id)
        self.assertEqual(len(ultimo_pedido["itens"]), 2)
        self.assertEqual(ultimo_pedido["itens"][0]["produto_nome"], "Notebook Gamer")

    def test_relatorio_vendas(self):
        response = self.app.get('/relatorios/vendas')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["sucesso"])
        self.assertIn("faturamento_bruto", data["dados"])

    def test_admin_query_bloqueado(self):
        # Por padrão, query arbitrária deve estar desativada
        payload = {"sql": "SELECT * FROM usuarios"}
        response = self.app.post('/admin/query', json=payload)
        self.assertEqual(response.status_code, 403)

if __name__ == '__main__':
    unittest.main()
