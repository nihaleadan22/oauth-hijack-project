# OAuth 2.0 Redirect URI Hijacking Attack

## Overview
This project demonstrates the OAuth 2.0 authorization code flow and a critical vulnerability: redirect URI hijacking. A malicious server intercepts the authorization code when the OAuth provider fails to validate the `redirect_uri`.

## Files
- `auth_server.py` – OAuth provider (runs on port 5000)
- `client_app.py` – Vulnerable client (port 5001)
- `attacker.py` – Attacker server that steals the code (port 8888)

## How to Run
1. Install dependencies:
2.  Open three terminals and run each script:
3.   Visit `http://localhost:5001` to see normal login.
4. To simulate attack: change `REAL_REDIRECT` in `client_app.py` to `http://localhost:8888/callback`, restart client, and click login again.

## Demonstration
- **Normal flow**: User logs in successfully.
- **Attack**: Authorization code is sent to attacker and printed in terminal.

## Mitigation
- Strict `redirect_uri` validation (exact match)
- Use of `state` parameter (already included)
- PKCE (Proof Key for Code Exchange)

## Author
[NIHAL E ADAN]
