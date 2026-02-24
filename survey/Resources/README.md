# Survey Form Value Bypass

## Vulnerability

Form validation enforced only on the client side (HTML `<select>` options); the server accepts any integer value — OWASP A04:2021 Insecure Design.

## Steps to Reproduce

1. Navigate to `http://<VM_IP>/index.php?page=survey`.
2. The form presents a dropdown of grades (1–10).
3. Submit a POST request with an out-of-range value using `survey.py`:
   ```bash
   python survey.py
   ```
   The script sends `sujet2=99` directly, bypassing the HTML dropdown constraint.
4. The server accepts the value and returns the flag.

## Why It Works

The `<select>` element restricts choices in the browser, but HTTP POST data is fully attacker-controlled. The server performs no server-side range or value validation.

## Fix / Mitigation

- Validate all POST parameters server-side against the same allowlist as the HTML options.
- Reject values outside the expected range with an HTTP 400 response.
- Never rely solely on HTML form constraints for security.
