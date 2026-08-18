<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump example: `put(new String("identityKey"), "Google")` then `put(new String("identityKey"), "Facebook")`. **`IdentityHashMap` keeps both** (two entries). **`HashMap` keeps one** (second value wins: `{key=Facebook}`).

> [!warning] Unverified traps from the dump
> - `new String("x")` is two instances; interned literals `"x"` / `"x"` may be `==`.
> - “Allows duplicate-looking keys” in short interview posts means distinct references, not duplicate `==` keys.
