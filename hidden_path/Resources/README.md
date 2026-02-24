# Hidden Path Enumeration

## Vulnerability

Directory listing enabled on `/.hidden/` exposes a deeply nested tree of README files containing the flag — OWASP A01:2021 Broken Access Control.

## Steps to Reproduce

1. Browse to `http://<VM_IP>/.hidden/` — directory listing is enabled.
2. The tree has hundreds of subdirectories, each with a `README` file.
3. Run `hidden_path.py` to crawl the tree concurrently and collect all README contents:
   ```bash
   python hidden_path.py
   ```
   Output is saved to `readme.json`.
4. Search the collected content for the flag string.

## Why It Works

Apache/nginx directory listing is enabled for `/.hidden/`. The application stores a secret in a leaf README file inside a large directory tree, relying on obscurity. An automated crawler trivially enumerates all paths.

## Fix / Mitigation

- Disable directory listing (`Options -Indexes` in Apache).
- Never store secrets in files served by the web server.
- Restrict access to sensitive directories via authentication.
