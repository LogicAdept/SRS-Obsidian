<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: an annotation method may return a primitive, `String`, `Class` (including bounded `Class<? extends …>`), an enum type, an annotation type, or a one-dimensional array of those. No `throws`. No parameters. Optional `default` if the value is a constant expression.

```java
enum Complexity { LOW, HIGH }
public @interface ComplexAnnotation {
    Class<?> value();
    int[] types();
    Complexity complexity();
}
```

`Object complexity();` does not compile.
> [!warning] Unverified traps from the dump
> - No boxed wrappers as the declared return type (use primitive int, not Integer) in dump examples.
> - Nested annotations are allowed as member types; arbitrary classes other than Class are not.
