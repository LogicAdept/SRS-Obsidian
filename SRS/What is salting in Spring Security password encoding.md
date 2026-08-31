<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/PasswordEncoder #Security/Cryptography #SRS

# What is salting in Spring Security password encoding?

> [!abstract] Short answer
> A **per-password random value** mixed into the hash so the **same password does not produce the same stored string**, and **rainbow tables** stop working. Adaptive [[What is PasswordEncoder in Spring Security]] implementations **generate the salt on `encode`** and **embed it in the encoded string**. You store **one** column (`{id}…` + hash), not a separate salt field. `matches` reads that salt back; it never decrypts.

Without a unique salt, every user with `password` shares one digest. Attackers precompute a table once and look everyone up. With a unique salt, each row is a different hash, so the table does not apply. That is why two `encode` calls differ: [[Why do two identical passwords hash to different strings with BCrypt]].

## Where the salt lives

Spring Security’s recommended encoders **do not** ask you to pass a salt. They draw a new one and concatenate or format it into the return value of `encode`:

| Encoder | Salt | Stored with the hash |
| --- | --- | --- |
| `BCryptPasswordEncoder` | `BCrypt.gensalt` (default strength 10) | Inside `$2a$10$…` (salt is part of that bcrypt string) |
| `Pbkdf2PasswordEncoder` | `KeyGenerators.secureRandom` (16 bytes on v5_8) | Prefix of the hex/Base64 blob (salt \|\| derived key) |
| `Argon2PasswordEncoder` | `KeyGenerators.secureRandom` (16 bytes on v5_8) | Inside `$argon2id$v=19$m=…$<salt>$<hash>` |

```java
PasswordEncoder encoder = PasswordEncoderFactories.createDelegatingPasswordEncoder();
String a = encoder.encode("secret");
String b = encoder.encode("secret");
boolean samePassword = encoder.matches("secret", a) && encoder.matches("secret", b);
boolean sameString = a.equals(b); // false — new salt each encode
```

**Listing 1.** Conceptual: identical passwords, different stored strings. Compare with **`matches`**, never `equals` on two encodes.

The 3.1 crypto `PasswordEncoder` (`StandardPasswordEncoder`) already generated an **8-byte random salt** per encode so “each hash is unique when the same password is used multiple times.” That is **not** a global “all passwords are salted” switch: [[What is NoOpPasswordEncoder]] still stores the raw secret. `StandardPasswordEncoder` itself is **deprecated** (iterated SHA-256 is not an adaptive winner). Prefer bcrypt / [[What is Pbkdf2PasswordEncoder]] / [[What is Argon2PasswordEncoder]] behind [[What is DelegatingPasswordEncoder]].

A **site-wide secret** (pepper) on `StandardPasswordEncoder` or PBKDF2 is **not** a salt: it is the same extra bytes for every user, kept **out** of the password database. Salt is **unique per encode** and **stored with the hash** (it is not a secret).

```d2
direction: down
raw: "same password" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
s1: "salt A (random)" {
  width: 180
  height: 50
  style.fill: "#fff3e0"
}
s2: "salt B (random)" {
  width: 180
  height: 50
  style.fill: "#fff3e0"
}
h1: "hash A + salt A\nin one stored string" {
  width: 220
  height: 70
  style.fill: "#c8e6c9"
}
h2: "hash B + salt B\nin one stored string" {
  width: 220
  height: 70
  style.fill: "#c8e6c9"
}

raw -> s1
raw -> s2
s1 -> h1
s2 -> h2
```

**Fig. 1.** One password, two salts, two stored values. Rainbow tables keyed on the password alone miss both.

> [!warning] Fast unsalted MD5 / SHA-256 is the old model
> A single SHA-256 of the password is **crackable** on modern hardware and **rainbow-table** friendly if the salt is missing or shared. Factory `{MD5}` / `{SHA-1}` / `{SHA-256}` ids still **match** leftover rows. Do not use them as `idForEncode`. Salt **inside** `StandardPasswordEncoder` does not make that class a modern choice either — it is still a fast-ish digest, not bcrypt/Argon2/PBKDF2.

> [!warning] Do not add a second salt column for bcrypt
> For BCrypt, PBKDF2, and Argon2 the encoded value **already contains** the salt. A extra column you concatenate yourself will not be what `matches` reads. `{bcrypt}` on a delegating encoder is an **algorithm id**, not a salt. [[What is NoOpPasswordEncoder]] (`{noop}`) has **no** salt at all.

> [!tip] Interview answer
> **Salting is a unique random value mixed into each password hash so identical passwords do not share a digest and rainbow tables fail.** In Spring Security, bcrypt, PBKDF2, and Argon2 **generate the salt on `encode` and store it in the encoded string** — you do not keep a separate salt column. Always **`matches`**; two `encode` results of the same password are supposed to differ.
