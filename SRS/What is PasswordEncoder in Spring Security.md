<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/PasswordEncoder #Security/Cryptography #SRS

# What is `PasswordEncoder` in Spring Security?

> [!abstract] Short answer
> **`PasswordEncoder`** one-way-hashes a password for storage and checks a login attempt with **`matches(raw, encoded)`** — it never decrypts. Prefer [[What is DelegatingPasswordEncoder]] from `PasswordEncoderFactories.createDelegatingPasswordEncoder()` so new hashes use a modern default (typically bcrypt) while old `{id}…` hashes still verify.

Spring Security’s password-storage docs treat plain-text storage as obsolete. A good encoder is an **adaptive one-way** function (bcrypt, PBKDF2, scrypt, argon2): intentionally expensive, with a tunable work factor, and (for bcrypt and peers) a **per-password salt** so identical passwords do not share a hash. See [[Why do two identical passwords hash to different strings with BCrypt]].

## Contract

```java
public interface PasswordEncoder {
    String encode(CharSequence rawPassword);
    boolean matches(CharSequence rawPassword, String encodedPassword);
    default boolean upgradeEncoding(String encodedPassword) { return false; }
}
```

**Listing 1.** Conceptual `PasswordEncoder` surface (Spring Security 6+/7). `matches` re-derives using the stored salt/parameters; the stored value is never decoded.

`encode` turns a raw password into a storage string. `matches` compares a submitted raw password to that stored string. Calling `encode` twice and comparing with `equals` fails for salted algorithms: each `encode` picks a new salt, so the strings differ even when the password is the same.

The interface JavaDoc names **`BCryptPasswordEncoder`** as the preferred concrete algorithm. Default strength is **10** log rounds (range 4–31). Since Spring Security 5, the **framework default bean** is usually a **`DelegatingPasswordEncoder`**, not a bare bcrypt instance — so you can migrate encodings without rewriting every row.

## `DelegatingPasswordEncoder` and `{id}` prefixes

```java
PasswordEncoder encoder =
    PasswordEncoderFactories.createDelegatingPasswordEncoder();

String stored = encoder.encode("password");
// e.g. {bcrypt}$2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HZWzG3YB1tlRy.fqvM/BG

boolean ok = encoder.matches("password", stored);
```

**Listing 2.** Factory default: encode with the current `idForEncode`, match by reading the `{id}` prefix.

Storage format is `{id}encodedPassword`. On `matches`, the prefix selects which delegate runs (bcrypt, argon2, pbkdf2, …). New encodes use the configured default id (commonly `bcrypt`). Legacy rows keep verifying under their original id. A bare `BCryptPasswordEncoder` alone cannot verify an `{argon2}…` or `{noop}…` string.

```d2
direction: down
raw: "raw password" {
  width: 200
  height: 60
  style.fill: "#e3f2fd"
}
enc: "encode()\n→ {bcrypt}$2a$…" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
store: "persist encoded string" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
login: "matches(raw, stored)" {
  width: 240
  height: 60
  style.fill: "#fff3e0"
}
route: "read {id} → pick encoder" {
  width: 260
  height: 60
  style.fill: "#f3e5f5"
}

raw -> enc
enc -> store
store -> login
login -> route
```

**Fig. 1.** Encode once for storage; at login, `matches` routes by `{id}` and verifies without decrypting.

> [!warning] Never `encode` twice and `equals`
> Salted hashes change on every `encode`. Authentication must use **`matches`**. Comparing two independently encoded strings is a classic false-negative.

> [!warning] `{noop}` is not a production encoder
> The delegating map still includes [[What is NoOpPasswordEncoder]] (`{noop}…`) so demos and migrations from plain text are easy. It stores the password in the clear after the prefix. Do not use it for real credentials.

Wire a `PasswordEncoder` `@Bean` when you need a non-default algorithm or work factor; otherwise Spring Security’s default delegating encoder is the migration-friendly choice. Related factory detail: [[What is PasswordEncoderFactories]].

> [!tip] Interview answer
> **`PasswordEncoder` hashes passwords one-way and verifies with `matches`, never decryption.** Use **`DelegatingPasswordEncoder`** so stored values look like `{bcrypt}…` and you can change the encoding algorithm later while old hashes still work. Always call `matches` — do not compare two fresh `encode` results.
