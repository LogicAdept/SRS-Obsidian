<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate/Session #Java/Persistence/JPA #SRS

# What are the JPA flush modes and when does auto flush happen?

> [!abstract] Short answer
> **Flush** copies the dirty-checked state of the persistence context into SQL — it is **not commit**: no transaction boundary moves. `FlushModeType.AUTO` (the JPA default) flushes **before a query whose tables overlap pending changes** and before transaction completion; `FlushModeType.COMMIT` flushes **only** before commit, so a query executed mid-transaction does **not** see the session's own pending changes. Hibernate adds two legacy modes: `ALWAYS` (flush before every query, even non-overlapping) and `MANUAL` (only when you call `flush()` explicitly). The subtle senior part of `AUTO` is the **query-space check**: a pending insert into `persons` forces a flush before a query over `persons` — measured: the `INSERT` is visible in the SQL log between `persist` and the `SELECT` — but the same pending insert before a query over `orders` triggers **no flush at all**. That overlap rule is what gives read-your-writes semantics without flushing before literally every query.

## The measured timing of AUTO

The flush-before-query is conditional, and the condition is table overlap, not "any query". With one pending `persist(new Person(...))` in the session:

| Scenario (pending insert into `persons`) | Statements issued around the query | Result |
| --- | --- | --- |
| query over `persons` | `INSERT` then `SELECT` (delta 2) | query **sees** the pending row |
| query over `orders` | `SELECT` only (delta 1) | **no flush** — spaces do not overlap |
| then a query over `persons` | `INSERT` then `SELECT` (delta 2) | flush deferred until actually needed |
| same, mode `COMMIT` | `SELECT` only (delta 1) | query does **not** see the pending row |
| `COMMIT`, after `commit()` | `INSERT` (delta 1) | flush happened at commit, not before query |

Two senior conclusions fall out of that table. First, `AUTO` is not "flush before every query" — the overlap check makes it as lazy as correctness allows, which is why the default mode is usually the right one. Second, under `COMMIT` the query result is **not wrong from the database's point of view** — the row simply does not exist in the database yet, so the session silently violates read-your-writes for its own unflushed changes. Code that persists and then re-queries "to be sure" under a non-default flush mode produces intermittent, environment-dependent bugs that no database log explains.

```java
Session s = sf.openSession();                 // AUTO by default
s.beginTransaction();
s.persist(new Person("auto-pending"));        // pending, no SQL yet

// AUTO: INSERT is flushed BEFORE this query because it reads persons
List<Person> seen = s.createQuery(
        "select p from Person p", Person.class).getResultList();   // contains the row

s.setHibernateFlushMode(FlushMode.COMMIT);    // Hibernate-native switch
s.persist(new Person("commit-pending"));
List<Person> blind = s.createQuery(
        "select p from Person p", Person.class).getResultList();   // does NOT contain it
s.getTransaction().commit();                  // INSERT flushed here
```

**Listing 1.** Same session, two modes: `AUTO` flushes the pending insert before the overlapping query; `COMMIT` defers it to commit and the intermediate query runs without the row.

## Choosing a mode deliberately

The default `AUTO` costs one flush attempt (dirty check + possible SQL) before each overlapping query; a session with many managed entities and many interleaved queries pays that repeatedly, which is the same reason a large persistence context is expensive. `COMMIT` removes that overhead for read-mostly sessions that bulk-load and query without writing — a legitimate throughput knob. `MANUAL` exists for flows where flush timing is a business decision: batch pipelines that call `flush()`/`clear()` at chunk boundaries, or flows that must never leak partial state before an explicit signal. What you must never do is change the mode to make a test pass: under `MANUAL` a forgotten explicit flush before close silently drops the pending changes, and nothing in the logs shouts about it — the transaction simply commits without those SQL statements ever existing. The order in which flushed statements are grouped is fixed by the action queue and covered separately ([[How does Hibernate order SQL statements on flush]]); the visibility rules here are what decide **when** that queue is drained.

| Mode | Flush before overlapping query | Flush before non-overlapping query | Flush at commit | Read-your-writes |
| --- | --- | --- | --- | --- |
| `AUTO` (JPA default) | yes | no | yes | yes |
| `COMMIT` | no | no | yes | **no** for unflushed changes |
| `ALWAYS` (Hibernate) | yes | **yes** | yes | yes |
| `MANUAL` (Hibernate) | no | no | no — only explicit `flush()` | only after manual flush |

> [!warning] COMMIT mode breaks the "I re-read it, so it is saved" pattern
> Any code that relies on re-querying the same table to verify its own writes depends on `AUTO`'s flush-before-overlapping-query. Switching the session to `COMMIT` (or a bulk operation bypassing the context) does not fail loudly — the re-read simply returns the old state, and the row appears "lost" until commit.

> [!tip] Interview answer
> Flush pushes dirty-checked changes as SQL; it is not commit. AUTO — the default — flushes before commit and before any query whose query space overlaps the pending changes, which I verified: a pending person insert is flushed before a persons query, but not before an orders query, so read-your-writes holds exactly where it must. COMMIT flushes only at commit, so an intermediate query does not see the session's own pending row — measured. Hibernate's ALWAYS forces a flush before every query and MANUAL hands timing to explicit flush calls for batch/ETL flows. I keep AUTO unless profiling shows real flush overhead, and then COMMIT only for read-mostly sessions.

See [[How does Hibernate order SQL statements on flush]], [[What is Hibernate dirty checking]], [[What is Hibernate entity lifecycle states]], [[What is the difference between save and saveAndFlush in Spring Data JPA]], and [[What is the difference between save(), persist(), merge(), update()]].
