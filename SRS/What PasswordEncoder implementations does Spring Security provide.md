<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/PasswordEncoder #Security/Cryptography #SRS

# What PasswordEncoder implementations does Spring Security provide?

> [!abstract] Short answer
> The type you actually wire is usually [[What is DelegatingPasswordEncoder]] from [[What is PasswordEncoderFactories]] (**encode `{bcrypt}`**, **match by `{id}`**). Adaptive one-way implementations: **`BCryptPasswordEncoder`**, [[What is Pbkdf2PasswordEncoder]], **`SCryptPasswordEncoder`**, [[What is Argon2PasswordEncoder]]. [[What is NoOpPasswordEncoder]] and MD5/SHA encoders exist for **legacy match**, not new passwords. Spring Security **7.0** also adds **Password4j** siblings (`*Password4jPasswordEncoder`).

Preferred **algorithm** on the `PasswordEncoder` interface is **bcrypt**. Preferred **bean** is the **delegating** factory encoder so you can change algorithms without rewriting every row. Contract: [[What is PasswordEncoder in Spring Security]] — `encode` stores; `matches` re-derives (never decrypts).

## Current adaptive encoders

Tune so **`matches` is about one second** on your hardware. All of these **salt automatically** ([[What is salting in Spring Security password encoding]]).

| Class | Why it exists | Factory id(s) |
| --- | --- | --- |
| `BCryptPasswordEncoder` | Default **write** path; strength = log rounds (default **10**) | `bcrypt` (encode id) |
| `Pbkdf2PasswordEncoder` | Adaptive KDF; **FIPS**-oriented | `pbkdf2` (v5_5), `pbkdf2@SpringSecurity_v5_8` |
| `SCryptPasswordEncoder` | Memory-hard, slow | `scrypt` (v4_1), `scrypt@SpringSecurity_v5_8` |
| `Argon2PasswordEncoder` | PHC winner; memory-hard; needs BouncyCastle | `argon2` (v5_2), `argon2@SpringSecurity_v5_8` |

Plain `{argon2}` / `{pbkdf2}` / `{scrypt}` ids are the **older** `defaultsForSpringSecurity_*` variants. New hashes of those algorithms should use the **`@SpringSecurity_v5_8`** ids (or the v5_8 factory methods).

```java
PasswordEncoder encoder = PasswordEncoderFactories.createDelegatingPasswordEncoder();
String stored = encoder.encode("password"); // {bcrypt}$2a$10$…
boolean ok = encoder.matches("password", stored);
boolean argon2Legacy = encoder.matches("password", "{argon2}$argon2id$…");
```

**Listing 1.** Conceptual factory default: **one** bean, many match ids. Fill `…` with a real stored hash.

```d2
direction: down
factory: "PasswordEncoderFactories\n.createDelegatingPasswordEncoder()" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
dpe: "DelegatingPasswordEncoder" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
write: "encode → BCryptPasswordEncoder" {
  width: 280
  height: 50
  style.fill: "#c8e6c9"
}
read: "matches → {id} map\nbcrypt argon2 pbkdf2 scrypt noop …" {
  width: 320
  height: 70
  style.fill: "#f3e5f5"
}

factory -> dpe
dpe -> write
dpe -> read
```

**Fig. 1.** Implementations you **new** yourself vs the map the factory already built.

## Also in the box

- **`DelegatingPasswordEncoder`** — not an algorithm; `{id}` router. Custom `idForEncode` if you want Argon2/PBKDF2 **writes**.
- **`NoOpPasswordEncoder`** — identity encode; `{noop}` — tests/legacy only.
- **Deprecated digest encoders** (still mapped for **match**): `MessageDigestPasswordEncoder` (`MD5`, `SHA-1`, `SHA-256`), `Md4PasswordEncoder`, `LdapShaPasswordEncoder`, `StandardPasswordEncoder` (`sha256`). **No plans to remove**; they are **not** secure for new encodes.
- **Password4j** (Spring Security **7.0**): `Argon2Password4jPasswordEncoder`, `BcryptPassword4jPasswordEncoder`, `ScryptPassword4jPasswordEncoder`, `Pbkdf2Password4jPasswordEncoder`, `BalloonHashingPassword4jPasswordEncoder`. **Different classes**, not drop-in renames of the BouncyCastle/JDK ones.

[[What is User.withDefaultPasswordEncoder]] is a **demo `User` builder**, not a `PasswordEncoder` implementation.

> [!warning] MD5 and SHA-1 are match ids, not modern beans
> The factory still **verifies** `{MD5}` / `{SHA-1}` leftover rows. Do not `new MessageDigestPasswordEncoder("MD5")` as `idForEncode`. Adaptive list is bcrypt, PBKDF2, scrypt, Argon2 — **scrypt is first-class**, not an afterthought.

> [!warning] Skipping `DelegatingPasswordEncoder` misses the default
> A lone `BCryptPasswordEncoder` cannot `matches` `{noop}` or `{argon2}`. The recommended default is the **factory delegating** encoder. `{noop}` and Password4j classes are easy to confuse with the built-in Argon2/BCrypt types — check the **class name**.

> [!tip] Interview answer
> **Spring Security’s default is `DelegatingPasswordEncoder` from `PasswordEncoderFactories`: encode bcrypt, match by `{id}`.** Adaptive implementations are **BCrypt, PBKDF2, scrypt, and Argon2**. **NoOp, MD5, and SHA-*** are legacy/demo matchers. In **7.0**, Password4j adds parallel encoder classes — not replacements unless you choose them.
