<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/Exceptions #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Interview dumps: **no null keys**, **yes multiple null values**.

Natural-order `TreeMap` rejects a null key because `compareTo` compared with `null` throws `NullPointerException`. With a **user-defined `Comparator`**, dumps say it **depends** on whether `compare` accepts null.

Harp-style table: `HashMap` allows one null key; `TreeMap` does not allow null keys but can have multiple null values. One dump’s `TreeMap` overview also says “this implementation does not allow nulls” (keys and values lumped together).

> [!warning] Unverified traps from the dump
> - “Does not allow nulls” vs “null values are OK” is a common dump contradiction; prefer the split (no null key / null values allowed) that the HashMap-vs-TreeMap tables use.
> - A custom comparator that treats null as a key is the dump’s exception to “never a null key.”
