<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.

Quarkus is a full-stack Java framework positioned as "Supersonic Subatomic Java", built to run Java on Kubernetes and GraalVM.
A draft description: a Kubernetes-native Java stack that optimizes at build time — it precomputes framework metadata, wires the CDI container ahead of time, and supports compiling to a native executable for fast startup and low RSS memory.
Built on standards: Jakarta REST, CDI, JPA/Hibernate, MicroProfile/SmallRye, Eclipse Vert.x underneath.
Marketing triad: fast boot, low memory, developer joy (live reload, Dev Services, one command scaffolding via code.quarkus.io).
License Apache 2.0; artifacts in Maven Central; current generation is Quarkus 3.x (Jakarta namespace).

> [!warning] Unverified traps from the draft
> - Facts above are plausible but unchecked; version numbers and exact API names must be confirmed against official docs before this card is used as a review answer.
> - Comparison cards must keep both sides tagged and avoid absolute always/never claims.
