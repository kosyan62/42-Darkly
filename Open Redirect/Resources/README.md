# Open Redirect

## Vulnerability

The `site` parameter in footer social links is passed to a redirect handler without allowlist validation — OWASP A01:2021 Broken Access Control.

## Steps to Reproduce

1. Inspect any page's footer — social media links look like:
   ```
   http://<VM_IP>/index.php?page=redirect&site=facebook
   ```
2. Change the `site` parameter to any arbitrary value:
   ```
   http://<VM_IP>/index.php?page=redirect&site=https://evil.com
   ```
3. The server issues a redirect to the supplied URL and returns the flag.

## Why It Works

The application passes the `site` query parameter directly to a redirect without checking it against an allowlist of permitted destinations. Any URL — including attacker-controlled ones — is accepted.

## Fix / Mitigation

- Maintain a server-side allowlist of valid redirect targets (e.g., `facebook`, `twitter`, `instagram`) mapped to their URLs.
- Reject any `site` value not in the allowlist.
- Never construct redirect URLs from raw user input.
