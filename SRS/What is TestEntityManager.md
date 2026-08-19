<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`TestEntityManager` is injected in `@DataJpaTest` to persist/flush entities for setup without going through the repository under test.

Dump: “simplifies interaction with JPA for test setups.” Example: `entityManager.persist(user)` then `userRepository.findByUsername(...)`.

> [!warning] Unverified traps from the dump
> - It is not a full EntityManager replacement for production code.
