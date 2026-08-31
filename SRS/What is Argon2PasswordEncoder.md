<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/PasswordEncoder #Security/Cryptography #SRS

# What is Argon2PasswordEncoder?

> [!abstract] Short answer
> Spring Security’s **`PasswordEncoder`** for **Argon2id**: a salted, one-way, deliberately slow hash that also spends a large, tunable amount of **memory** so custom hardware is a poor fit for cracking. Added in **5.3**. Prefer **`defaultsForSpringSecurity_v5_8()`** for new hashes; keep [[What is DelegatingPasswordEncoder]] in front so `{bcrypt}` (and older `{argon2}`) rows still **`matches`**.

It sits next to bcrypt, PBKDF2, and scrypt as an **adaptive one-way** function. Tune memory and iterations so **`matches` takes about one second** on *your* hardware — not so cheap that an attacker can try billions of guesses, not so expensive that logins stall. The class needs **BouncyCastle** on the classpath. Contract of the interface: [[What is PasswordEncoder in Spring Security]].

## Parameters and defaults

Construct with salt length, hash length, parallelism, memory cost, and iteration count. Two factories pin documented defaults (both since **5.8**):

| Factory | Salt | Hash | Parallelism | Memory | Iterations |
| --- | --- | --- | --- | --- | --- |
| `defaultsForSpringSecurity_v5_8()` | 16 bytes | 32 bytes | 1 | `1 << 14` (16384 KiB) | 2 |
| `defaultsForSpringSecurity_v5_2()` (deprecated) | 16 bytes | 32 bytes | 1 | `1 << 12` (4096 KiB) | 3 |

`v5_8` is the current starting point. `v5_2` remains only so existing hashes still verify.

```java
Argon2PasswordEncoder encoder = Argon2PasswordEncoder.defaultsForSpringSecurity_v5_8();
String stored = encoder.encode("myPassword");
boolean ok = encoder.matches("myPassword", stored);
```

**Listing 1.** Dedicated Argon2 encoder (Spring Security **5.8+** API). `encode` returns a PHC string such as `$argon2id$v=19$m=16384,t=2,p=1$…` — **no** `{argon2}` prefix unless a [[What is DelegatingPasswordEncoder]] wraps this instance.

Each `encode` draws a **fresh secure-random salt** of the configured length (`KeyGenerators.secureRandom(saltLength)`), then runs BouncyCastle **Argon2id** and embeds salt plus parameters in the stored string. Two encodes of the same password therefore differ; authentication must call **`matches`**, which re-derives using the **stored** salt and cost — the same reason bcrypt hashes differ: [[Why do two identical passwords hash to different strings with BCrypt]]. `upgradeEncoding` is true when the stored hash used **less memory or fewer iterations** than this encoder instance.

```d2
direction: down
raw: "raw password" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
salt: "new salt\nsecureRandom(saltLength)" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
hash: "Argon2id\nmemory · iterations · parallelism" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
phc: "$argon2id$v=19$m=…,t=…,p=…$…" {
  width: 300
  height: 60
  style.fill: "#f3e5f5"
}
login: "matches(raw, stored)\nre-derive with stored params" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}

raw -> salt
salt -> hash
hash -> phc
phc -> login
```

**Fig. 1.** One-way encode with a per-password salt; `matches` never decrypts.

## `{argon2}` under the factory default

`PasswordEncoderFactories.createDelegatingPasswordEncoder()` still **encodes with bcrypt**. Argon2 is registered for **matching** only, under two ids ([[What is PasswordEncoderFactories]]):

- `{argon2}` → `defaultsForSpringSecurity_v5_2()` (the older, smaller-memory parameters)
- `{argon2@SpringSecurity_v5_8}` → `defaultsForSpringSecurity_v5_8()`

So a stored `{argon2}$argon2id$…` verifies while new `encode` calls still produce `{bcrypt}$2a$…`. That is the migration story: change what you **write**, keep verifying what you **already stored**. A bare `Argon2PasswordEncoder` cannot verify a `{bcrypt}…` string.

To **encode** new passwords as Argon2, build your own `DelegatingPasswordEncoder` and set `idForEncode` to `argon2@SpringSecurity_v5_8` (or put the v5_8 instance under the `argon2` key yourself). Do not assume the factory’s `argon2` id is the v5_8 work factor.

```java
String idForEncode = "argon2@SpringSecurity_v5_8";
Map<String, PasswordEncoder> encoders = new HashMap<>();
encoders.put("bcrypt", new BCryptPasswordEncoder());
encoders.put("argon2", Argon2PasswordEncoder.defaultsForSpringSecurity_v5_2());
encoders.put(idForEncode, Argon2PasswordEncoder.defaultsForSpringSecurity_v5_8());
PasswordEncoder encoder = new DelegatingPasswordEncoder(idForEncode, encoders);

String stored = encoder.encode("myPassword");
// {argon2@SpringSecurity_v5_8}$argon2id$v=19$m=16384,t=2,p=1$…
boolean ok = encoder.matches("myPassword", stored);
boolean legacyBcrypt = encoder.matches("myPassword", "{bcrypt}$2a$10$…");
```

**Listing 2.** Conceptual custom delegating encoder: new hashes use v5_8 Argon2; `{bcrypt}` and `{argon2}` (v5_2) rows still match. Fill `…` with a real stored hash.

> [!warning] `{argon2}` is not the v5_8 work factor
> As of Spring Security **7.1**, the factory still maps the plain **`argon2`** id to **`defaultsForSpringSecurity_v5_2()`** (4096 KiB, 3 iterations). Switching `idForEncode` to `"argon2"` encodes with those **older** parameters. Use **`argon2@SpringSecurity_v5_8`** or construct **`defaultsForSpringSecurity_v5_8()`** yourself.

> [!warning] Changing `idForEncode` does not rewrite rows
> Only **new** `encode` calls pick the new id. Existing `{bcrypt}…` (or `{argon2}…`) strings stay as they are and keep matching through the map. Hashes are one-way: there is no bulk convert of stored strings to Argon2 without the raw password.

> [!warning] BouncyCastle, and a defender/attacker gap
> `Argon2PasswordEncoder` **requires BouncyCastle**. This implementation **does not exploit parallelism and optimizations that crackers will**, so the defender pays more than a tuned attacker for the same parameters. Raise memory/iterations on *your* hardware; do not assume the factory numbers are enough. Spring Security **7.0** also ships a separate **`Argon2Password4jPasswordEncoder`** — a different class, not a drop-in rename.

> [!tip] Interview answer
> **`Argon2PasswordEncoder` is Spring Security’s Argon2id password hash: salted, one-way, and memory-hard, since 5.3.** Use **`defaultsForSpringSecurity_v5_8()`**, and keep **`DelegatingPasswordEncoder`** so you can still verify `{bcrypt}` while new hashes can be `{argon2@SpringSecurity_v5_8}`. Changing the default id does **not** rewrite old rows — only new `encode` calls change. Always **`matches`**, never `equals` on two fresh `encode` results.
