<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

troubleshooting is harder than imperative apps; extra learning curve; limited reactive data-store support because classic relational stores have not fully embraced the reactive paradigm.

CPU-bound work; blocking dependencies with no reactive driver; team lacks reactive experience; need full JPA/Hibernate; simple CRUD; Boot 3.2+ virtual threads may cover the same concurrency with simpler code.

> [!warning] Unverified traps from the dump
> - Limited reactive DB support is the dump claim; R2DBC appears in another cue as the non-blocking SQL alternative.

