<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Autoboxing lets primitives and wrappers mix. The hidden cost: unboxing a `null` wrapper throws `NullPointerException`, and boxing in a tight loop creates throwaway objects (GC pressure). A classic trap is `Integer sum = 0; for (...) sum += x;` which boxes/unboxes every iteration — use a primitive `int` accumulator instead.

> [!warning] Unverified traps from the dump
> - `sum += x` on `Integer` unboxes, adds, then boxes a new `Integer`.
> - Prefer primitive accumulators in hot loops.
