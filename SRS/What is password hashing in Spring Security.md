<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/PasswordEncoder #Security/Cryptography #SRS

# What is password hashing in Spring Security?

> [!abstract] Short answer
> A **one-way** transform of a password for storage: you keep the **hash**, never the secret, and at login you **`matches(raw, stored)`** — you do **not** decrypt. In Spring Security that contract is [[What is PasswordEncoder in Spring Security]]. New hashes should be an **adaptive** function (bcrypt, PBKDF2, scrypt, Argon2), not MD5 or SHA-1.

Plain-text storage is obsolete. A fast cryptographic digest (SHA-256 and friends) is also obsolete: modern hardware can try billions of guesses per second, and unsalted hashes fall to rainbow tables. Adaptive hashes are **intentionally expensive**, with a tunable **work factor**. Tune so **`matches` takes about one second** on *your* hardware. The preferred concrete algorithm is **`BCryptPasswordEncoder`**. The framework default **bean** is usually [[What is DelegatingPasswordEncoder]] from [[What is PasswordEncoderFactories]], which **encodes bcrypt** and still **matches** older `{id}` prefixes.

## One-way, not encryption

`PasswordEncoder` is the hashing API:

```java
public interface PasswordEncoder {
    String encode(CharSequence rawPassword);
    boolean matches(CharSequence rawPassword, String encodedPassword);
    default boolean upgradeEncoding(String encodedPassword) { return false; }
}
```

**Listing 1.** Conceptual `PasswordEncoder` (Spring Security **6+/7**). `encode` is for **storage**. `matches` re-derives using the **stored** salt and parameters. The stored value is **never decoded**. `matches` is never true if either argument is null or empty. `encode(null)` must return null (user with no password).

This is **not** reversible encryption. If you need to recover a secret later (for example credentials the app uses to log into a database), `PasswordEncoder` is the wrong tool.

Salted adaptive hashes **change on every `encode`**. Comparing two fresh `encode` results with `equals` is a false negative. Use `matches`. Same idea: [[Why do two identical passwords hash to different strings with BCrypt]] and [[What is the difference between encode and matches on PasswordEncoder]].

```d2
direction: right
plain: "plain text\n(do not store)" {
  width: 180
  height: 70
  style.fill: "#ffcdd2"
}
fast: "fast digest\nMD5 / SHA-1 / SHA-256" {
  width: 220
  height: 70
  style.fill: "#ffe0b2"
}
salt: "per-password salt" {
  width: 180
  height: 70
  style.fill: "#fff9c4"
}
adapt: "adaptive one-way\nbcrypt · argon2 · pbkdf2 · scrypt" {
  width: 280
  height: 80
  style.fill: "#c8e6c9"
}

plain -> fast
fast -> salt
salt -> adapt
```

**Fig. 1.** History of storage: plain text → fast hashes → salt → adaptive work factor. Spring Security’s recommended encoders live in the last box.

## What to use, what the factory still matches

Use **bcrypt**, **PBKDF2**, **scrypt**, or [[What is Argon2PasswordEncoder]]. Factory `createDelegatingPasswordEncoder()` **writes** `{bcrypt}…`. It still **reads** `{argon2}`, `{pbkdf2}`, `{scrypt}`, `{noop}`, and legacy `{MD5}` / `{SHA-1}` / `{SHA-256}` so old rows keep working. Those message-digest ids exist for **migration**, not for new encodes.

[[What is NoOpPasswordEncoder]] (`{noop}…`) stores the password in the clear after the prefix. Pre-**5.0** it was the framework default. It is `@Deprecated` and not for production.

> [!warning] MD5 and SHA-1 are not new-password encoders
> They are **fast** one-way hashes. On modern hardware they are **crackable** (including SHA-256 used alone). The factory still **maps** `{MD5}` and `{SHA-1}` so leftover rows verify. Do not set `idForEncode` to those ids, and do not `new MessageDigestPasswordEncoder("MD5")` for new users. Adaptive or go home.

> [!warning] Do not `encode` twice and `equals`
> `matches` is the comparison. Independent `encode` calls pick new salts, so the strings differ even when the password is the same. Also do not treat hashing as encryption: there is **no** `decode`.

> [!tip] Interview answer
> **Password hashing in Spring Security is `PasswordEncoder`: one-way `encode` for storage and `matches` at login, never decryption.** Use an **adaptive** hash — bcrypt by default via **`DelegatingPasswordEncoder`** — so you can still verify old `{id}` rows. **MD5/SHA-1 are legacy matchers, not algorithms for new passwords**; `{noop}` is plain text.
