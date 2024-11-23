import unittest
from flask import session
from routes import app  # Substitua pelo nome do seu arquivo se necessário

class TestAuthRoutes(unittest.TestCase):

    def setUp(self):
        """Configura o aplicativo para testes"""
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_secret_key'
        self.client = app.test_client()
        self.client.testing = True

    def test_login_valid_credentials(self):
        """Teste de login com credenciais válidas"""
        response = self.client.post('/login', json={
            'email': 'usuario1@pds2.com',
            'password': 'senha123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['logado'])
        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get('user_id'), 1)

    def test_login_invalid_credentials(self):
        """Teste de login com credenciais inválidas"""
        response = self.client.post('/login', json={
            'email': 'usuario1@pds2.com',
            'password': 'senha_errada'
        })
        self.assertEqual(response.status_code, 401)
        self.assertFalse(response.json['logado'])
        with self.client.session_transaction() as sess:
            self.assertIsNone(sess.get('user_id'))

    def test_logout_with_logged_in_user(self):
        """Teste de logout com um usuário logado"""
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
        response = self.client.post('/logout')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json['logado'])
        with self.client.session_transaction() as sess:
            self.assertIsNone(sess.get('user_id'))

    def test_logout_without_logged_in_user(self):
        """Teste de logout sem usuário logado"""
        response = self.client.post('/logout')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json['logado'])

    def test_sessao_with_logged_in_user(self):
        """Teste do endpoint de sessão com usuário logado"""
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
        response = self.client.get('/sessao')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['logado'])
        self.assertEqual(response.json['user_id'], 1)

    def test_sessao_without_logged_in_user(self):
        """Teste do endpoint de sessão sem usuário logado"""
        response = self.client.get('/sessao')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json['logado'])

if __name__ == '__main__':
    unittest.main()