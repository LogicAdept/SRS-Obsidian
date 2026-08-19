<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/HashSet #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **yes.** `HashSet` allows a **null** element. `add` has no null check; it is backed by `HashMap`, which allows one **null key**, so the set allows one **null**.

Same dump: `TreeSet` uses a `NavigableMap`, which **does not** allow a null key — adding `null` to a `TreeSet` throws **`NullPointerException`**.

Another dump’s HashSet bullet list: **HashSet allows null value.**

> [!warning] Unverified traps from the dump
> - “One null” is the HashMap-key story, not “many nulls.”
> - A dump that says “Set allows a single null” is false for `TreeSet` / `EnumSet` in the same compilations.
