<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps (Oracle-style FAQ): annotations are metadata bound to source elements and have no direct effect on the operation of the code they annotate.

They matter only because a compiler check, annotation processor, bytecode tool, or runtime framework reads them. Typical dump buckets: compiler information (`@Override`), compile/deploy-time generation, runtime processing via reflection.

A custom `@LogExecutionTime` does not time a method until an aspect, processor, or reflective wrapper consumes it.
> [!warning] Unverified traps from the dump
> - Popular lie: putting an annotation on a method changes JVM semantics by itself.
> - Frameworks that “make annotations work” still use processors, proxies, or reflection — the language does not execute the annotation.
