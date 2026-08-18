<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

If a primitive type or a string is defined as a constant and the value is known at compile time, the compiler replaces the constant name everywhere in the code with its value. This is called a compile-time constant.

A compile-time constant must be:

- Declared `final`
- Primitive or `String`
- Initialized within the declaration
- Initialized with a constant expression

They are replaced with actual values at compile time because the compiler knows their value up front and that it cannot change at run time.

```java
private final int x = 10;
```

> [!warning] Unverified traps from the dump
> - Compile-time constants are a subset of `final` variables: primitive or `String`, initialized with a constant expression in the declaration.
