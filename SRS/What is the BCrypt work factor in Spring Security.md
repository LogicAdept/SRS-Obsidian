<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/PasswordEncoder #Security/Cryptography #SRS

# What is the BCrypt work factor in Spring Security?

> [!abstract] Short answer
> On `BCryptPasswordEncoder` it is the **`strength`** constructor argument — bcrypt **log rounds**. Default **10**, legal range **4–31**. Each extra round **exponentially** increases the CPU for `encode` and for `matches` of hashes created at that strength. Raise it over time as hardware gets faster; tune so verification takes about **one second** on *your* machines.

Spring names this **strength**; bcrypt literature calls the same number **log rounds** / **work factor**. `new BCryptPasswordEncoder()` and `new BCryptPasswordEncoder(strength, random)` both use it. A `SecureRandom` only affects **salt** generation, not the round count. Salt vs work factor: [[What is salting in Spring Security password encoding]].

## How strength is applied

`encode` calls `BCrypt.gensalt(version, strength, random)` then `hashpw`. The log rounds are **written into** the stored string (`$2a$10$…` vs `$2a$16$…`). `matches` runs `BCrypt.checkpw` against that string, so **login cost follows the stored rounds**, not whatever strength the encoder bean has now.

```java
BCryptPasswordEncoder encoder = new BCryptPasswordEncoder(16);
String stored = encoder.encode("myPassword");
boolean ok = encoder.matches("myPassword", stored);
```

**Listing 1.** Official-style construction (Spring Security **7**). Strength **16** is an example, not a new default — the no-arg constructor still uses **10**. Values other than **-1** (meaning “use 10”) that fall outside **4–31** throw `IllegalArgumentException` (`Bad strength`).

`upgradeEncoding` is true when the **stored** log rounds are **less than** this encoder’s strength. That is a signal to `encode` again and **save**; the encoder does not update the database.

```d2
direction: down
str: "strength N\n(log rounds, default 10)" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
enc: "encode → gensalt(N)\n$2a$N$…" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
login: "matches → checkpw\nuses stored N" {
  width: 240
  height: 70
  style.fill: "#c8e6c9"
}
up: "upgradeEncoding\nif stored N < bean N" {
  width: 260
  height: 70
  style.fill: "#f3e5f5"
}

str -> enc
enc -> login
enc -> up
```

**Fig. 1.** New hashes use the bean’s strength. Old `$2a$10$` rows still verify at cost 10 until you re-encode.

Factory [[What is DelegatingPasswordEncoder]] still **encodes** with `new BCryptPasswordEncoder()` (strength **10**) unless you put a stronger instance in the map. Changing the bean does **not** rewrite `{bcrypt}$2a$10$…` rows. Comparison API: [[What is the difference between encode and matches on PasswordEncoder]].

> [!warning] Default 10 is a starting point, not a forever setting
> Adaptive hashes are supposed to get **more expensive** as hardware improves. Tune until **`matches` is about one second** on production-like CPUs. Strength **16** in the constructor example is “heavier,” not a mandate. Too high **DoS**es your own login thread pool — bcrypt is CPU-bound and **exponential**.

> [!warning] Raising strength does not re-hash existing rows
> Users who still have `$2a$10$…` keep logging in at **10** rounds. `upgradeEncoding` only **reports** that the stored cost is behind. You must `encode` the raw password (typically after a successful `matches`) and **persist** the new string. There is no bulk convert without the plaintext.

> [!tip] Interview answer
> **BCrypt’s work factor in Spring Security is `BCryptPasswordEncoder` strength — log rounds, default 10, range 4–31.** Higher strength makes hashing **exponentially** slower; embed that number in `$2a$N$…`. Raising the bean does **not** rewrite old rows — `matches` uses the **stored** rounds until you re-`encode` and save.
