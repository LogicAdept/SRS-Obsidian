<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps (Reflection): obtain a `Class`, then methods/fields. `isAnnotationPresent(MyAnnotation.class)` then `getAnnotation(MyAnnotation.class)` and read elements. Repeat for `getDeclaredMethods()` / `getDeclaredFields()`.

```java
if (method.isAnnotationPresent(MyAnnotation.class)) {
    MyAnnotation a = method.getAnnotation(MyAnnotation.class);
    // a.value()
}
```

Retention must be RUNTIME or these calls see nothing. Repeating types: dumps mention `getAnnotationsByType` so the compiler-generated container is unwrapped.
> [!warning] Unverified traps from the dump
> - getAnnotation on a class follows @Inherited; getDeclaredAnnotations does not look at the superclass.
> - Looking at getDeclaredMethods() misses inherited methods; that is a reflection lookup issue, not retention.
