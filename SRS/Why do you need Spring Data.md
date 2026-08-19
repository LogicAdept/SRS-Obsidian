<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

JPA repositories duplicate the same EntityManager find/merge boilerplate per entity. Data stores also exploded in variety (including big-data stores).

Spring Data supplies common abstractions to store and retrieve data, independent of the store type, and cuts that boilerplate by generating repository implementations.
> [!warning] Unverified traps from the dump
> - The abstraction is shared; each module still keeps store-specific traits.
> - You still write custom code when derivation and @Query are not enough.
