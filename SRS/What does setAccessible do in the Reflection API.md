<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`setAccessible(true)` on `Field`, `Method`, or `Constructor` (they share `AccessibleObject`) suppresses Java language access checks for that reflected member so private / protected / package-private members can be used.

Dumps: needed for tests, serialization, libraries you do not control. It weakens encapsulation and the security model — use only when necessary.

Java 9+ class-loading dump: deep reflection into a module that did not `opens` the package needs `--add-opens`.

> [!warning] Unverified traps from the dump
> - `setAccessible(true)` does not make the field non-private in the language sense; it suppresses checks on that reflective object.
> - JDK internals may refuse access even after `setAccessible` (module encapsulation) — verify on modern JDKs.
