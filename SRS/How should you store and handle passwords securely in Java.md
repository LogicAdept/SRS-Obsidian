<!--
reps: 0
priority: 0
-->
#Java/Security #SRS

# How should you store and handle passwords securely in Java

> [!abstract] Short answer
> **Store only a salted, intentionally slow hash of the password — never plaintext, never encrypt, never fast-hash (SHA-256 alone).** In the JDK: `SecretKeyFactory` with `PBKDF2WithHmacSHA256`, a random per-user salt, and a high iteration count; bcrypt/Argon2 come from vetted libraries. Verify by re-deriving and comparing with a constant-time `MessageDigest.isEqual` — and let failures stay indistinguishable.

## The pipeline

Registration: generate a random salt, run the password through a key-derivation function with many iterations, store `salt + hash + parameters`. Login: re-derive with the *stored* salt and parameters, compare. The salt kills rainbow tables and makes two equal passwords look different; the iteration count makes offline guessing expensive per attempt.

```d2
direction: down
p: "password + random salt\n+ PBKDF2, 100k+ iterations" {
  width: 340
  height: 90
  style.fill: "#e3f2fd"
}
h: "store: salt | hash | params\n(NOT the password)" {
  width: 320
  height: 90
  style.fill: "#fff3e0"
}
v: "verify: re-derive with stored\nsalt/params, compare" {
  width: 330
  height: 90
  style.fill: "#fff3e0"
}
c: "constant-time compare\nMessageDigest.isEqual" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
p -> h -> v -> c
```

**Fig. 1.** Derive once, store the derived value with its salt and parameters, re-derive and compare on every login.

```java
byte[] salt = new byte[16];
new SecureRandom().nextBytes(salt);       // one random salt PER user

PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), salt, 120_000, 256);
byte[] hash = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256")
                              .generateSecret(spec).getEncoded();

// verification: re-derive, then constant-time compare
byte[] candidate = pbkdf2(candidatePassword, storedSalt, storedIterations);
System.out.println("verify: " + MessageDigest.isEqual(hash, candidate));
```

**Listing 1.** Verified on JDK 21 (fixed all-zero demo salt, 120 000 iterations):

```java
iterations: 120000, key length: 256 bits
hash: IPvd1eHOgK2L+EErWPfM+hSrOeukmSUevwznQforpEQ=
verify right password: true
verify wrong password: false
```

**Listing 2.** The re-derivation matched only the correct password. With a random per-user salt the stored value differs for every registration, even for identical passwords.

> [!warning] Fast hashes are the classic mistake — and timing leaks do the rest
> The failure modes this question exists for. First, `MessageDigest.getInstance("SHA-256")` directly on a password: hardware does billions of SHA-256s per second, so a database leak becomes an offline dictionary attack with no cost barrier — the whole point of a slow KDF (PBKDF2 iterations, bcrypt cost factor, Argon2 memory hardness) is to make each guess expensive. Second, salt reuse: a shared or hardcoded salt lets attackers precompute once for the whole database; the salt is not secret but must be unique per user and stored alongside the hash. Third, timing: `Arrays.equals` short-circuits on the first differing byte and leaks progress; `MessageDigest.isEqual` exists to compare in constant time. Fourth, ergonomics that betray the design: rejecting passwords by length policy over ~64 chars (you may be truncating — `PBEKeySpec` takes chars, but some schemes cap input), logging passwords, or "resettable" storage — if the system can *show* a password, it was not hashed. Where credentials actually live in a Spring app: [[How do you choose among InMemoryUserDetailsManager JdbcUserDetailsManager and a custom UserDetailsService]]; for transport protection around all of this, [[How do you enable HTTPS in a Spring Boot application]].

> [!tip] Interview answer
> **Never store plaintext or even encrypted passwords — store a salted, slow hash: in the JDK, PBKDF2WithHmacSHA256 via SecretKeyFactory with a random per-user salt and a high iteration count; bcrypt or Argon2 from vetted libraries are equally right. Verify by re-deriving with the stored salt and parameters and comparing with MessageDigest.isEqual — constant-time. Fast unsalted SHA-256 or shared salts turn any leak into an offline dictionary attack.**

