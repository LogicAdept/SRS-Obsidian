<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps list several construction paths:

- Constructors from the primitive (`new Integer(55)`), from `String` (`new Integer("55")`), and type-specific cases (`new Float(55.0)` double argument vs `new Float(55.0f)`; `Character` only from `char`; `Boolean` from `boolean` or `String`).
- `valueOf` factories, including radix: `Integer.valueOf("111", 2)`.
- Autoboxing: `Integer y = 10`.

`xxxValue()` methods convert a wrapper back to a primitive (`intValue`, `floatValue`, …).

> [!warning] Unverified traps from the dump
> - `new Character(124)` is shown as a compiler error — only a `char` constructor in that dump.
> - Dumps still show `new Integer`; other materials prefer `valueOf` because of caching.
