<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `Integer.valueOf()` is the factory that uses the integer cache and returns a cached object for values between `-128` and `127`. `new Integer()` always creates a brand-new heap object. Autoboxing always uses `valueOf`, which is why cache identity applies.

One dump says `new Integer()` is deprecated since Java 9 and removed in Java 17, and that you should never use it in modern code. For strings: `parseInt` for a primitive, `valueOf` for an `Integer`.

> [!warning] Unverified traps from the dump
> - `new Integer(100) == new Integer(100)` is false even inside the cache range.
> - Verify the “removed in Java 17” claim; other dumps still show `new Integer` examples.
