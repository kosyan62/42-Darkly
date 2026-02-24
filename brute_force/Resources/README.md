# Brute Force

## Vulnerability

HTTP login form with no rate limiting or account lockout — OWASP A07:2021 Identification and Authentication Failures.

## Steps to Reproduce

1. Navigate to `http://<VM_IP>/index.php?page=signin`
2. Run `brute_force.py` (or any HTTP client) against the form, iterating over usernames from `usernames.txt` and passwords from a wordlist.
3. The script submits POST requests to the signin form and parses the response for a success indicator.
4. Credentials found: `Aaren` / `shadow`
5. Log in — the flag appears on the page.

> **Note:** Multiple accounts share the password `shadow`. `admin` works as the most common username to try; `wil` is visible on the feedback page as a hint; `Aaren` is the first hit from the wordlist.

## Why It Works

The application imposes no limit on failed login attempts, no CAPTCHA, and no account lockout. An attacker can submit thousands of credential pairs per second until one succeeds.

## Fix / Mitigation

- Implement account lockout after N failed attempts (e.g., 5), with a time-based reset.
- Add rate limiting per IP on the login endpoint.
- Use CAPTCHA to prevent automated submissions.
- Hash passwords with bcrypt/argon2 (not MD5).
