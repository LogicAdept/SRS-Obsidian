<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Besides `Integer` (`-128` to `127` by default, high bound configurable), dumps say the same cache idea applies to:

- `Short`, `Byte`
- `Character` (`0`–`127`)
- `Boolean` (both `true` and `false` cached)

`==` on those wrappers can therefore look like value equality only inside the cached set. Always use `.equals()` for wrapper values.

> [!warning] Unverified traps from the dump
> - Do not assume `Float` or `Double` share the integer-style identity cache; this dump does not claim they do.
> - `Boolean` caching is both values, not a numeric range.
