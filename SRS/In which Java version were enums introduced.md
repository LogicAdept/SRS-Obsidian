<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Compilations place Java enums in JDK 1.5 / Java 5. They are a type-safe list of named constants (days of the week, coins, states), richer than C/C++ enumerations: fields, constructors, methods, `switch`, and their own namespace.

Constants are described as implicitly `static` and `final`.

> [!warning] Unverified traps from the dump
> - Older dumps contrast this with the pre-1.5 `public static final int` / String constant patterns.
