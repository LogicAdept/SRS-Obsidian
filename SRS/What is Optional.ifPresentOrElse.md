<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #Java/Versions/9 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`ifPresentOrElse(consumer, runnable)` (Java 9+) runs the consumer when present and the runnable when empty.

```java
find(id).ifPresentOrElse(
    user -> System.out.println("Found " + user.getName()),
    ()   -> System.out.println("No user found")
);
```

Functional `if/else` on presence. Still side-effect oriented.

> [!warning] Unverified traps from the dump
> - Java 9+ API; Java 8 code uses a manual `if (isPresent())`.
