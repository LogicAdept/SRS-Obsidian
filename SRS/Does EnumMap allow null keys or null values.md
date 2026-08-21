<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/EnumMap #Java/Exceptions/Unchecked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: you **cannot** insert a **null key**. `EnumMap` throws `NullPointerException`. **Null values are permitted.**

> [!warning] Unverified traps from the dump
> - This is the opposite of `HashMap` (one null key, many null values) in the usual comparison tables.
> - A `get` that returns `null` may mean “mapped to null” or “no mapping”; dumps still allow null values.
