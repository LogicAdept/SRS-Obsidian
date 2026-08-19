<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/Cryptography #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump DelegatingPasswordEncoder: {noop}plain means NoOpPasswordEncoder for that row. In-memory samples use {noop}password. Production dumps forbid it except tests.
> [!warning] Unverified traps from the dump
> - A mix of {noop} and {bcrypt} rows is exactly what DelegatingPasswordEncoder is for — do not point a bare BCryptPasswordEncoder at {noop} hashes.
