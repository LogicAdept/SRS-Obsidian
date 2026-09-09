<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.

Draft: after compilation, an augmentation phase runs. Extensions declare build steps (@BuildStep in a deployment artifact); steps consume and produce build items and are wired into a dependency graph.
Work performed at build time: bean discovery via Jandex indexes, CDI container layout, proxy generation, configuration mapping validation, native-image metadata registration, service descriptor merging, bytecode recording via Gizmo.
The output is recorded calls that the runtime bootstrap replays; heavy classes used only during the build do not ship in the runtime artifact.
Result: the JVM/native runtime starts from recorded state instead of discovering it.

> [!warning] Unverified traps from the draft
> - Facts above are plausible but unchecked; version numbers and exact API names must be confirmed against official docs before this card is used as a review answer.
> - Comparison cards must keep both sides tagged and avoid absolute always/never claims.
