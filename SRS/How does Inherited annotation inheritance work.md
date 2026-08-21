<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: annotations are not inherited by default. `@Inherited` on an annotation type makes a class-level annotation visible on subclasses when you query the subclass and it does not declare that annotation. The lookup walks superclasses until a match or `Object`.

If the subclass declares the same annotation type, dumps say that declaration replaces the inherited one (no merge).

Interfaces: dumps say implementing a class does not inherit annotations from an annotated interface; you must read interface annotations yourself via reflection.
> [!warning] Unverified traps from the dump
> - @Inherited applies only to class (TYPE) annotations, not methods, fields, or parameters.
> - It does not follow interface implementation, even if the annotation type is @Inherited.
