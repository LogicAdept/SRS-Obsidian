<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/PasswordEncoder #Security/Cryptography #SRS

# What is PasswordEncoderFactories?

> [!abstract] Short answer
> A **final** helper (since **5.0**) with one public method: **`createDelegatingPasswordEncoder()`**. It returns a [[What is DelegatingPasswordEncoder]] whose **encode id is `bcrypt`** and whose map can still **`matches`** `{argon2}…`, `{noop}…`, `{pbkdf2}…`, and other prefixed hashes. New encodes pick the current default; old `{id}` rows keep verifying.

You do not construct `PasswordEncoderFactories` (private constructor). Call the static factory and use the result as your `PasswordEncoder` bean, or rely on Spring Security’s default, which is this same delegating type. Contract: [[What is PasswordEncoder in Spring Security]].

## What the factory actually builds

```java
PasswordEncoder encoder = PasswordEncoderFactories.createDelegatingPasswordEncoder();
String stored = encoder.encode("password");
// {bcrypt}$2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HZWzG3YB1tlRy.fqvM/BG
boolean ok = encoder.matches("password", stored);
```

**Listing 1.** Factory default (Spring Security **5+**). `encode` always goes through the **`bcrypt`** delegate and prefixes `{bcrypt}`. `matches` reads the prefix and routes.

The method is a thin wrapper: `encodingId = "bcrypt"`, fill a `Map<String, PasswordEncoder>`, `return new DelegatingPasswordEncoder(encodingId, encoders)`. Mappings as of **7.1** / current source:

- **Encode id:** `bcrypt` → `new BCryptPasswordEncoder()`
- **Also for match:** `noop`, `pbkdf2` / `pbkdf2@SpringSecurity_v5_8`, `scrypt` / `scrypt@SpringSecurity_v5_8`, `argon2` / `argon2@SpringSecurity_v5_8`
- **Legacy match only:** `ldap`, `MD4`, `MD5`, `SHA-1`, `SHA-256`, `sha256`

Versioned ids exist so a work-factor bump does not break stored hashes. Plain `{argon2}` is still [[What is Argon2PasswordEncoder]] **`defaultsForSpringSecurity_v5_2()`**; current parameters live under `{argon2@SpringSecurity_v5_8}`. Same pattern for PBKDF2 and scrypt.

**Additional mappings may be added** later and the encode algorithm may change with best practice, but **DelegatingPasswordEncoder** means existing `{id}` rows **should not** stop matching.

```d2
direction: down
factory: "PasswordEncoderFactories\n.createDelegatingPasswordEncoder()" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
dpe: "DelegatingPasswordEncoder\nidForEncode = bcrypt" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
write: "encode → {bcrypt}$2a$…" {
  width: 260
  height: 55
  style.fill: "#c8e6c9"
}
read: "matches → parse {id} → map" {
  width: 280
  height: 55
  style.fill: "#f3e5f5"
}

factory -> dpe
dpe -> write
dpe -> read
```

**Fig. 1.** One static call: bcrypt for new hashes, prefix routing for everything already stored.

Need a different write algorithm? Build **`new DelegatingPasswordEncoder(idForEncode, yourMap)`** yourself — the factory does not take a custom encode id. Keep the old ids in the map so `{bcrypt}` rows still verify.

> [!warning] `User.withDefaultPasswordEncoder()` is not this factory
> That builder hashes **in process** (result looks like `{bcrypt}…`) so samples skip a `PasswordEncoder` bean. The raw password still sits in **source and memory**. It is a **demo** convenience, not `PasswordEncoderFactories`, and not production. See [[What is User.withDefaultPasswordEncoder]].

> [!warning] `{argon2}` and `{noop}` are match ids, not the write path
> Factory `encode` is **bcrypt** until you replace the bean. `{noop}` still maps to [[What is NoOpPasswordEncoder]] so plaintext rows verify — do not leave it on real users. Switching `idForEncode` on a *custom* delegating encoder does **not** rewrite existing rows.

> [!tip] Interview answer
> **`PasswordEncoderFactories.createDelegatingPasswordEncoder()` builds the default `DelegatingPasswordEncoder`: encode as `{bcrypt}`, match by `{id}`.** That is how you migrate algorithms without invalidating every row. It is **not** `User.withDefaultPasswordEncoder()` — that sample helper is unsafe for production.
