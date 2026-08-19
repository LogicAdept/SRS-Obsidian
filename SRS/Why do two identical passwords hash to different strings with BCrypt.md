<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/Cryptography #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: BCryptPasswordEncoder generates a random salt per encode. Two users with Password1 still store different hashes. matches() uses the salt embedded in the stored value.
> [!warning] Unverified traps from the dump
> - Work factor (strength) is also in the encoded string. Raising strength does not rewrite old hashes until the user authenticates and you re-encode.
