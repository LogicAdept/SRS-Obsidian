<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: no. Annotation types implicitly extend `java.lang.annotation.Annotation`. An `extends` clause on `@interface` is a compile-time error.

```java
public @interface AnAnnotation extends OtherAnnotation {} // does not compile
```

You compose annotations by nesting annotation-typed members or by meta-annotating, not by subclassing.
> [!warning] Unverified traps from the dump
> - Dumps that call Object the parent class of Annotation mix up the Annotation interface with java.lang.Object.
> - A member whose type is another annotation is nesting, not inheritance.
