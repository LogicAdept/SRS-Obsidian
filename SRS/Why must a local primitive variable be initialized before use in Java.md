<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Instance and static fields are automatically initialized to a zero value: `0` for numeric primitives, `false` for `boolean`, `\u0000` for `char`, and `null` for any reference type.

The crucial exception: local variables get no default. The compiler requires you to assign one before use, or it is a compile error ("variable might not have been initialized").

```java
public void show() {
    int localVariable = 100; // must assign before read
}
```

> [!warning] Unverified traps from the dump
> - Field defaults apply to instance/static fields, not to locals.
> - Reading an uninitialized local `int` does not yield `0`; it does not compile.
