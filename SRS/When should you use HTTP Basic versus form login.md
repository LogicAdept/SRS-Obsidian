<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

SpringCertified dump follow-up: HTTP Basic for machine-to-machine or simple APIs (Authorization header each request). Form login for traditional server-rendered apps (cookie session, login page). OAuth2/OIDC when you delegate login to an external IdP.

You can enable both: formLogin() and httpBasic() on the same chain in dumps.
> [!warning] Unverified traps from the dump
> - Basic on a browser app pops a native dialog and sends Base64 on every request; CSRF/cookie rules still apply if you also have a session.
