# User-Agent / Referer Header Spoofing

## Vulnerability

Access to a secret page is gated on client-supplied HTTP headers (`User-Agent` and `Referer`) which are trivially spoofable — OWASP A05:2021 Security Misconfiguration.

## Steps to Reproduce

1. View the HTML source of `http://<VM_IP>/` — a comment reveals the target page and required headers.
2. The secret page URL is:
   ```
   http://<VM_IP>/index.php?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f
   ```
3. Send a request with the required headers using `req.py`:
   ```bash
   python req.py
   ```
   Headers sent:
   ```
   Referer: https://www.nsa.gov/
   User-Agent: ft_bornToSec
   ```
4. The server returns the flag.

## Why It Works

HTTP headers are set by the client and can be set to any arbitrary value. Using them as an access control mechanism provides no security — any HTTP client can spoof them.

## Fix / Mitigation

- Never use client-supplied headers for access control decisions.
- Use server-side authentication (sessions, tokens) to control access to protected pages.
- If the page must be obscure, keep the URL secret rather than relying on headers.
