<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: an enum may be declared as a top-level type or nested inside a class. It **cannot** be declared inside a method.

Nested in a class, extra modifiers `private`, `protected`, and `static` are listed as allowed. Top-level: `public` and `strictfp`. An enum cannot be declared `abstract` because it is implicitly `final`. It cannot be declared `final` explicitly either (already final).

> [!warning] Unverified traps from the dump
> - Contrast with local records (Java 16+), which dumps do allow inside a method.
