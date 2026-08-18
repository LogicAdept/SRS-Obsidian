<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Use the compiler-generated static `values()` method. It returns an array of constants in declaration order.

```java
for (Day day : Day.values()) {
    System.out.println(day);
}
```

One dump: `values()` is implicit on the enum type and is **not** declared on `java.lang.Enum` or `Object`. Other dumps say you “get `values()` because you extend `Enum`.”

> [!warning] Unverified traps from the dump
> - `values()` allocates a new array on each call in some interview follow-ups — not stated in these compilations; do not invent a cache rule here.
