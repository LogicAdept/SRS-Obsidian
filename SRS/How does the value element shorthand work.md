<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: if the only element (or the one you set) is named `value`, you may omit the name: `@SuppressWarnings("unchecked")` instead of `@SuppressWarnings(value = "unchecked")`.

Marker annotations have no elements. Multi-member annotations require `name =` for each supplied member. Defaults let you omit members whose default is a constant expression.

Array members with several values need braces: `types = {1, 2}`. A single array value may omit braces in some dump examples.
> [!warning] Unverified traps from the dump
> - The shorthand is only for an element named value, not for an arbitrary single member like time().
> - Defaults must be compile-time constants; dumps reject non-constant expressions.
