<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: you may pass `-ea`, `-da`, `-esa`, and `-dsa` together. **All flags are executed from left to right.**

Example: `java -ea -esa -dsa -ea -dsa -esa Test` — after the last flags, assertions are enabled in both system and non-system classes.

Package/class selectors are the same idea: later `-da:pack1.B` can punch a hole in an earlier `-ea:pack1`.

> [!warning] Unverified traps from the dump
> - Order matters; repeating a flag is not a no-op if an earlier flag turned the other domain on or off.
> - Default with **no** flags remains: assertions off.
