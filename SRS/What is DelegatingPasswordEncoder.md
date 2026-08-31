<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/PasswordEncoder #Security/Cryptography #SRS

# What is DelegatingPasswordEncoder?

> [!abstract] Short answer
> A **`PasswordEncoder`** (since **5.0**) that **encodes with one algorithm** and **matches by `{id}` prefix**. `encode` writes `{bcrypt}$2a$…` (factory default). `matches` reads `{argon2}…`, `{noop}…`, `{pbkdf2}…`, and so on, and routes to that delegate. That is how you change the hashing algorithm without invalidating every stored row. Interface: [[What is PasswordEncoder in Spring Security]].

Spring Security’s default `PasswordEncoder` is this type. Build it with [[What is PasswordEncoderFactories]] (`createDelegatingPasswordEncoder()`), or pass `idForEncode` plus a `Map<String, PasswordEncoder>` yourself. Prefix and suffix default to `{` and `}`; a four-argument constructor can change them.

## Encode vs match

Format is `{id}encodedPassword`. The `id` must sit at the **start** of the stored string. If there is no `{…}` prefix, the id is **null**.

`idForEncode` selects which delegate runs on **`encode`**. The factory uses **`bcrypt`**, so new hashes look like `{bcrypt}$2a$10$…`. **`matches`** ignores that default: it parses the prefix and looks up the map. Unmapped ids (including null) throw **`IllegalArgumentException`** unless you set **`setDefaultPasswordEncoderForMatches`**.

```java
PasswordEncoder encoder = PasswordEncoderFactories.createDelegatingPasswordEncoder();

String stored = encoder.encode("password");
// {bcrypt}$2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HZWzG3YB1tlRy.fqvM/BG

boolean ok = encoder.matches("password", stored);
boolean argon2Row = encoder.matches("password", "{argon2}$argon2id$…");
```

**Listing 1.** Factory default: write bcrypt, still match other `{id}` rows. The `{argon2}` call is conceptual — use a real stored hash.

The factory map (Spring Security **7.1**) includes `bcrypt` (encode id), `noop`, `pbkdf2` / `pbkdf2@SpringSecurity_v5_8`, `scrypt` / `scrypt@SpringSecurity_v5_8`, `argon2` / `argon2@SpringSecurity_v5_8`, plus legacy `ldap`, `MD4`, `MD5`, `SHA-1`, `SHA-256`, `sha256`. Plain `{argon2}` is still the older v5_2 parameters — [[What is Argon2PasswordEncoder]].

```d2
direction: down
raw: "raw password" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
enc: "encode()\nidForEncode (bcrypt)" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
stored: "{bcrypt}$2a$…" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
login: "matches(raw, stored)" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
route: "parse {id} → map lookup" {
  width: 260
  height: 60
  style.fill: "#f3e5f5"
}
delegate: "delegate.matches\n(strip prefix first)" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

raw -> enc
enc -> stored
stored -> login
login -> route
route -> delegate
```

**Fig. 1.** One encoder for new hashes; `matches` routes by prefix and never decrypts.

Custom instance: `idForEncode` must be a key in the map. `encode` concatenates `{` + id + `}` + the delegate’s encoded string. `upgradeEncoding` is true when the stored id is **not** `idForEncode` (or when that delegate’s own `upgradeEncoding` says so).

```java
String idForEncode = "bcrypt";
Map<String, PasswordEncoder> encoders = new HashMap<>();
encoders.put(idForEncode, new BCryptPasswordEncoder());
encoders.put("noop", NoOpPasswordEncoder.getInstance());
encoders.put("argon2", Argon2PasswordEncoder.defaultsForSpringSecurity_v5_8());
PasswordEncoder encoder = new DelegatingPasswordEncoder(idForEncode, encoders);
```

**Listing 2.** Conceptual custom map. Official samples also register PBKDF2, scrypt, and versioned `@SpringSecurity_v5_8` ids.

> [!warning] No `{id}` means id `null`
> Unprefixed rows (`$2a$10$…`, plaintext, …) hit **`IllegalArgumentException`: there is no PasswordEncoder mapped for the id `"null"`**. Prefix legacy bcrypt as `{bcrypt}$2a$…`, or set **`setDefaultPasswordEncoderForMatches`** (the fallback receives the **full** stored string, prefix included). Reverting to [[What is NoOpPasswordEncoder]] is not a secure fix.

> [!warning] A bare `BCryptPasswordEncoder` has no id map
> It cannot verify `{argon2}…` or `{noop}…`. The prefix **is** the migration story: one delegating bean matches every mapped scheme while new `encode` calls keep using `idForEncode`. Changing that id does **not** rewrite old rows.

> [!warning] `{noop}` is still in the factory map
> `{noop}password` stores the secret in the clear after the prefix. It exists so demos and plaintext migrations are easy. Do not use it for production credentials.

> [!tip] Interview answer
> **`DelegatingPasswordEncoder` encodes with one algorithm and matches by `{id}` prefix**, so you can keep `{bcrypt}` as the write path while old `{noop}` or `{argon2}` rows still verify. Use **`PasswordEncoderFactories.createDelegatingPasswordEncoder()`** — that is Spring Security’s default. A stored hash **without** `{id}` throws unless you set a default matcher; a lone **`BCryptPasswordEncoder`** cannot route other schemes.
