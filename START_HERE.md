## 1. Start the application on Windows

1. Download the ZIP and select Extract All. Do not run it from inside the ZIP.
2. Open the extracted text-encryption-tool folder containing app.py.
3. Click File Explorer's address bar, type cmd, and press Enter.
4. Run these commands separately:

```bat
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

5. Open http://127.0.0.1:5000 in your browser. Keep the terminal open.
6. If py is unrecognized, use `python -m venv .venv` for the first command. If neither works, install Python 3 from https://www.python.org/downloads/, enable PATH if offered, and reopen Command Prompt.

Internet is needed for package installation; the application then runs locally. You do not need to activate the virtual environment.

## 2. Check the features

- Caesar: shift 3, input `Hello, World!`, Encrypt. Expected: `Khoor, Zruog!`. Click Use result as input, then Decrypt to restore the original.
- AES: password `DemoPass123!`, input `Information Security Assignment`, Encrypt. Click Use result as input, then Decrypt with the same password. Keep the entire JSON ciphertext packet.
- RSA: click Generate RSA key pair once, enter `Hello RSA!`, Encrypt, Use result as input, Decrypt. Do not regenerate keys or reload the page between operations.
- SHA-256: input `abc`, Generate hash. Expected: `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`. Decrypt is disabled.
- Validation: clear the input and try processing; also test the empty method option.
- Copy result: copy a generated result and paste it into Notepad.

Optional automated test from a second terminal in this folder:

```bat
.venv\Scripts\python.exe -m unittest -v
```

## 3. Personalize your report

1. Double-click report.html to open it in a browser.
2. Click the editable identity fields and enter your name, roll number, section, and date.
3. Press Ctrl+P, select Save as PDF, use A4/default margins, and disable browser headers/footers if shown.
4. Save as Information_Security_Report_YourRollNumber.pdf.
5. Open the PDF to verify your details and all pages. Browser edits are preserved in the printed PDF, not automatically in the original HTML.

report.pdf is also included, but has blank identity fields.

## 4. Record a 3-4 minute demonstration

Use a screen recorder you already have. On Windows, Win+G may open Xbox Game Bar; Win+Alt+R may start/stop recording the active browser. Windows 11 Snipping Tool may also offer recording. Enable your microphone if narrating, and verify the saved video plays with readable text.

Suggested sequence and narration:

- 0:00-0:20: Show the app. "This is a single-page encryption tool built with HTML, CSS, JavaScript, and a Python Flask backend. It supports three encryption methods plus hashing."
- 0:20-0:50: Show Caesar encryption/decryption. "Caesar shifts English letters. With shift three, Hello becomes Khoor. It demonstrates substitution but is not secure for real data."
- 0:50-1:30: Show AES encryption/decryption. "AES is symmetric: the same password derives the key for both operations. GCM checks integrity. The output contains salt, nonce, authentication tag, and ciphertext."
- 1:30-2:10: Generate RSA keys and show encryption/decryption. "RSA uses the public key for encryption and matching private key for decryption. This demo uses 2048-bit RSA and OAEP with SHA-256."
- 2:10-2:35: Hash abc and copy its result. "SHA-256 is a one-way hash, not encryption, so it cannot be decrypted."
- 2:35-3:00: Show empty-input/missing-method validation and briefly show app.py. "Both frontend and backend validate input. JavaScript sends JSON to Flask and displays the response without leaving this page."

Use only disposable demo data/keys. Save as Demo_YourRollNumber.mp4 if supported. The video duration above is a suggestion, not an assignment requirement.

## 5. Upload the code to GitHub

1. Sign in to https://github.com and open https://github.com/new.
2. Name the repository text-encryption-tool. Choose the visibility required by your teacher; private repositories require granting the teacher access.
3. Create it. On an empty repository use the upload-existing-file link; otherwise choose Add file > Upload files.
4. Drag app.py, requirements.txt, README.md, test_app.py, .gitignore, and the templates and static folders into the upload area. You may add your personalized report PDF too.
5. Do not upload .venv, __pycache__, private keys, or only the ZIP. Upload the actual source files. Enable hidden files to find .gitignore if needed.
6. Enter a commit message such as "Add encryption assignment" and commit.
7. Verify app.py is at the root and templates/index.html, static/app.js, and static/style.css are in their folders.
8. Copy the repository URL.

GitHub stores your code. GitHub Pages does not execute this Flask backend. A live deployment is not requested in the provided assignment.

## 6. Submit in your course portal

1. Open the Information Security assignment in your course portal.
2. Attach your personalized report PDF and demo video.
3. Paste the GitHub URL in the submission text box, or attach a text file containing it if only files are accepted.
4. If the video is too large, use a teacher-approved hosting service and submit its accessible viewing link.
5. Attach the source ZIP too if the portal/teacher requests it.
6. Click the final Submit/Turn in button, not merely Save draft.
7. Reopen the submission and check attachments and links. Save the submission receipt/screenshot.

Suggested submission text:

Name: YOUR NAME
Roll number: YOUR ROLL NUMBER
Project: Web-Based Text Encryption Tool
GitHub: YOUR REPOSITORY URL
Report: attached
Demo: attached / YOUR VIDEO LINK

## Troubleshooting

- ModuleNotFoundError: install and run using the same .venv\Scripts\python.exe interpreter.
- Browser cannot connect: leave app.py running and use http://127.0.0.1:5000, not templates/index.html.
- Port 5000 busy: change port=5000 to port=5001 at the bottom of app.py, then visit http://127.0.0.1:5001.
- AES error: use the original password and complete output JSON. Corruption is rejected.
- RSA error: use the matching private key. Encryption accepts at most 190 UTF-8 bytes. If keys were lost, generate a fresh pair and encrypt a new example.
- Copy blocked: press Ctrl+C after the app selects the result.

## Quick viva preparation

- Encryption is reversible with a key; hashing produces a one-way digest.
- AES is symmetric; RSA is asymmetric.
- GCM provides confidentiality and integrity checking.
- PBKDF2 derives an AES key from a password and salt, increasing the cost of password guessing. Weak passwords remain weak.
- Base64 only encodes binary data as text; it does not provide confidentiality.
- RSA limit: 256-byte key size minus OAEP overhead (2*32+2) equals 190 bytes.
- Decryption, hashing, and copying are implemented bonus features. User authentication/message storage is not implemented.
