const $ = (id) => document.getElementById(id);
const hints = {
  caesar: 'Classical substitution: shifts English letters and preserves case, spaces, and punctuation. Educational only.',
  aes: 'Symmetric encryption: AES-256-GCM with password-derived keys and authenticated ciphertext.',
  rsa: 'Asymmetric encryption: a public key encrypts and a private key decrypts. Maximum input: 190 UTF-8 bytes.',
  sha256: 'One-way hashing: generates a 64-character hexadecimal digest. Hashes cannot be decrypted.'
};
let busy = false;
function status(message, error = false) { $('status').textContent = message; $('status').className = error ? 'error' : ''; }
function update() {
  const method = $('method').value;
  for (const name of ['caesar', 'aes', 'rsa']) $(name + '-options').hidden = name !== method;
  $('hint').textContent = hints[method] || 'Choose one of three encryption methods or generate a SHA-256 hash.';
  $('encrypt').textContent = method === 'sha256' ? 'Generate hash' : 'Encrypt';
  for (const id of ['encrypt', 'decrypt', 'keys', 'use', 'clear', 'method']) $(id).disabled = busy;
  $('decrypt').disabled = busy || method === 'sha256';
}
async function post(path, data) {
  const response = await fetch(path, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)});
  const body = await response.json();
  if (!response.ok) throw new Error(body.error || 'Request failed.');
  return body;
}
async function transform(action) {
  if (!$('method').value) return status('Please select an encryption method.', true);
  if (!$('input').value.trim()) return status('Please enter text; empty input is not allowed.', true);
  busy = true; update(); status('Processing...'); $('output').value = '';
  try {
    const data = await post('/api/process', {text: $('input').value, method: $('method').value, action,
      shift: $('shift').value, password: $('password').value,
      key: $(action === 'encrypt' ? 'public-key' : 'private-key').value});
    $('output').value = data.result; status('Done. Result is ready.');
  } catch (error) { status(error.message === 'Failed to fetch' ? 'Cannot reach Flask. Check that python app.py is still running.' : error.message, true); }
  finally { busy = false; update(); }
}
$('method').addEventListener('change', () => { $('output').value = ''; status('Ready.'); update(); });
$('encrypt').addEventListener('click', () => transform('encrypt'));
$('decrypt').addEventListener('click', () => transform('decrypt'));
$('keys').addEventListener('click', async () => {
  busy = true; update(); status('Generating RSA keys...');
  try { const data = await post('/api/keys', {}); $('public-key').value = data.public_key; $('private-key').value = data.private_key; status('RSA keys generated. Keep this page open to retain them.'); }
  catch (error) { status(error.message, true); }
  finally { busy = false; update(); }
});
$('copy').addEventListener('click', async () => {
  if (!$('output').value) return status('There is no result to copy.', true);
  try { await navigator.clipboard.writeText($('output').value); status('Result copied.'); }
  catch { $('output').focus(); $('output').select(); status('Press Ctrl+C (Mac: Cmd+C) to copy the selected result.'); }
});
$('use').addEventListener('click', () => {
  if (!$('output').value) return status('There is no result to move.', true);
  $('input').value = $('output').value; $('output').value = ''; status('Result moved to input. You can now decrypt it.');
});
$('clear').addEventListener('click', () => { $('input').value = ''; $('output').value = ''; status('Text cleared.'); });
update();
