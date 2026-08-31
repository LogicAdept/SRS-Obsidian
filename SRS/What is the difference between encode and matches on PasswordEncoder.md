<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/PasswordEncoder #Security/Cryptography #SRS

# What is the difference between encode and matches on PasswordEncoder?

> [!abstract] Short answer
> **`encode(raw)`** turns a password into a **storage string** (hash, usually with a fresh salt). **`matches(raw, encoded)`** checks a login attempt against that stored string. It **re-derives** using the **salt and cost already in `encoded`**. It **never decrypts**. Do not `encode` twice and `equals`.

[[What is PasswordEncoder in Spring Security]] also has default **`upgradeEncoding(encoded)`** (usually `false`): whether the stored value should be hashed again for a stronger cost. That is a follow-up to a successful `matches`, not a substitute for it.

## Two jobs

`encode` is for **write**. A good algorithm is an **adaptive one-way** function. `null` in must yield `null` (user with no password). Otherwise the result is a non-null encoded string.

`matches` is for **read/verify**. It returns whether the submitted raw password, once encoded **with the stored parameters**, matches storage. **Never true** if either argument is **null or empty**. The stored value is **never decoded**.

For bcrypt, Argon2, and PBKDF2, `encode` picks a **new salt** every time, so the stored string **changes**. `matches` parses that salt (and work factor) out of `encoded` and hashes the candidate the same way. [[What is salting in Spring Security password encoding]] is why two encodes of `"secret"` are unequal. Same demo: [[Why do two identical passwords hash to different strings with BCrypt]].

```java
PasswordEncoder encoder = PasswordEncoderFactories.createDelegatingPasswordEncoder();

String stored = encoder.encode("secret");
boolean loginOk = encoder.matches("secret", stored);      // true
boolean wrong = encoder.matches("other", stored);         // false
boolean naive = encoder.encode("secret").equals(stored);  // false — new salt
```

**Listing 1.** Conceptual (Spring Security **5+** factory encoder). `matches` is the comparison. A second `encode` is a **new** hash, not a verifier.

[[What is DelegatingPasswordEncoder]] adds a `{id}` on `encode` (`{bcrypt}…`) and **routes** `matches` by that prefix. A bare `BCryptPasswordEncoder` `matches` has no id map. [[What is NoOpPasswordEncoder]] is the exception where `encode` is the identity and two encodes **can** `equals` — still use `matches`; that class is not for production.

```d2
direction: right
raw: "raw password" {
  width: 160
  height: 50
  style.fill: "#e3f2fd"
}
enc: "encode()\nfresh salt + hash" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
db: "store encoded string" {
  width: 200
  height: 50
  style.fill: "#c8e6c9"
}
match: "matches(raw, stored)\nreuse stored salt/cost" {
  width: 260
  height: 70
  style.fill: "#f3e5f5"
}

raw -> enc
enc -> db
db -> match
raw -> match
```

**Fig. 1.** `encode` writes a new salted hash. `matches` reads that hash and compares one-way — no `decode`.

> [!warning] `encode` + `equals` is a false negative
> Salted encoders **must** differ on every `encode`. Authentication that hashes the login form and `equals` the database column will reject valid users. The API for that is **`matches`**.

> [!warning] `matches` is strict about empty and null
> Either side null or `""` → **false**, never a match. Unprefixed rows on a delegating encoder are a different failure: **`IllegalArgumentException`** (id `"null"`), not a quiet `false`. Empty string is not `{noop}`.

> [!tip] Interview answer
> **`encode` is for storage; `matches` is for login.** `matches` re-derives with the **stored** salt and never decrypts. **Do not encode twice and compare strings** — a new salt makes a new hash. Use `matches(raw, stored)` every time.
