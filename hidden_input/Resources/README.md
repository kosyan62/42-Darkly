# Hidden Input Field

## Vulnerability

Password-reset email address supplied via a hidden HTML form field and trusted by the server without server-side validation — OWASP A04:2021 Insecure Design.

## Steps to Reproduce

1. Navigate to `http://<VM_IP>/index.php?page=recover`.
2. View page source — find:
   ```html
   <input type="hidden" name="mail" value="webmaster@borntosec.com">
   ```
3. Using browser DevTools, change `type="hidden"` to `type="text"`.
4. Clear the field, type any email address, and submit the form.
5. Flag appears on the page.

## Why It Works

The server takes the email address from the POST body (`mail` parameter) without checking that it matches the expected recipient. The "hidden" attribute is purely cosmetic — any HTTP client can send arbitrary values.

## Fix / Mitigation

- Store the target email address in the server-side session, not in the form.
- Never trust client-supplied values for security-sensitive parameters.
- Validate server-side that the submitted email matches the session/user record.
