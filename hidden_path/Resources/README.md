# Hidden Path Enumeration

## Vulnerability

`robots.txt` discloses a restricted path `/.hidden/`, and directory listing is enabled there — exposing a tree of 18 000+ README files containing the flag — OWASP A01:2021 Broken Access Control.

## Steps to Reproduce

1. Browse to `http://<VM_IP>/robots.txt` — it lists `/.hidden` as disallowed, revealing its existence.
2. Navigate to `http://<VM_IP>/.hidden/` — directory listing is enabled, showing hundreds of subdirectories.
3. Run `hidden_path.py` to crawl the tree concurrently and find the README containing the flag:
   ```bash
   python hidden_path.py
   ```
4. The script scans all README files and prints the flag when found.

## Why It Works

Two flaws compound each other: `robots.txt` is used as a security mechanism (it is not — it's a search engine hint), and Apache directory listing is left enabled. The flag is hidden by obscurity inside a large directory tree, but an automated crawler trivially enumerates all 18 000+ paths.

## Fix / Mitigation

- Never list sensitive paths in `robots.txt` — it is publicly readable.
- Disable directory listing (`Options -Indexes` in Apache).
- Never store secrets in files served by the web server.
- Restrict access to sensitive directories via authentication.
