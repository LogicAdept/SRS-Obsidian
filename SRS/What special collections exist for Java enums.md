<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/EnumMap #Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: use **`EnumSet`** and **`EnumMap`** whenever you store enums; they are the specialized `Set` / `Map` implementations and are described as very efficient.

- `EnumSet`: bit vector; a bit per ordinal. Membership is “is this bit a one”.
- `EnumMap`: array indexed by ordinal. No `hashCode`, no collision resolution.

> [!warning] Unverified traps from the dump
> - This is not “enums cannot go in `HashSet` / `HashMap`”; dumps say you *should* use the specialized types for efficiency.
