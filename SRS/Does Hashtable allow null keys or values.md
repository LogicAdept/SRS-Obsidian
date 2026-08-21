<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/Hashtable #Java/Exceptions/Unchecked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: **neither.** `Hashtable` does not allow a null key or a null value. `HashMap` allows **one null key** and any number of null values.

A Dictionary dump: keys and values must not be null; inserting a null key or value causes `NullPointerException`. The dump’s example is `new Hashtable()`.

> [!warning] Unverified traps from the dump
> - Interview tables often stop at “no nulls”; they do not always name `NullPointerException` on `put` / `get`.
> - `ConcurrentHashMap` dumps also forbid nulls; “no nulls” is not unique to `Hashtable`.
