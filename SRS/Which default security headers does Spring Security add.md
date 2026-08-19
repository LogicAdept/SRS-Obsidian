<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/AppSec #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps say Spring Security adds protective response headers by default:

- X-Content-Type-Options: nosniff — MIME sniffing.
- X-Frame-Options: DENY — clickjacking (iframe embed).
- Cache-Control: no-cache, no-store — caching of sensitive pages.
- Strict-Transport-Security (HSTS) — force HTTPS.
- X-XSS-Protection appears in some lists (legacy browsers).

Customize via http.headers() on the SecurityFilterChain.
> [!warning] Unverified traps from the dump
> - X-XSS-Protection is obsolete in modern browsers; dumps still list it.
> - X-Frame-Options DENY breaks legitimate same-app iframes; dumps also mention SAMEORIGIN.
