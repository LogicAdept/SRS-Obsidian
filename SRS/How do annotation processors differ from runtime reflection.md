<!--
reps: 0
priority: 0
-->
#Java/Annotations #Java/Language/Reflection #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps split readers:

- Annotation processor (`javax.annotation.processing.Processor` / `AbstractProcessor`): runs during compilation. Can see SOURCE retention, generate sources via `Filer`, fail the build. Register in `META-INF/services/javax.annotation.processing.Processor`.
- Reflection (`Class` / `AnnotatedElement`): runs after load. Needs RUNTIME retention. `isAnnotationPresent` then `getAnnotation`.
- CLASS retention: dumps point at bytecode libraries (ASM, Byte Buddy), not `getAnnotation`.

Dumps: annotations do nothing until some processor, compiler, or framework acts on them.
> [!warning] Unverified traps from the dump
> - A runtime reader cannot recover SOURCE annotations from the class file.
> - CLASS is visible to bytecode tools and still invisible to Class.getAnnotation.
