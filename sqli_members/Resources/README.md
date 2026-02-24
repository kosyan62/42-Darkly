# SQL Injection — Member Search

## Vulnerability

The member search `id` parameter is concatenated directly into a SQL query — OWASP A03:2021 Injection.

## Steps to Reproduce

1. Navigate to `http://<VM_IP>/index.php?page=member&id=1`.
2. Inject a UNION SELECT payload to enumerate the database:
   ```
   http://<VM_IP>/index.php?page=member&id=1 UNION SELECT table_name, NULL FROM information_schema.tables --
   ```
3. Run `enumerate.py` to automate full extraction:
   ```bash
   python enumerate.py
   ```
4. The script finds the `users` table, extracts `Commentaire` and `countersign` columns, MD5-decodes the password, and retrieves the flag.

## Why It Works

The `id` parameter is interpolated into a SQL query string without sanitization. UNION injection allows appending arbitrary SELECT statements to read from any table the database user has access to.

## Fix / Mitigation

- Use parameterized queries / prepared statements:
  ```php
  $stmt = $pdo->prepare("SELECT * FROM members WHERE id = ?");
  $stmt->execute([$_GET['id']]);
  ```
- Enforce least-privilege DB user (read-only, limited to the app's tables).
