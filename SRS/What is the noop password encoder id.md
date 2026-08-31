<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/PasswordEncoder #Security/Cryptography #SRS

# What is the noop password encoder id?

> [!abstract] Short answer
> The DelegatingPasswordEncoder map key **`noop`**. A stored value **`{noop}password`** means: strip the prefix, then [[What is NoOpPasswordEncoder]] — the remaining string **is** the password. Factory `encode` still writes **`{bcrypt}`**; `{noop}` is for **matching** leftover plaintext rows and samples, not for new production hashes.

Format is `{id}encodedPassword`. The id must be at the **start**, wrapped in `{` `}`. [[What is PasswordEncoderFactories]] registers `noop` → `NoOpPasswordEncoder.getInstance()`. Official examples of the same raw password `"password"` include `{noop}password` next to `{bcrypt}$2a$10$…`.

## Match id, not encode id

```java
PasswordEncoder encoder = PasswordEncoderFactories.createDelegatingPasswordEncoder();

boolean ok = encoder.matches("password", "{noop}password");
String newlyStored = encoder.encode("password");
// newlyStored starts with {bcrypt}, not {noop}
```

**Listing 1.** Factory default (Spring Security **5+**). `matches` routes `{noop}…` to the no-op encoder. `encode` uses **`idForEncode = bcrypt`**.

That mix is the point of [[What is DelegatingPasswordEncoder]]: verify `{noop}` and `{bcrypt}` (and `{argon2}`, …) with **one** bean. A bare `BCryptPasswordEncoder` has **no** id map and cannot verify `{noop}password`.

Unprefixed `"password"` is **not** the noop id. With the factory encoder, `matches("password", "password")` throws **no PasswordEncoder mapped for the id `"null"`**. You must store `{noop}password`, or set a default matcher — not a production plan.

Spring Boot OAuth **client-secret** samples use `{noop}secret…` so the default delegating encoder can match. Boot’s default in-memory user **prefixes `{noop}`** only when **no** `PasswordEncoder` **bean** exists. [[What is User.withDefaultPasswordEncoder]] hashes **bcrypt**; it is not this id.

```d2
direction: down
stored: "{noop}password" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
parse: "id = noop\nrest = password" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
delegate: "NoOpPasswordEncoder\nmatches by String.equals" {
  width: 280
  height: 70
  style.fill: "#ffe0b2"
}

stored -> parse
parse -> delegate
```

**Fig. 1.** The id selects the encoder; after `{noop}` there is no hash — only the secret.

> [!warning] `{noop}` in production is plaintext
> After the prefix, the credential is sitting in the database in the clear. The factory keeps `noop` so **demos and migrations from plain text** can `matches`. Do not set `idForEncode` to `"noop"`, and do not leave `{noop}` on real user rows.

> [!warning] `{noop}` is case-sensitive and not `{NoOp}`
> Lookup is the map key **`noop`**. A typo or `{NOOP}` is an **unmapped id** (`IllegalArgumentException`) unless you registered it. `{bcrypt}` rows are the write path; pointing a **bare bcrypt encoder** at `{noop}…` will not verify.

> [!tip] Interview answer
> **`noop` is the DelegatingPasswordEncoder id for plaintext:** `{noop}secret` stores `secret` and matches with `NoOpPasswordEncoder`. The factory **still encodes `{bcrypt}`**; `{noop}` exists so old or sample rows can verify. Never ship it as the write id or on production users — a lone `BCryptPasswordEncoder` cannot read `{noop}` hashes.
