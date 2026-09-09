<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.

Draft: build with ./mvnw package -Dnative (optionally -Dquarkus.native.container-build=true using a builder image). Result: a native executable containing the app, libraries, a reduced VM (SubstrateVM), plus a small VM base for fast startup and minimal disk footprint.
Why Quarkus fits closed-world compilation: DI resolved at build time, no runtime classpath scanning, extensions register reflection/resource/proxy metadata programmatically instead of user-maintained JSON.
Distributions: Oracle GraalVM CE/EE or Mandrel (downstream of GraalVM CE built from OpenJDK sources, recommended for Linux containers; macOS/Windows limited).
Trade-offs: native build is slow and memory hungry; peak throughput is below JIT for long-running hot loops; some JVM features restricted (reflection by default, dynamic proxies, finalization).
JVM mode vs native: native wins startup/RSS; JVM mode wins peak throughput; both start fast in Quarkus.

> [!warning] Unverified traps from the draft
> - Facts above are plausible but unchecked; version numbers and exact API names must be confirmed against official docs before this card is used as a review answer.
> - Comparison cards must keep both sides tagged and avoid absolute always/never claims.
