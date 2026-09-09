<!--
reps: 0
priority: 0
-->
#Java/Quarkus #Java/Spring/Boot #SRS #New

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.

Draft mechanism: Quarkus moves framework work from runtime startup to build time. During the build it scans classes, resolves CDI beans, builds configuration models, generates bytecode, and records bootstrap steps; at boot it executes a mostly precomputed program graph.
Spring Boot does the analogous discovery work on every startup: classpath scanning, @Conditional evaluation, bean definition building, reflection and proxy generation at boot.
Fewer runtime layers: no runtime classpath scanning, no runtime XML/annotation parsing, fewer classes loaded, lazy-by-default bean instantiation.
Consequence quoted by the project: sub-second JVM boot, ~tens of milliseconds native boot.
Trap: this is not free — the cost is paid in build time and in build-time-only configuration.

> [!warning] Unverified traps from the draft
> - Facts above are plausible but unchecked; version numbers and exact API names must be confirmed against official docs before this card is used as a review answer.
> - Comparison cards must keep both sides tagged and avoid absolute always/never claims.
