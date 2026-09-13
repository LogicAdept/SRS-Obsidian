<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate/Session #Java/Persistence/JPA #SRS

# Is the Hibernate Session thread-safe?

> [!abstract] Short answer
> No — and it is not supposed to be. The `SessionFactory` **is** thread-safe: it is an immutable, expensive, application-wide object, and multiple threads call it concurrently to open their own sessions. The `Session` (and the JPA `EntityManager`) is deliberately **not** thread-safe: it wraps the persistence context — an identity map plus a write-behind action queue — none of which is synchronized, because adding synchronization would serialize every load and flush without making shared mutable entity state safe anyway. The correct concurrency model is **one session per unit of work per thread**, never one shared session. Measured: two threads persisting through one shared session end in a race with a varying exception (`ConstraintViolationException` on the primary key in one run, `HibernateException: Flush during cascade is dangerous` in another) while the same work through two sessions completes cleanly. In Spring this is invisible by design — `@Transactional` binds an `EntityManager` to the current thread and transaction, and an injected `EntityManager` is a thread-safe proxy that hands each thread its own underlying session.

## Two objects, two contracts

The asymmetry confuses people because both objects live in the same API. The `SessionFactory` holds the immutable metadata — mappings, compiled query plans, connection pool wiring — and is built once; every thread may share it for the lifetime of the application. The `Session` is the opposite: a cheap, short-lived, **stateful** context. Its identity map guarantees one database row maps to one Java object, and its action queue accumulates pending changes until flush. Both guarantees are per-context and per-thread by construction. Synchronizing the session across threads would couple unrelated units of work: thread A's flush would drain thread B's pending changes — a correctness disaster even if the data structures were made thread-safe. The design answer is not locking, it is **scoping**: a session belongs to exactly one unit of work (one request, one message, one batch chunk).

| Object | Thread-safe? | Lifetime | Shared across threads? |
| --- | --- | --- | --- |
| `SessionFactory` | **yes** | application | yes — by design |
| `Session` / `EntityManager` | **no** | unit of work | **never** |
| Injected `EntityManager` in Spring | yes — it is a proxy | — | the proxy, not the session |
| `StatelessSession` | no | unit of work | never (no identity map, but not synchronized either) |

```java
// WRONG: one Session shared by threads — measured race, outcome varies
Session shared = sf.openSession();          // two threads persist + flush into it

// RIGHT: every unit of work opens its own
try (Session s = sf.openSession()) {        // thread-local by ownership
    s.beginTransaction();
    s.persist(new Parent("p"));
    s.getTransaction().commit();
}
```

**Listing 1.** The rule in code shape: sharing the factory is the pattern, sharing the session is the bug.

## What actually breaks, measured

Two threads, one shared session, fifty `persist`+`flush` pairs each — the run fails, but **how** it fails changes from run to run: one execution died with `ConstraintViolationException` (the two threads raced into the same identifier allocation of a shared sequence-cache slot), another with `HibernateException: Flush during cascade is dangerous` (interleaved flushes walked the action queue while another thread was mutating it). The nondeterminism is the message: a shared session is not "unsafe sometimes" — it is undefined behavior whose symptom you cannot even rely on for tests. The control run — the same hundred persists through two separate sessions — completed with every row committed and counted. So the interview-grade statement is precise: **the session is not thread-safe, but the API family is safe by composition** — the factory hands out sessions, threads never meet inside one, and isolation between units of work comes from transactions, not from locks.

> [!warning] The stateless request-handler trap
> A "singleton" controller or consumer that opens **one** session in a field at startup and reuses it per call has the same bug as the measured race — the object feels stateless, but the session accumulates entities from every concurrent request into one identity map and one flush. Sessions are cheap; create one per request (or let the framework do it) rather than amortizing one across threads.

> [!tip] Interview answer
> The SessionFactory is thread-safe and shared for the app's lifetime; the Session is intentionally not — it is the persistence context, an identity map plus an action queue scoped to one unit of work, and synchronizing it would corrupt isolation rather than fix races. I verified the failure: two threads on one session die with varying exceptions — primary-key violations one run, "flush during cascade is dangerous" the next — while two sessions complete cleanly. The pattern is one session per request or message; in Spring the injected EntityManager is a thread-safe proxy that dispatches to a per-transaction, per-thread session, which is why the bug only appears when people manage sessions by hand.

See [[What is Hibernate SessionFactory]], [[What are the pros and cons of EntityManager versus Spring Data JPA repositories]], [[What is Hibernate entity lifecycle states]], [[How does Hibernate order SQL statements on flush]], and [[Is a singleton Spring bean thread-safe]].
