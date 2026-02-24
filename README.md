# Darkly — 42 School Web Security Project

A hands-on web security audit of a deliberately vulnerable web application. The goal: find, exploit, and document **14 security breaches** across a range of classic vulnerability categories.

All 14 breaches completed. Each directory contains a captured `flag` and a `Resources/` write-up with reproduction steps, root cause analysis, and mitigation recommendations.

---

## Breaches

| Directory | Vulnerability | OWASP |
|---|---|---|
| `brute_force` | No rate limiting on login — brute-forced with `admin` / `wil` / `Aaren` + `shadow` | A07 |
| `md5_cookie` | `I_am_admin` cookie stored as unsalted MD5 — forge admin session by flipping "false" → "true" | A02 |
| `hidden_input` | Password-reset email in hidden form field — override it with any address | A04 |
| `hidden_path` | `robots.txt` discloses `/.hidden/`; directory listing exposes 18 000+ README files | A01 |
| `htpasswd` | `.htpasswd` served from web root — MD5 hash cracked → `root` / `qwerty123@` | A01 + A02 |
| `sqli_images` | UNION-based SQL injection on `?page=searchimg&id=` — dumps `list_images` table | A03 |
| `sqli_members` | UNION-based SQL injection on `?page=member&id=` — dumps `users` table, cracks hash | A03 |
| `file_upload` | File upload checks only `Content-Type` header — upload PHP shell as `image/jpeg` | A04 |
| `open_redirect` | `?page=redirect&site=` accepts any URL — redirect to arbitrary destination | A01 |
| `path_traversal` | `?page=` used as file include without sanitization — read `/etc/passwd` via `../` | A01 |
| `form_validation` | Survey grade validated only client-side — POST out-of-range integer directly | A04 |
| `header_spoofing` | Secret page gated on `User-Agent` + `Referer` headers — trivially spoofable | A05 |
| `xss_guestbook` | Guestbook reflects input — submitting `script` triggers the flag | A03 |
| `xss_image` | `?page=media&src=` rendered in `<object data="">` — inject via `data:text/html;base64,...` | A03 |

---

## Structure

Each breach directory follows the same layout:

```
<breach>/
├── flag              ← captured flag (SHA-256 hex)
└── Resources/
    ├── README.md     ← vulnerability description, steps to reproduce, fix
    └── *.py / *.php  ← exploit scripts
```

Scripts use the `VM_IP` environment variable — no hardcoded IPs:

```bash
VM_IP=192.168.x.x python <breach>/Resources/<script>.py
```

---

## Setup

```bash
python -m venv .venv
source .venv/activate
pip install requests lxml aiohttp
```

Target: i386 ISO running in a VM. IP displayed on boot. Access at `http://<VM_IP>/`.
