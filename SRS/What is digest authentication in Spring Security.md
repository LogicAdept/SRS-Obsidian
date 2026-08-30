<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Digest authentication hashes username, realm, password, HTTP method, and URI (MD5 in dumps) so the password is not sent in the clear like Basic. The Authorization header carries Digest username, realm, nonce, uri, response, qop, nc, cnonce.

Dumps present it as a stronger REST option than Basic. It still needs a shared secret (password or HA1) on the server and is rare next to Bearer JWT in current lists.
> [!warning] Unverified traps from the dump
> - MD5 digest as in classic HTTP Digest is not modern password hashing (BCrypt/Argon2).
> - Digest does not replace TLS; nonce replay is still a dump talking point.
