<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Persistence/JPA #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump comparison:

EntityManager: full control over queries and transactions; easier to write complex custom queries; direct control over transaction boundaries. Cost: more CRUD boilerplate, steeper learning curve, and you optimize by hand.

Spring Data JPA repositories: simplified CRUD, less boilerplate, derived query methods, built-in transaction management, easier for beginners, automatic optimizations. Cost: less flexibility for complex queries and less control when you need to tune performance.
> [!warning] Unverified traps from the dump
> - Dumps still send you to EntityManager or a custom repository fragment when derived queries run out.
> - Repository methods are described as transactional by default in other dumps; service-layer @Transactional is still the usual business boundary.
