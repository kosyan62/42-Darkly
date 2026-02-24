# Path Traversal

## Vulnerability

The `page` parameter is used to include files from the filesystem without sanitization, allowing traversal outside the web root — OWASP A01:2021 Broken Access Control.

## Steps to Reproduce

1. Normal page URLs look like `http://<VM_IP>/index.php?page=signin`.
2. Replace the `page` value with a traversal path:
   ```
   http://<VM_IP>/index.php?page=../../../../../../../etc/passwd
   ```
3. The contents of `/etc/passwd` are rendered in the response, and the flag appears on the page.

## Why It Works

The application reads `$_GET['page']` and uses it directly in a file-include or file-read operation (e.g., `include($_GET['page'] . '.php')`). The `../` sequences walk up the directory tree to reach arbitrary files.

## Fix / Mitigation

- Use `basename()` to strip directory components from user input.
- Maintain an allowlist of valid page names; reject anything not in it.
- Never concatenate user input into file paths or `include`/`require` calls.
- Run the web process with minimal filesystem permissions.
