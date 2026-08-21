<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `@Retention` picks a `RetentionPolicy` that controls how long an annotation instance is kept.

- SOURCE: discarded by the compiler; not written to the class file. Dumps cite `@Override` and `@SuppressWarnings`.
- CLASS: recorded in the `.class` file but not retained by the VM, so `getAnnotation` cannot see it. Dumps say this is the default when `@Retention` is omitted. Used by bytecode tools.
- RUNTIME: recorded in the class file and kept by the VM so reflection (`AnnotatedElement.getAnnotation`) can read it. Dumps cite `@Deprecated` and framework metadata.

Retrieving an annotation uses reflection or an annotation processor. Processors can see SOURCE; bytecode parsers can see CLASS; runtime frameworks need RUNTIME.
> [!warning] Unverified traps from the dump
> - Dumps often imply the default is RUNTIME because Spring needs it — dumps also say the language default is CLASS.
> - SOURCE vs CLASS: SOURCE never appears in bytecode; CLASS does, but still not via reflection.
