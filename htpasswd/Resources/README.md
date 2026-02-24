# .htpasswd Exposure

## Vulnerability

`.htpasswd` file accessible as static web content; credentials protected only by a weak MD5 hash — OWASP A01:2021 Broken Access Control + A02:2021 Cryptographic Failures.

## Steps to Reproduce

1. Navigate to `http://<VM_IP>/whatever/.htpasswd`.
2. The file is served directly — contents reveal a username and MD5-hashed password:
   ```
   root:437394baff5aa33daa618be47b75cb49
   ```
3. Crack the hash (MD5 of "qwerty123@"): `echo -n "qwerty123@" | md5sum`
4. Navigate to `http://<VM_IP>/admin/` and log in with `root` / `qwerty123@`.
5. Flag appears on the admin page.

## Why It Works

The `.htpasswd` file is stored inside the web root and served as a static file. Apache's `.htpasswd` mechanism protects directories but does not prevent the file itself from being downloaded.

## Fix / Mitigation

- Store `.htpasswd` outside the web root (e.g., `/etc/apache2/.htpasswd`).
- Use bcrypt for password hashing (`AuthUserFile` with `htpasswd -B`).
- Restrict access to `/.htpasswd` explicitly in Apache config:
  ```apache
  <Files ".htpasswd">
      Require all denied
  </Files>
  ```
