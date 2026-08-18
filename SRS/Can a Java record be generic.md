<!--
reps: 0
priority: 0
-->
#Java/Language/Records #Java/Generics #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Yes. Records take type parameters like ordinary classes.

```java
record Pair<A, B>(A first, B second) {}
record Result<T>(T value, String message) {}
record ApiResponse<T>(int status, T data, String message) {}

Pair<String, Integer> p = new Pair<>("hello", 42);
p.first();
p.second();

record ListNode<T>(T value, ListNode<T> next) {}
```

Dumps call generic records a replacement for generic tuples / wrappers. Type bounds are also claimed to work.

> [!warning] Unverified traps from the dump
> - Generics on records still erase at runtime like other generic classes (not expanded in the record dumps).
