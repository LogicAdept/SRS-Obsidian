<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Java/Spring/Data/JPA #SRS

# What is TestEntityManager?

> [!abstract] Short answer
> **`TestEntityManager`** (`org.springframework.boot.jpa.test.autoconfigure`) is Boot’s **test-only alternative to `EntityManager`**: a **subset** of persist/find/flush/merge/remove plus helpers **`persistAndFlush`**, **`persistFlushFind`**, **`persistAndGetId`**. **`@DataJpaTest` auto-configures** a bean of this type so you **set up rows without calling the repository under test**. It **does not extend `EntityManager`**. Full JPA: **`getEntityManager()`**. Outside the slice: **`@AutoConfigureTestEntityManager`** and the test **must be `@Transactional`**.

## Persist for setup, query through the repo

Official sample: **`entityManager.persist(new User(…))`** then **`repository.findByUsername(…)`**. **`persist`** delegates to **`EntityManager.persist`** and returns the **same instance** (now managed). **`flush()`** syncs SQL. **`persistAndFlush`** is persist then flush. **`persistFlushFind`** then **`find` by generated id** — useful when you need to prove the row **round-tripped**. **`clear()` / `detach()` / `refresh()`** match JPA.

The slice already wraps each method in a **transaction that rolls back**. That is why setup persists do not leak. Slice: [[What is the DataJpaTest annotation]]. How-to: [[How do you test JPA repositories in Spring]]. Rollback: [[What is Transactional used for in tests]]. SQL seed: [[How do you handle test data in Spring integration tests]]. Family: [[What are Spring Boot test slices]].

```java
@DataJpaTest
class MyRepositoryTests {

    @Autowired TestEntityManager entityManager;
    @Autowired UserRepository repository;

    @Test
    void testExample() {
        this.entityManager.persist(new User("sboot", "1234"));
        User user = this.repository.findByUsername("sboot");
        assertThat(user.getUsername()).isEqualTo("sboot");
    }
}
```

**Listing 1.** Conceptual Boot **4.1**. Setup via **`TestEntityManager`**, assert via the **repository**.

```java
MyEntity written = this.testEntityManager.persistAndFlush(new MyEntity("Spring"));
MyEntity reread = this.testEntityManager.persistFlushFind(new MyEntity("Spring"));
```

**Listing 2.** Conceptual JavaDoc helpers. **`persistFlushFind`** is persist + flush + **`find` by id**.

```d2
direction: down
tem: "TestEntityManager\npersist / persistAndFlush" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
pc: "persistence context\n(+ flush to DB)" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
repo: "UserRepository.findBy…" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}

tem -> pc -> repo
```

**Fig. 1.** Do not `save()` on the same repository you are proving, if the point is that **`findBy…`** hits stored state.

> [!warning] Not a production `EntityManager`
> No `createQuery`, no `createNativeQuery`, no lifecycle you would inject into a `@Service`. Use **`getEntityManager()`** only in the test when the subset is not enough. Never ship this type in application code.

> [!warning] Unflushed `persist` vs JPQL
> A query can miss the row until **`flush`**. Prefer **`persistAndFlush`** when the next call is a query that does not auto-flush the way you think.

> [!warning] `@AutoConfigureTestEntityManager` needs a transaction
> On **`@SpringBootTest`** (or any non-slice class) add **`@Transactional`**. Without it the helper has **no persistence context**.

> [!tip] Interview answer
> **`TestEntityManager` is Boot’s test `EntityManager` subset — persist/flush/find helpers auto-configured by `@DataJpaTest`.** Seed with it, query with the repository. It is not a production bean.
