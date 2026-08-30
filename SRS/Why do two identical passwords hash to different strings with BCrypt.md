<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/PasswordEncoder #Security/Cryptography #SRS

# Why do two identical passwords hash to different strings with BCrypt?

> [!abstract] Short answer
> **`BCryptPasswordEncoder.encode()` draws a fresh random salt on every call** and embeds **salt + work factor + hash** in the returned string. Two users with the same plaintext therefore store **different encoded values**. **`matches(raw, encoded)`** parses the stored string, re-hashes the candidate password with **that** salt and cost, and compares — it never decrypts.

## Random salt per password

Spring Security's password-storage guide describes adaptive one-way functions (bcrypt among them) as mitigating rainbow tables: **each password gets its own salt**, so identical plaintexts produce **different hashes**.

`BCryptPasswordEncoder` implements that by generating a new salt inside **`encode()`** (optionally from a supplied **`SecureRandom`**). The output is self-describing — typical form:

```
$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy
 └─┬─┘└┬┘└────────── 22-char salt ──────────┘└──── hash ────┘
  ver  cost (strength)
```

**Listing 1.** BCrypt string layout — version, work factor, salt, and hash in one column.

```java
BCryptPasswordEncoder encoder = new BCryptPasswordEncoder(); // default strength 10

String hashA = encoder.encode("Password1");
String hashB = encoder.encode("Password1");
// hashA.equals(hashB) → false

encoder.matches("Password1", hashA); // true — salt read from hashA
encoder.matches("Password1", hashB); // true — different salt, same plaintext
```

**Listing 2.** Same raw password, different encodings; verification uses the stored string, not a second `encode().equals()`.

```d2
direction: right
raw: "Plaintext\nPassword1" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}
enc1: "encode()\nsalt₁ → hash₁" {
  width: 160
  height: 60
  style.fill: "#e3f2fd"
}
enc2: "encode()\nsalt₂ → hash₂" {
  width: 160
  height: 60
  style.fill: "#fff3e0"
}
db: "DB stores\ndifferent strings" {
  width: 160
  height: 50
  style.fill: "#fce4ec"
}

raw -> enc1 -> db
raw -> enc2 -> db
```

**Fig. 1.** Salt randomizes the stored hash; equality of plaintext is checked only through `matches`.

## Work factor and migration

The **`10`** in **`$2a$10$...`** is the **log rounds / strength** (default in `BCryptPasswordEncoder` Javadoc). Higher strength makes **`encode`** and **`matches`** slower on purpose — tune it so verification takes ~1 second on your hardware, per Spring's recommendation.

Raising the encoder's strength **does not rewrite existing database rows**. Old hashes keep their embedded cost until the user logs in successfully and you **`encode()` again** (often gated by **`PasswordEncoder.upgradeEncoding(encoded)`**, which `BCryptPasswordEncoder` overrides when the stored cost is below the configured strength). See [[What is the BCrypt work factor in Spring Security]].

> [!warning] Never compare two encode() outputs with equals
> **`encode()` is for storage at registration/password change.** Login must call **`matches(rawPassword, storedHash)`** only. Comparing two **`encode()`** results always fails because salts differ. With **`DelegatingPasswordEncoder`**, stored values look like **`{bcrypt}$2a$10$...`** — see [[What is PasswordEncoder in Spring Security]] and [[What is DelegatingPasswordEncoder]].

> [!tip] Interview answer
> BCryptPasswordEncoder generates a new random salt on every encode, so identical passwords produce different stored strings. matches() extracts the salt and work factor from the stored hash and re-hashes the candidate for comparison. Raising strength does not update old rows until the user authenticates and you re-encode.
