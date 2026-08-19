<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/Cryptography #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps construct BCryptPasswordEncoder(strength, new SecureRandom()) with strength (work factor) often 10. Higher strength makes encode/matches slower so brute force costs more. Hardware gets faster, so dumps treat raising strength as the adaptive part of BCrypt.

encode() hashes; matches(raw, encoded) re-hashes and compares.
> [!warning] Unverified traps from the dump
> - Raising strength does not re-hash existing rows until the user logs in and you call upgradeEncoding / re-save.
