<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Each `Optional` is a heap object wrapping the value: allocation plus indirection. Fine as a method return; in hot loops or per-element stream work it adds GC pressure.

```java
Optional<User> u = find(id);  // fine

for (int i = 0; i < 10_000_000; i++) {
    Optional.of(i).map(x -> x + 1).get();  // dump: avoid
}
```

For primitives, `OptionalInt` / `OptionalLong` / `OptionalDouble` skip boxing. Use Optional for occasional returns, not as a per-element structure on a hot path.

> [!warning] Unverified traps from the dump
> - The dump’s “millions of throwaway Optionals” example also calls `get()` — a second anti-pattern.
