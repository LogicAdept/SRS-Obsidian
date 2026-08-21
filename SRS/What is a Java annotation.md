<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: annotations are metadata attached to program elements. They are a Java type, declared with `@interface`, similar in shape to an interface. They are not part of the program’s algorithm and have no direct effect on the annotated code.

Uses in dumps: compiler information (errors/warnings), compile-time / deployment-time processors (generate code or descriptors), runtime processing via reflection.

Introduced in Java 5. Java 8 added repeating annotations and type annotations.
> [!warning] Unverified traps from the dump
> - Annotation types are a form of interface and implicitly extend Annotation; you still cannot write extends on @interface.
> - Java 5 vs “always been in the language”: dumps date them to Java 5.
