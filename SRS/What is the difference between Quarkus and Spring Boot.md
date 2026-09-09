<!--
reps: 0
priority: 0
-->
#Java/Quarkus #Java/Spring/Boot #SRS #New

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.

Draft contrast: Spring Boot = auto-configuration at runtime startup (classpath scanning, conditions, reflection-heavy); Quarkus = build-time processing ("compile time boot") — most wiring is done during the build, boot then just runs recorded bytecode.
Startup: Quarkus JVM mode starts in fractions of a second; native mode in milliseconds. Boot apps start in seconds (improved with AOT in Boot 3, but still slower).
Memory: Quarkus targets low RSS, native executables much smaller than a JVM footprint.
Ecosystem: Boot has the largest ecosystem and hiring pool; Quarkus covers standards (Jakarta REST, CDI, JPA) plus MicroProfile, Spring API compatibility layer exists but is partial.
Dev experience: Quarkus dev mode live reload + Dev Services vs Boot DevTools.
Native: Quarkus treats GraalVM native as a first-class build target; Boot 3 AOT helps but is not the same closed-world story.

> [!warning] Unverified traps from the draft
> - Facts above are plausible but unchecked; version numbers and exact API names must be confirmed against official docs before this card is used as a review answer.
> - Comparison cards must keep both sides tagged and avoid absolute always/never claims.
