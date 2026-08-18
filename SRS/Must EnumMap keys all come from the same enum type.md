<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/EnumMap #Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: **yes**. Every key in one `EnumMap` instance must be a constant of the **single enum type** given when the map is created. You cannot mix constants from two different enums.

The type is specified at construction, for example `new EnumMap<STATE, String>(STATE.class)`.

> [!warning] Unverified traps from the dump
> - A `HashMap<Enum, V>` could in principle mix different enum types as keys; that is exactly what dumps say not to do with `EnumMap`.
