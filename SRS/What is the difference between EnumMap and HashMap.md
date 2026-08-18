<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/EnumMap #Java/Collections/Map/HashMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps treat this as a collections interview comparison. Both implement `Map` (`get` / `put`).

- **Keys:** `EnumMap` accepts only enum constants of one type. `HashMap` accepts any object key, including enums.
- **Internals:** `EnumMap` is an array in declaration/`ordinal()` order. `HashMap` hashes and may collide.
- **Performance:** `EnumMap` is described as likely faster for enum keys because it skips `hashCode`.
- **Fit:** `EnumMap` is not a general-purpose map; use it when the key *is* an enum.

Both can be passed wherever a `Map` is expected.

> [!warning] Unverified traps from the dump
> - You *can* put enum keys in a `HashMap`; dumps say IDEs often suggest switching to `EnumMap`.
> - “No collision” is the dump’s claim for ordinal indexing, not a `HashMap` guarantee.
