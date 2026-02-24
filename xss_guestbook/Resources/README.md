# XSS — Guestbook

## Vulnerability

The guestbook input field reflects user content back to the page; submitting the keyword "script" triggers the flag — OWASP A03:2021 Injection.

## Steps to Reproduce

1. Navigate to `http://<VM_IP>/index.php?page=guestbook`.
2. In the message field, type `script` and submit the form.
3. The flag appears on the page.

Alternatively, test standard XSS:
```html
<script>alert(1)</script>
```
Input is sanitized, but the literal word "script" in the message body triggers the flag response.

## Why It Works

The application detects the keyword "script" in input and returns the flag as a trigger. In a real XSS scenario, unsanitized user input is reflected into the HTML response, allowing script injection. Even with partial sanitization, blocklist-based filters are bypassable.

## Fix / Mitigation

- Use an allowlist approach: only permit known-safe HTML (or no HTML at all).
- Encode output with `htmlspecialchars()` before rendering user content.
- Set `Content-Security-Policy` headers to prevent inline script execution.
- Use a proper HTML sanitization library (e.g., HTMLPurifier).
