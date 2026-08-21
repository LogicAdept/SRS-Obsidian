<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: `@Target({})` means the annotation type cannot be applied to any program element as a modifier. That is useful when the type exists only as a nested member type inside a more complex annotation.

Trying to write `@NoTargetAnnotation` on a class or method is then a compile-time error, even though the `@interface` itself is legal.
> [!warning] Unverified traps from the dump
> - Empty Target is not the same as omitting Target (omitting is “many declaration contexts”).
> - Member-type usage inside another annotation does not require the nested type to be a legal standalone target.
