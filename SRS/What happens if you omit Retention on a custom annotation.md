<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: if `@Retention` is missing, retention defaults to CLASS.

A custom annotation used like a Spring/JPA marker then compiles, is stored in the class file, and still returns null from `isAnnotationPresent` / `getAnnotation` at runtime.

Dumps tell you to set `@Retention(RetentionPolicy.RUNTIME)` when a runtime framework, test runner, or your own reflective reader must see the annotation.
> [!warning] Unverified traps from the dump
> - Popular lie: “annotations are always available at runtime.” Only RUNTIME retention is.
> - CLASS still occupies the class file; omitting Retention is not the same as SOURCE (zero bytecode cost).
