<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Compilations disagree.

Coderboi / Medium: **yes**. An enum may declare an abstract method that each constant implements (constant-specific class bodies).

```java
enum MathOp implements Op {
  ADD { public int apply(int a, int b) { return a + b; } },
  MUL { public int apply(int a, int b) { return a * b; } };
}
```

Basicsstrong: **no**, because enums are final.

Separately: you cannot declare the enum type itself `abstract`.

> [!warning] Unverified traps from the dump
> - Treat “no abstract methods because final” vs constant-specific abstract methods as a dump contradiction to verify.
