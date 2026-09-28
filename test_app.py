"""Run with: python -m unittest -v"""
import json
import unittest
from app import app

class EncryptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.keys = cls.client.post('/api/keys').get_json()

    def call(self, method, text, action='encrypt', **kwargs):
        return self.client.post('/api/process', json=dict(method=method, text=text, action=action, **kwargs))

    def test_page_and_assets(self):
        for url in ('/', '/static/app.js', '/static/style.css'):
            with self.client.get(url) as response:
                self.assertEqual(response.status_code, 200)

    def test_caesar_known_vector_and_roundtrip(self):
        encrypted = self.call('caesar', 'Hello, World! 123', shift=3).get_json()['result']
        self.assertEqual(encrypted, 'Khoor, Zruog! 123')
        self.assertEqual(self.call('caesar', encrypted, 'decrypt', shift=3).get_json()['result'], 'Hello, World! 123')

    def test_aes_unicode_randomness_and_roundtrip(self):
        text = 'Hello اردو 🔐\nKeep spaces  '
        first = self.call('aes', text, password='DemoPass123!').get_json()['result']
        second = self.call('aes', text, password='DemoPass123!').get_json()['result']
        self.assertNotEqual(first, second)
        self.assertEqual(self.call('aes', first, 'decrypt', password='DemoPass123!').get_json()['result'], text)

    def test_aes_wrong_password_and_tampering(self):
        packet = self.call('aes', 'Secret', password='DemoPass123!').get_json()['result']
        self.assertEqual(self.call('aes', packet, 'decrypt', password='WrongPass123!').status_code, 400)
        damaged = json.loads(packet)
        damaged['tag'] = 'AAAAAAAAAAAAAAAAAAAAAA=='
        self.assertEqual(self.call('aes', json.dumps(damaged), 'decrypt', password='DemoPass123!').status_code, 400)
        self.assertEqual(self.call('aes', '{}', 'decrypt', password='DemoPass123!').status_code, 400)

    def test_rsa_roundtrip_and_public_key_rejection(self):
        encrypted = self.call('rsa', 'Hello RSA!', key=self.keys['public_key']).get_json()['result']
        self.assertEqual(self.call('rsa', encrypted, 'decrypt', key=self.keys['private_key']).get_json()['result'], 'Hello RSA!')
        self.assertEqual(self.call('rsa', encrypted, 'decrypt', key=self.keys['public_key']).status_code, 400)
        self.assertEqual(self.call('rsa', 'not ciphertext', 'decrypt', key=self.keys['private_key']).status_code, 400)

    def test_rsa_size_boundary(self):
        self.assertEqual(self.call('rsa', 'a'*190, key=self.keys['public_key']).status_code, 200)
        self.assertEqual(self.call('rsa', 'a'*191, key=self.keys['public_key']).status_code, 400)
        self.assertEqual(self.call('rsa', '🔐'*48, key=self.keys['public_key']).status_code, 400)

    def test_sha256_known_vector_and_no_decrypt(self):
        self.assertEqual(self.call('sha256', 'abc').get_json()['result'], 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')
        self.assertEqual(self.call('sha256', 'abc', 'decrypt').status_code, 400)

    def test_validation(self):
        for method, text, kwargs in [('aes', '', {}), ('caesar', '  ', {}), ('', 'hello', {}), ('des', 'hello', {}), ('caesar', 'x', {'shift':26}), ('aes', 'x', {'password':'short'}), ('rsa','x',{'key':'bad'}), ('caesar','x'*24001,{})]:
            with self.subTest(method=method, kwargs=kwargs):
                self.assertEqual(self.call(method, text, **kwargs).status_code, 400)
        self.assertEqual(self.client.post('/api/process', json=[]).status_code, 400)

if __name__ == '__main__':
    unittest.main()
