<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/Cryptography #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Never store passwords in plain text. `PasswordEncoder` is a one-way, salted hash. `BCryptPasswordEncoder` is the usual example: adaptive work factor, random salt per password, `matches(raw, encoded)` re-hashes and compares — it does not decrypt.

`DelegatingPasswordEncoder` (from `PasswordEncoderFactories.createDelegatingPasswordEncoder()`) stores an `{id}` prefix (`{bcrypt}…`, `{argon2}…`) and routes verification to the matching encoder. New hashes use the default id; old hashes still verify. That is the recommended default so you can migrate algorithms without invalidating every password.

A bare `BCryptPasswordEncoder` cannot verify a hash produced by a different scheme.

> [!warning] Unverified traps from the dump
> - `{noop}` in the delegating map is for tests only.
> - Matching must use `matches`, not `encode` twice and `equals` (salt would differ).
