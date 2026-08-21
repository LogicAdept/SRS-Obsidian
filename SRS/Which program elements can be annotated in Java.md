<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: declarations of classes, constructors, fields, methods, parameters, local variables (including for-loop and try-with-resources variables), other annotation types, and packages (`package-info.java`).

Java 8 type-use: with `@Target(ElementType.TYPE_USE)` dumps place annotations on `new`, casts, `implements` type arguments, and `throws` types.

```java
new @SimpleAnnotation Apply();
aString = (@SimpleAnnotation String) something;
void m() throws @SimpleAnnotation Exception {}
```
> [!warning] Unverified traps from the dump
> - TYPE (class/interface/enum/annotation declaration) is not TYPE_USE (any use of a type in code).
> - Package annotations live on package-info.java, not on a random class in the package.
