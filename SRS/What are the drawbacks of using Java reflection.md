<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Compilations:

- **Performance** — slower than direct calls / field access.
- **Security** — bypasses access control; `setAccessible` removes barriers.
- **Maintainability** — harder to read; names as strings.
- **Breakage** — class-structure changes become runtime errors (`NoSuchFieldException`, `NoSuchMethodException`).

Tpoint-style lists add: breaks encapsulation, can expose sensitive data.

> [!warning] Unverified traps from the dump
> - Frameworks still use it; dumps say reserve it for tools/frameworks, not everyday app code.
