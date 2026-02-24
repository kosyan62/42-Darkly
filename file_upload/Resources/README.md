# Unrestricted File Upload

## Vulnerability

The upload endpoint validates only the MIME type (`Content-Type` header), not the file extension or content — OWASP A04:2021 Insecure Design.

## Steps to Reproduce

1. Navigate to `http://<VM_IP>/index.php?page=upload`.
2. The form accepts image uploads. Normal PHP files are rejected.
3. Send a PHP file with `Content-Type: image/jpeg` using `exploit.py`:
   ```bash
   python exploit.py
   ```
   The script POSTs `reverse.php` with the MIME type spoofed to `image/jpeg`.
4. The server accepts the upload and saves the file to `/tmp/`.
5. The flag is returned in the response.

## Why It Works

The server checks `$_FILES['file']['type']` (the MIME type from the `Content-Type` header), which is fully attacker-controlled. It does not inspect the file extension, magic bytes, or content. A PHP file disguised as an image executes as PHP when accessed.

## Fix / Mitigation

- Validate file extension against an allowlist (`.jpg`, `.png`, `.gif`).
- Validate magic bytes (file signature), not the MIME header.
- Store uploads outside the web root so they cannot be executed.
- Rename uploaded files to strip dangerous extensions.
