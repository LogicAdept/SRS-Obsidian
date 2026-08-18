<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `compareTo` follows the same order as `ordinal()` (declaration order, the enum’s natural order).

Same type:
- `0` — same ordinal
- negative — invoker’s ordinal is smaller
- positive — invoker’s ordinal is larger

Constants of two different enum types cannot be compared with `compareTo` or `==` (compile error). `equals` between two different enum types is allowed and returns `false`.

`compareTo` on `Enum` is `final` — you cannot override it to change sort order.

> [!warning] Unverified traps from the dump
> - Do not promise you can customise enum ordering via `compareTo`.
