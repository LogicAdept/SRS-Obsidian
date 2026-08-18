<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: the second argument of `assert(b) : e;` may be a **method call**, but a **`void` method is not allowed** — compile-time error (“void type not allowed here”).

If the method returns a value (dump: `methodOne()` returns `999`), a failed assert can produce `AssertionError: 999`.

> [!warning] Unverified traps from the dump
> - The method still must not be used as required side-effecting logic; it only runs when the boolean is false and assertions are on.
