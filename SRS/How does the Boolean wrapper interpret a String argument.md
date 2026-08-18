<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps show `Boolean` construction from `String`: `"true"`, `"True"`, `"tRUe"` all store `true`. Anything else, including `"False"` and `"SomeString"`, stores `false`.

```java
Boolean b1 = new Boolean("true");       // true
Boolean b2 = new Boolean("True");       // true
Boolean b3 = new Boolean("False");      // false
Boolean b4 = new Boolean("SomeString"); // false
```

> [!warning] Unverified traps from the dump
> - `"False"` is not parsed as boolean false via a dedicated false token in this dump — it is just “not true”, so the value is `false`.
> - This is wrapper/`String` conversion, not the `boolean` primitive itself.
