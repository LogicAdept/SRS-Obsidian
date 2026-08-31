<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/PasswordEncoder #Security/Cryptography #SRS

# What is NoOpPasswordEncoder?

> [!abstract] Short answer
> A **deprecated** `PasswordEncoder` that **does not hash**: `encode` returns the raw password, `matches` is ordinary `String.equals`. It exists for **legacy data and tests**. Prefer an adaptive encoder (bcrypt, Argon2, PBKDF2, scrypt) behind [[What is DelegatingPasswordEncoder]]. There are **no plans to remove** it — `@Deprecated` means **insecure**, not gone.

Spring Security’s default before **5.0** was this class (plain text). The factory default is now a delegating encoder whose encode id is **bcrypt**. The map still has **`noop`**, so a stored `{noop}password` verifies as plain text while new `encode` calls write `{bcrypt}…`. Interface: [[What is PasswordEncoder in Spring Security]].

## Identity encode

The class is a **singleton**: private constructor, **`NoOpPasswordEncoder.getInstance()`**. It is `final`.

```java
PasswordEncoder encoder = NoOpPasswordEncoder.getInstance();
String stored = encoder.encode("password"); // "password"
boolean ok = encoder.matches("password", stored); // true
```

**Listing 1.** `encode` is the identity function; `matches` compares the submitted raw string to the stored string. Same password in, same password out — nothing is salted or stretched.

Under [[What is PasswordEncoderFactories]], the id is `noop`. Delegating `matches` strips `{noop}` and calls this encoder, so `{noop}secret` is the stored secret `secret`.

```java
PasswordEncoder encoder = PasswordEncoderFactories.createDelegatingPasswordEncoder();
boolean ok = encoder.matches("secret", "{noop}secret");
```

**Listing 2.** One row of plain text inside a delegating encoder. New `encoder.encode("secret")` is still `{bcrypt}$2a$…`, not `{noop}`.

Spring Boot OAuth **client-secret** samples use `{noop}…` so the default delegating encoder can match. Boot’s default in-memory user also **prefixes `{noop}`** when **no** `PasswordEncoder` **bean** is present (generated password included). That is not [[What is User.withDefaultPasswordEncoder]] — that API hashes with **bcrypt** (and is still not for production: the raw password stays in source and memory).

```d2
direction: down
raw: "raw password" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
enc: "encode()\nreturn raw unchanged" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
stored: "stored: \"password\"\nor {noop}password" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
login: "matches → String.equals" {
  width: 260
  height: 60
  style.fill: "#f3e5f5"
}

raw -> enc
enc -> stored
stored -> login
```

**Fig. 1.** No salt, no work factor, no one-way hash — comparison is string equality.

Exposing a `NoOpPasswordEncoder` `@Bean` (XML id **`passwordEncoder`**) restores the old “everything is plain text” behavior. That is a migration escape hatch from 4.2, not a production setting.

> [!warning] `{noop}` in production is the interview fail
> The stored value **is** the password after the prefix. A breach dumps credentials in the clear. `@Deprecated` plus “legacy and testing only” is the official verdict. Do not ship `NoOpPasswordEncoder.getInstance()` as your `PasswordEncoder` bean, and do not leave `{noop}` on real user rows.

> [!warning] Unprefixed plain text is not `{noop}`
> A delegating encoder with no `{id}` throws **no PasswordEncoder mapped for the id `"null"`**. Prefix the row `{noop}…`, or (worse) install this encoder as the default matcher. A bare bcrypt encoder cannot verify `{noop}…` either — only the id map can.

> [!tip] Interview answer
> **`NoOpPasswordEncoder` stores and compares passwords as plain text** — `encode` returns the input, `matches` is `equals`. It is **deprecated**, for tests and old data only; Spring Security 5 replaced it as the default with **`DelegatingPasswordEncoder`**. The `{noop}` prefix is the same idea on a single hash: never leave it on production users.
