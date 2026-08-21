<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump compile puzzle:

```java
@Target({ ElementType.FIELD, ElementType.TYPE, ElementType.FIELD })
public @interface TestAnnotation {
    int[] value() default {};
}
```

Does not compile: it is a compile-time error if the same enum constant appears more than once in `@Target`. Removing the duplicate `FIELD` makes it legal.
> [!warning] Unverified traps from the dump
> - The error is duplicate Target constants, not the empty-array default on value().
