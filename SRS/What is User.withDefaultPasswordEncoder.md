<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/PasswordEncoder #Security/Cryptography #SRS

# What is User.withDefaultPasswordEncoder?

> [!abstract] Short answer
> A **deprecated** `User.UserBuilder` factory that **hashes the `.password(...)` you type in source** with [[What is PasswordEncoderFactories]] (`createDelegatingPasswordEncoder()`, so `{bcrypt}…`). It is for **demos and getting started only**. The raw password is still in the **bytecode and in memory** at creation. There are **no plans to remove** it; `@Deprecated` means **unsafe for production**, not gone.

It is **not** [[What is the noop password encoder id]] and **not** a `PasswordEncoder` `@Bean`. `User.withUsername("user").password("{bcrypt}$2a$…")` is the production-shaped in-memory user: you hash **outside** the app (or print `encoder.encode` once) and paste the encoded string.

## What it actually does

```java
UserDetails user = User.withDefaultPasswordEncoder()
        .username("user")
        .password("password")
        .roles("USER")
        .build();
System.out.println(user.getPassword());
// {bcrypt}$2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HZWzG3YB1tlRy.fqvM/BG
```

**Listing 1.** Official sample (Spring Security **5+** / **7.1**). The stored `UserDetails` password is a real bcrypt hash. The string `"password"` was still compiled in.

You can reuse the same builder for several users. That still leaves every raw `.password("…")` in the class file.

Production-shaped equivalent:

```java
PasswordEncoder encoder = PasswordEncoderFactories.createDelegatingPasswordEncoder();
// run once, record the printed hash, then hard-code that hash — not the raw password
System.out.println(encoder.encode("password"));

UserDetails user = User.withUsername("user")
        .password("{bcrypt}$2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HZWzG3YB1tlRy.fqvM/BG")
        .roles("USER")
        .build();
```

**Listing 2.** Hash **ahead of time**, then `withUsername`. The raw secret never sits in the builder call. Prefer a real `UserDetailsService` and hashes created outside the repo.

```d2
direction: down
raw: "\"password\" in source" {
  width: 240
  height: 50
  style.fill: "#ffcdd2"
}
enc: "withDefaultPasswordEncoder\nDelegatingPasswordEncoder.encode" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
stored: "UserDetails password\n{bcrypt}$2a$10$…" {
  width: 260
  height: 70
  style.fill: "#c8e6c9"
}

raw -> enc
enc -> stored
```

**Fig. 1.** Slightly better than `{noop}` if `UserDetails.getPassword()` leaks — the **raw** password was still in the program that built the user.

> [!warning] Not production — recoverability
> Official warning: **unsafe for production**, samples only. The plaintext is in **source** and **memory** at `build()`, so it can still be recovered. Hashing the `UserDetails` field is only a **slight** improvement over storing `{noop}password`. Hash externally; do not call this in a shipping app.

> [!warning] Do not confuse it with the factory bean
> It **calls** `PasswordEncoderFactories.createDelegatingPasswordEncoder()` **inside the builder**. Exposing that factory as a Spring `PasswordEncoder` bean is a different, normal setup. This method does **not** replace [[What is DelegatingPasswordEncoder]] for login; it only pre-hashes in-memory `User` instances.

> [!tip] Interview answer
> **`User.withDefaultPasswordEncoder()` is a demo `UserBuilder` that bcrypt-hashes the password you type in Java.** It is **deprecated** and **not for production** because the raw password remains in the class file and in memory. For real apps, **`encode` ahead of time** (or a user store) and use **`User.withUsername`** with the `{bcrypt}…` string.
