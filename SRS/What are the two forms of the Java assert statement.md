<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps name two statement forms.

Simple: `assert expression;` where `expression` is boolean. If true, continue; if false and assertions are on, throw `AssertionError`.

Augmented (“argumented”): `assert expression1 : expression2;` — `expression2` may be any type except `void`. It supplies the detail for `AssertionError` (stringified).

Example from dumps:

```java
assert age <= 18 : "Cannot Vote";
```

Another dump writes `assert index >= 0 : "index must be non-negative, got " + index;`

> [!warning] Unverified traps from the dump
> - Parentheses around the boolean (`assert(x > 10)`) appear in SCJP-style dumps; they are not required by the keyword syntax.
> - `expression2` is not evaluated when the boolean is true.
