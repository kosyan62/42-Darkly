# Cookie Manipulation

## Vulnerability

Authorization state stored in a client-side cookie as an MD5 hash — trivially forgeable. OWASP A02:2021 Cryptographic Failures.

## Steps to Reproduce

1. Open `http://<VM_IP>/` in a browser.
2. Inspect cookies — find `I_am_admin=68934a3e9455fa72420237eb05902327`.
3. Verify: `echo -n "false" | md5sum` → `68934a3e9455fa72420237eb05902327`
4. Compute MD5 of "true": `echo -n "true" | md5sum` → `b326b5062b2f0e69046810717534cb09`
5. Replace the cookie value with `b326b5062b2f0e69046810717534cb09` and reload.
6. Flag appears in an alert on the page.

## Why It Works

The server reads the `I_am_admin` cookie and treats its MD5-hashed value as a trustworthy authorization signal. Because MD5 is unsalted and deterministic, any value can be computed offline and injected.

## Fix / Mitigation

- Never store authorization state in client-side cookies.
- Use server-side sessions (opaque session token mapped to server state).
- If cookies must carry data, sign them with HMAC (e.g., Flask's `itsdangerous`).
