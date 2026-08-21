<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `@Target` takes `ElementType` constants (TYPE, FIELD, METHOD, PARAMETER, CONSTRUCTOR, LOCAL_VARIABLE, ANNOTATION_TYPE, PACKAGE, and later TYPE_PARAMETER, TYPE_USE, MODULE, RECORD_COMPONENT). Using the annotation outside those contexts is a compile-time error.

Multiple constants are allowed: `@Target({ElementType.FIELD, ElementType.METHOD})`.

If `@Target` is omitted, dumps say the annotation may be used on declarations (not type-parameter declarations in older wording).

`@Target({})` makes the type unusable as a standalone annotation so it can exist only as a member type inside another annotation.
> [!warning] Unverified traps from the dump
> - A dump wrote ElementType.USE for type annotations; the enum constant is TYPE_USE.
> - Duplicate constants in one @Target array are a compile-time error.
