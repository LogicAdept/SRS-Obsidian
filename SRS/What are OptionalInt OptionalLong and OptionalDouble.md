<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Primitive specializations: hold `int` / `long` / `double` without boxing. Primitive streams return them from `max`, `min`, `average`, `findFirst`.

```java
OptionalInt max = IntStream.of(3, 7, 2).max();
int result = max.getAsInt();  // not get()
double avg = IntStream.rangeClosed(1, 5).average().orElse(0);
```

Accessors: `getAsInt` / `getAsLong` / `getAsDouble`. Dumps: no `map` / `flatMap` / `filter` — minimal, for a possibly absent primitive result.

> [!warning] Unverified traps from the dump
> - `get()` does not exist on these types in the dump — `getAsInt` and friends.
