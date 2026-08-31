<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/PasswordEncoder #Security/Cryptography #SRS

# What is Pbkdf2PasswordEncoder?

> [!abstract] Short answer
> Spring Security’s **`PasswordEncoder`** for **PBKDF2** (since **4.1**): a salted, deliberately slow key-derivation function. Use **`defaultsForSpringSecurity_v5_8()`** for new hashes. It is the adaptive encoder to reach for when **FIPS** matters; the factory still **encodes bcrypt** and only **matches** `{pbkdf2}…`. Interface: [[What is PasswordEncoder in Spring Security]].

PBKDF2 sits with bcrypt, scrypt, and [[What is Argon2PasswordEncoder]] as an **adaptive one-way** function. Tune iterations so verification costs real CPU on *your* hardware. This class’s factories were aimed at about **0.5 seconds** when they were added; the general password-storage advice is about **one second**. Do not ship the 2010s iteration count.

## Parameters and defaults

Configurable: **salt length**, **iterations**, **SecretKeyFactory** algorithm (`PBKDF2WithHmacSHA1` / `SHA256` / `SHA512`), and an optional **secret** concatenated with the salt (default **empty**). PBKDF2 then runs on salt + secret + password. A new **secure-random salt** is generated on every `encode`. Stored form is **salt || derived key**, **hex** by default (`setEncodeHashAsBase64(true)` switches to Base64).

| Factory | Salt | Iterations | Algorithm | Hash |
| --- | --- | --- | --- | --- |
| `defaultsForSpringSecurity_v5_8()` | 16 bytes | 310,000 | HMAC-SHA-256 | 256 bits |
| `defaultsForSpringSecurity_v5_5()` (deprecated) | 8 bytes | 185,000 | HMAC-SHA-1 | 256 bits |

```java
Pbkdf2PasswordEncoder encoder = Pbkdf2PasswordEncoder.defaultsForSpringSecurity_v5_8();
String stored = encoder.encode("myPassword");
boolean ok = encoder.matches("myPassword", stored);
```

**Listing 1.** Current defaults (Spring Security **5.8+**). Direct `encode` does **not** add `{pbkdf2}` — that prefix appears only under [[What is DelegatingPasswordEncoder]].

`matches` slices the stored salt (encoder’s configured length) and compares with **`MessageDigest.isEqual`**. Two `encode` calls of the same password differ; never `equals` the strings. Current constructor: `Pbkdf2PasswordEncoder(secret, saltLength, iterations, algorithm)`. The old `(secret, saltLength, iterations, hashWidth)` constructor is deprecated and forces **SHA-1**.

```d2
direction: down
raw: "raw password" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
salt: "new salt + optional secret" {
  width: 260
  height: 55
  style.fill: "#fff3e0"
}
kdf: "PBKDF2\niterations · HMAC-SHA-256" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
store: "hex(salt || dk)\nor {pbkdf2}… if delegated" {
  width: 280
  height: 70
  style.fill: "#f3e5f5"
}

raw -> salt
salt -> kdf
kdf -> store
```

**Fig. 1.** Slow salted KDF; `matches` re-derives with the stored salt and never decrypts.

## `{pbkdf2}` under the factory

[[What is PasswordEncoderFactories]] **writes bcrypt**. For match it registers:

- `{pbkdf2}` → `defaultsForSpringSecurity_v5_5()` (SHA-1, 8-byte salt, 185k iterations)
- `{pbkdf2@SpringSecurity_v5_8}` → `defaultsForSpringSecurity_v5_8()`

To **encode** new passwords as PBKDF2, build your own `DelegatingPasswordEncoder` with `idForEncode` of `pbkdf2@SpringSecurity_v5_8` (or put the v5_8 instance under the `pbkdf2` key). Changing that id does not rewrite old `{bcrypt}` rows.

Spring Security **7.0** also ships **`Pbkdf2Password4jPasswordEncoder`** — a different class (Password4j; stored form `{salt}:{hash}`), not a rename of this one.

> [!warning] Factory `{pbkdf2}` is still the v5_5 work factor
> As of **7.1**, the plain **`pbkdf2`** id is **SHA-1**, **8-byte salt**, **185,000** iterations. New hashes should use **`pbkdf2@SpringSecurity_v5_8`** or **`defaultsForSpringSecurity_v5_8()`**. Mixing hex and Base64, or a different **secret**, makes `matches` fail even when the password is right.

> [!warning] Iterations are the work factor — and they age
> 185k or even 310k is a **starting point**, not a forever constant. Raise iterations (or hash algorithm) until verification is expensive on *your* CPUs. Default **encode** in Spring Security is still **bcrypt**; pick PBKDF2 when you need a **FIPS-oriented** adaptive hash, not because it is “stronger than bcrypt.”

> [!tip] Interview answer
> **`Pbkdf2PasswordEncoder` is Spring Security’s PBKDF2 hasher: salted, iterated, one-way, since 4.1.** Use **`defaultsForSpringSecurity_v5_8()`** (16-byte salt, 310k iterations, SHA-256). The factory still **encodes bcrypt** and matches `{pbkdf2}` with the **older** v5_5 parameters — use **`{pbkdf2@SpringSecurity_v5_8}`** for new PBKDF2 hashes, especially when **FIPS** is the reason you are not using bcrypt or Argon2.
