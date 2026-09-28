"""Local information-security assignment: Flask + PyCryptodome."""
import base64
import binascii
import hashlib
import json
from flask import Flask, jsonify, render_template, request
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 128 * 1024
ITERATIONS = 200_000

def b64(raw):
    return base64.b64encode(raw).decode('ascii')

def unb64(value):
    return base64.b64decode(value, validate=True)

def caesar(text, shift):
    result = []
    for char in text:
        if 'A' <= char <= 'Z':
            result.append(chr((ord(char) - 65 + shift) % 26 + 65))
        elif 'a' <= char <= 'z':
            result.append(chr((ord(char) - 97 + shift) % 26 + 97))
        else:
            result.append(char)
    return ''.join(result)

def aes_key(password, salt):
    return PBKDF2(password.encode('utf-8'), salt, dkLen=32,
                  count=ITERATIONS, hmac_hash_module=SHA256)

@app.get('/')
def index():
    return render_template('index.html')

@app.post('/api/keys')
def keys():
    key = RSA.generate(2048)
    return jsonify(public_key=key.public_key().export_key().decode(),
                   private_key=key.export_key().decode())

@app.post('/api/process')
def process():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error='Send a JSON object.'), 400
    text = data.get('text', '')
    method = data.get('method', '')
    action = data.get('action', '')
    if not isinstance(text, str) or not text.strip():
        return jsonify(error='Please enter text; empty input is not allowed.'), 400
    if len(text.encode('utf-8')) > 24000:
        return jsonify(error='Input must be at most 24,000 UTF-8 bytes.'), 400
    if method not in ('caesar', 'aes', 'rsa', 'sha256'):
        return jsonify(error='Please select a valid method.'), 400
    if action not in ('encrypt', 'decrypt'):
        return jsonify(error='Select encrypt or decrypt.'), 400
    try:
        if method == 'caesar':
            shift = int(data.get('shift', 3))
            if not 1 <= shift <= 25:
                raise ValueError('Caesar shift must be between 1 and 25.')
            result = caesar(text, shift if action == 'encrypt' else -shift)
        elif method == 'aes':
            password = data.get('password', '')
            if not isinstance(password, str) or len(password) < 8:
                raise ValueError('Use an AES password with at least 8 characters.')
            if action == 'encrypt':
                salt = get_random_bytes(16)
                cipher = AES.new(aes_key(password, salt), AES.MODE_GCM, nonce=get_random_bytes(12))
                ciphertext, tag = cipher.encrypt_and_digest(text.encode('utf-8'))
                result = json.dumps({'v': 1, 'salt': b64(salt), 'nonce': b64(cipher.nonce),
                                     'tag': b64(tag), 'ciphertext': b64(ciphertext)})
            else:
                try:
                    packet = json.loads(text)
                    if packet['v'] != 1:
                        raise ValueError()
                    salt, nonce, tag, ciphertext = [unb64(packet[k]) for k in ('salt', 'nonce', 'tag', 'ciphertext')]
                    if len(salt) != 16 or len(nonce) != 12 or len(tag) != 16:
                        raise ValueError()
                    cipher = AES.new(aes_key(password, salt), AES.MODE_GCM, nonce=nonce)
                    result = cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
                except (ValueError, KeyError, TypeError, binascii.Error):
                    raise ValueError('AES decryption failed: wrong password or damaged ciphertext.')
        elif method == 'rsa':
            try:
                key = RSA.import_key(data.get('key', ''))
            except (ValueError, IndexError, TypeError):
                raise ValueError('Paste a valid RSA PEM key, or generate a key pair.')
            if key.size_in_bits() != 2048:
                raise ValueError('This demo accepts 2048-bit RSA keys.')
            cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
            if action == 'encrypt':
                if len(text.encode('utf-8')) > 190:
                    raise ValueError('RSA supports at most 190 UTF-8 bytes in this demo. Use AES for longer text.')
                result = b64(cipher.encrypt(text.encode('utf-8')))
            else:
                if not key.has_private():
                    raise ValueError('RSA decryption requires the private key.')
                try:
                    result = cipher.decrypt(unb64(text)).decode('utf-8')
                except (ValueError, binascii.Error):
                    raise ValueError('RSA decryption failed: wrong private key or damaged ciphertext.')
        else:
            if action == 'decrypt':
                raise ValueError('SHA-256 is a one-way hash and cannot be decrypted.')
            result = hashlib.sha256(text.encode('utf-8')).hexdigest()
        return jsonify(result=result)
    except (ValueError, TypeError, OverflowError) as error:
        return jsonify(error=str(error) or 'Invalid input.'), 400

@app.errorhandler(413)
def too_large(error):
    return jsonify(error='Request too large.'), 413

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
