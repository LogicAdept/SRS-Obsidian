<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps state that wrapper classes are `final` and that wrapper objects are immutable (like `String`). Once created, you cannot change the wrapped value; operations such as `ten++` on an `Integer` produce a new value via unbox/increment/box rather than mutating the old object.

> [!warning] Unverified traps from the dump
> - Immutability is about the object; the variable can still be reassigned to another wrapper.
> - `++` on `Integer` is allowed because of autoboxing, not because the instance is mutated.
