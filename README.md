# Web-Based Text Encryption Tool

A single-page web application for encrypting, decrypting, and hashing text. The frontend is built with HTML, CSS, and JavaScript, and the backend is a Python Flask API that performs all cryptographic operations.

## Features

- **Caesar cipher**: shifts English letters by a chosen amount (non-letters are left unchanged) and can reverse the shift.
- **AES encryption**: password-based symmetric encryption using AES in GCM mode.
- **RSA encryption**: asymmetric encryption using a generated 2048-bit key pair with OAEP (SHA-256) padding.
- **SHA-256 hashing**: produces a one-way hash of the input text.
- **Decryption** for Caesar, AES, and RSA. Hashing is one-way, so Decrypt is disabled for SHA-256.
- **Use result as input** button to feed an output straight back in for decryption.
- **Copy result** button to copy the output to the clipboard.
- **Input validation** on both the frontend and the backend (empty input, missing method, missing password or keys, invalid data).

## Tech Stack

- Python 3 and Flask (backend API)
- `cryptography` library (AES-GCM, PBKDF2, RSA-OAEP)
- HTML, CSS, and vanilla JavaScript (frontend)
- `unittest` (automated tests)

## Project Structure

```
text-encryption-tool/
├── app.py              # Flask app and cryptography logic
├── requirements.txt    # Python dependencies
├── test_app.py         # Automated tests
├── templates/
│   └── index.html      # Single-page interface
├── static/
│   ├── app.js          # Frontend logic (sends JSON to the API)
│   └── style.css       # Styling
├── .gitignore
└── README.md
```

## Installation and Running (Windows)

1. Open a Command Prompt in the project folder (the one containing `app.py`).
2. Create a virtual environment:

   ```bat
   py -m venv .venv
   ```

3. Install the dependencies:

   ```bat
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

4. Start the app:

   ```bat
   .venv\Scripts\python.exe app.py
   ```

5. Open http://127.0.0.1:5000 in your browser and keep the terminal open while using the app.

If `py` is not recognized, use `python` instead. Python 3 must be installed and on your PATH. An internet connection is only needed to install packages; the app then runs locally.

## Usage

| Method | How to use |
| --- | --- |
| **Caesar** | Enter text and a shift value, then Encrypt or Decrypt. Example: shift 3 turns `Hello, World!` into `Khoor, Zruog!`. |
| **AES** | Enter text and a password, then Encrypt. Keep the entire JSON output, and Decrypt with the same password. |
| **RSA** | Click **Generate RSA key pair** once, then Encrypt. Decrypt with the matching private key. Do not regenerate keys between encrypting and decrypting. |
| **SHA-256** | Enter text and click Generate hash. Example: `abc` gives `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`. |

## How It Works

The browser sends the input and selected method as JSON to the Flask backend. The backend processes it and returns a JSON response, and the page displays the result without reloading.

- **Caesar**: shifts alphabetic characters, wrapping around the alphabet and preserving case.
- **AES**: derives a key from the password and a random salt using PBKDF2, then encrypts with AES-GCM using a random nonce. The output packet contains the salt, nonce, authentication tag, and ciphertext (Base64-encoded). GCM also verifies integrity, so modified ciphertext or a wrong password is rejected.
- **RSA**: generates a 2048-bit key pair and encrypts with the public key using OAEP with SHA-256. Decryption uses the matching private key. Maximum message length is 190 UTF-8 bytes (256-byte key size minus 66 bytes of OAEP overhead).
- **SHA-256**: computes a one-way digest of the input. It cannot be reversed.

Base64 is used only to represent binary data as text. It does not provide security.

## Running the Tests

From the project folder:

```bat
.venv\Scripts\python.exe -m unittest -v
```

## Troubleshooting

- **`ModuleNotFoundError`**: install dependencies and run the app with the same `.venv\Scripts\python.exe` interpreter.
- **Browser cannot connect**: make sure `app.py` is still running and use http://127.0.0.1:5000 rather than opening `templates/index.html` directly.
- **Port 5000 is busy**: change `port=5000` to `port=5001` at the bottom of `app.py` and visit http://127.0.0.1:5001.
- **AES decryption error**: use the original password and the complete, unmodified JSON output.
- **RSA error**: use the matching private key, and keep messages within 190 UTF-8 bytes. If the keys were lost, generate a new pair and encrypt again.
- **Copy blocked by the browser**: press `Ctrl+C` after the app selects the result.

## Limitations

- Caesar cipher is for demonstration only and is not secure.
- AES security depends on password strength; weak passwords remain weak.
- RSA keys are generated for demo use and are not stored persistently.
- There is no user authentication or message storage.
- Use only disposable demo data and keys. This project is educational and is not intended to protect real sensitive information.
