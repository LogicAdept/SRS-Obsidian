<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #Java/Collections #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: Java primitive types are not reference types (`int` is not an `Object`). Generics use type-erasure of reference types, so a `List` is a list of references at run time. Therefore generic collections cannot store primitives directly.

Wrapper classes make primitives usable as objects. Adding an `int` to `List<Integer>` is compiled as `add(Integer.valueOf(i))` (autoboxing).

```java
List<Integer> list = new ArrayList<>();
list.add(i); // compiler treats this as add(Integer.valueOf(i))
```

Invalid illustration from a dump: `vector.addElement(3)` vs valid `vector.addElement("3")`.

> [!warning] Unverified traps from the dump
> - You write `List<Integer>`, never `List<int>`.
> - Autoboxing hides the wrapper allocation when you `add` an `int`.
