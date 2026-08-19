<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Instrumentation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Load-time weaving changes bytecode when the class loader defines a class. Dumps say that needs a special class loader or a Java agent attached at JVM start.

The usual dump command is `-javaagent:/path/to/aspectjweaver.jar` next to the application jar. Compilations name the trade-off: no special compiler in the build, but slower class loading, a JVM flag, and the agent must be present in every environment that should weave.

> [!warning] Unverified traps from the dump
> - `@EnableLoadTimeWeaving` without `-javaagent` is a dump failure mode: the annotation does not attach an agent by itself.
> - Dumps use `aspectjweaver.jar` as the agent. A different agent jar is a different claim — do not treat them as interchangeable from dump text alone.
