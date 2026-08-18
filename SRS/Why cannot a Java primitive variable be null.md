<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`null` is a special literal meaning a reference points to no object. Only reference types can be `null` — primitives cannot. Using a `null` reference (calling a method, accessing a field, unboxing) throws `NullPointerException`.

```java
Integer boxed = null;
int x = boxed;       // NPE — unboxing null
```

Dumps also show `int primitiveAge = null;` as a compilation error.

> [!warning] Unverified traps from the dump
> - Primitives cannot hold `null`; wrappers can.
> - Unboxing a `null` wrapper throws `NullPointerException`.
