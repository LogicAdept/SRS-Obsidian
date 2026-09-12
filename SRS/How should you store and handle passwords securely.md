<!--
reps: 0
priority: 0
-->
#Security/Cryptography #Security/Authentication #SRS

# How should you store and handle passwords securely

> [!abstract] Short answer
> Store passwords as **salted hashes computed by a slow, memory-hard key derivation function** - Argon2id, bcrypt, scrypt, or PBKDF2 - never as plaintext, encrypted passwords, or a bare fast hash. NIST SP 800-63B requires verifiers to store secrets "in a form that is resistant to offline attacks" using a salted one-way KDF with a cost parameter; OWASP's current cheat sheet ranks Argon2id first. Handling also matters: compare in constant time, allow long passwords, check against blocklists, and rate-limit guessing.

## The storage chain

```text
password -> KDF(password, unique_salt, cost) -> stored hash + salt + params
login:    recompute -> constant-time compare -> (optionally rehash if params rose)
```

**Listing 1.** The only acceptable pipeline. The salt is per-user and stored next to the hash; its purpose is defeating precomputed and cross-user "rainbow" tables, while the cost factor defeats bulk GPU guessing.

Why each element is non-negotiable:

- **Slow KDF, not SHA/MD5**: an offline attacker hashes millions of guesses per second per GPU against raw SHA-256; Argon2id/bcrypt burn RAM and iterations to make each guess expensive.
- **Unique salt per user**: equal passwords must produce different stored hashes - otherwise the attacker sees which users share a password and can attack the cheapest account to reach all of them.
- **Cost parameters stored with the hash**: parameters evolve; rehash on successful login when the configured cost has been raised (transparent upgrade).

```java
PasswordEncoder encoder = new Argon2PasswordEncoder(16, 32, 1, 19456, 2);
// OWASP minimum area: 19 MiB memory, t=2 iterations, p=1 parallelism
String hash = encoder.encode(rawPassword);
boolean ok = encoder.matches(rawPassword, hash); // constant-time inside
```

**Listing 2.** Spring Security's Argon2 encoder with the OWASP-recommended floor. `DelegatingPasswordEncoder` reads the `{argon2id}` prefix so hashes can be upgraded without breaking old entries.

## Policy around the hash

- **Length and content**: permit at least 64 characters and all printable characters; NIST dropped composition rules (forced `!@#$`) in favor of length plus blocklist checks against known-breached and common passwords.
- **Never log the password**, avoid including it in exceptions, and strip it from request logging.
- **Rate limit and throttle** verification attempts; NIST recommends rate-limiting rather than hard expiry of passwords.
- **Pepper** (an application-wide secret added outside the database) is an optional hardening layer - it helps only if stored outside the leaked store, e.g. in a KMS.

> [!warning] "SHA-256 with a salt is fine"
> It resists rainbow tables but not brute force: SHA-256 on a GPU is blisteringly fast, so a leaked table falls to dictionary attacks user by user. The KDF's cost parameter is the actual defense - the salt only makes each attack start from zero ([[What is SHA-2]], [[What is MD5]]).

> [!tip] Interview answer
> Passwords go in as salted Argon2id (or bcrypt/PBKDF2 with tuned cost) and nothing else - never plaintext, reversible encryption, or a bare fast hash. Salts are per-user, parameters travel with the hash, verification compares in constant time, and policy allows long passphrases checked against breach blocklists. Spring's DelegatingPasswordEncoder gives you the upgrade path for free.
