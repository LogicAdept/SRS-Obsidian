<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump path: `@DataJpaTest` + in-memory (or test) database + `TestEntityManager` / repository `@Autowired`. Do not load MVC.

DEBAGanov lists “how to test JPA repositories” as a standard Spring testing question; Boot dumps answer with `@DataJpaTest`.

> [!warning] Unverified traps from the dump
> - @SpringBootTest + real DB is slower and not the slice interview answer.
