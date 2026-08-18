<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`ifPresent(consumer)` runs the action only when a value is present; it does nothing when empty.

```java
u.ifPresent(user -> System.out.println(user.getName()));

if (u.isPresent()) {
    System.out.println(u.get().getName());
}
```

It takes a `Consumer` — side effects (print, save), not a return value. For both branches, use `ifPresentOrElse`.

> [!warning] Unverified traps from the dump
> - Do not use `ifPresent` when you need to compute and return a value — dumps point at `map` / `orElse`.
