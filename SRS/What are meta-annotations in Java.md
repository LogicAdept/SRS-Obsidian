<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: meta-annotations are annotations that apply to other annotation types.

Named set: `@Retention` (how long it is stored), `@Target` (legal elements), `@Documented` (include in Javadoc; dumps say annotations are omitted from Javadoc by default), `@Inherited` (class-level lookup on subclasses), `@Repeatable` (Java 8, more than once on one element).

`@Target(ElementType.ANNOTATION_TYPE)` marks a type that is itself only legal on annotation declarations. Dumps also call any annotation whose target includes ANNOTATION_TYPE a meta-annotation.
> [!warning] Unverified traps from the dump
> - @Deprecated can mark an annotation type as outdated; that is not the same as the java.lang.annotation meta-annotation set.
> - @Documented does not change retention; it only affects Javadoc generation.
