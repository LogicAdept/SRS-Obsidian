<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Embedded #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump three steps: packaging `war`, extend `SpringBootServletInitializer` (override `configure`), mark the embedded server `provided` so it is not bundled.

Modern default in the same dumps: executable jar; WAR is for legacy or platform-mandated containers.

> [!warning] Unverified traps from the dump
> - Forgetting `SpringBootServletInitializer` is the dump's 'WAR starts but context never boots' case.
