<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@DataJpaTest` is a Boot slice for JPA: scans `@Entity`, configures Spring Data repositories, usually an **in-memory** DB. Does not load web/service layers.

Dumps: `@Autowired TestEntityManager` + repository; tests are `@Transactional` and roll back. Prefer this over `@SpringBootTest` for repository tests.

> [!warning] Unverified traps from the dump
> - Replacing the embedded DB with Testcontainers is a common follow-up; the slice still will not load MVC.
