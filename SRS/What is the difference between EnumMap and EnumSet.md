<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/EnumMap #Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: both are enum-specialized collections.

- `EnumMap` implements `Map`: array of values, index = key `ordinal()`.
- `EnumSet` implements `Set`: bit vector of ordinals.

Dumps say always prefer these over general `HashMap` / `HashSet` when the elements or keys are enums.

> [!warning] Unverified traps from the dump
> - `EnumSet` is about membership of constants; `EnumMap` associates a value with each constant.
