<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Autoboxing is implicit initialization of wrapper objects (`Byte`, `Short`, `Integer`, `Long`, `Float`, `Double`, `Character`, `Boolean`) from the matching primitives, without an explicit constructor.

It happens on assignment to a wrapper or when passing a primitive to a method that expects the wrapper.

Dumps add rules:

- Variables require an exact primitive-to-wrapper match. Boxing a `byte` variable into `Short` without a cast to `short` is a compile error.
- Compile-time constants (literals and `final` primitives) allow extra implicit widening/narrowing before boxing, with limits: assignment with `=` only (not as a method argument without a cast), and only some conversions among `byte`/`short`/`char`/`int`.
- Integer wrappers boxed from constants in `-128 … +127` are cached, so equal values can be the same object.

```java
Integer a3 = 5; // boxing
```

> [!warning] Unverified traps from the dump
> - A `byte` variable does not autobox to `Short`/`Integer` without a primitive conversion first.
> - Cached boxed integers in `-128..127` can make `==` look like value equality.
