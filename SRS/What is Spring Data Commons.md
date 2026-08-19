<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Spring Data Commons is the shared module under the Spring Data umbrella. It provides core concepts and interfaces such as Repository that every store module reuses.

Sibling modules in the same dump list: Spring Data JPA, MongoDB, Redis, REST, Cassandra, Elasticsearch. Commons is the programming model; each store module keeps the traits of that database.
> [!warning] Unverified traps from the dump
> - CrudRepository and query derivation live here; JpaRepository does not.
> - Umbrella means several modules, not one JAR that talks to every database.
