<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Instance fields need an instance: `get(obj)` / `set(obj, value)`.

Static fields belong to the class: dumps say `get(null)` and `set(null, value)`.

Same `getDeclaredField` + `setAccessible(true)` story for non-public statics.

> [!warning] Unverified traps from the dump
> - Passing a random instance for a static field is unnecessary; dumps use `null`.
