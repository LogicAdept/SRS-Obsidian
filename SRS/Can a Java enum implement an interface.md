<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Yes. An enum is a type, like a class, so it can `implements` interfaces. Compilations use this for per-constant behaviour instead of a `switch` on the enum.

```java
interface Op { int apply(int a, int b); }
enum MathOp implements Op {
  ADD { public int apply(int a, int b) { return a + b; } },
  MUL { public int apply(int a, int b) { return a * b; } };
}
MathOp.ADD.apply(2, 3);  // 5
```

Dumps also say `java.lang.Enum` already implements `Serializable` and `Comparable`.

> [!warning] Unverified traps from the dump
> - Implementing an interface does not lift the “cannot extend a class” rule.
