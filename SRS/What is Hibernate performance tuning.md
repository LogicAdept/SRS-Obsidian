<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate #SRS

# What is Hibernate performance tuning?

> [!abstract] Short answer
> **Hibernate performance tuning** is not one property. It is **fewer SQL round-trips**, a **small persistence context**, and **JDBC statement batching**, checked with **`Statistics`**. Fetching too little is [[What is the N plus one problem in Hibernate]]; fetching too much is cartesian joins and unused columns. Writes: **`hibernate.jdbc.batch_size`** (default **0** = off), **`flush`/`clear`** on bulk persist, **`@DynamicUpdate`** when you want fewer `UPDATE` columns. Optional: **L2 / query cache**. **`StatelessSession`** and bulk HQL `UPDATE`/`DELETE` skip the first-level cache when you do not need it.

## Measure, then cut round-trips

Turn on **`hibernate.generate_statistics`** (or `Statistics.setStatisticsEnabled(true)`). `SessionFactory.getStatistics()` counts **entity load vs fetch**, **collection fetch**, **query execution time**, **prepare/close statement**, **L2 / query-cache hits**, **flushes**, **sessions**. `entityFetchCount` climbing with a loop over associations is N+1. Tuning without this is guesswork.

The Fetching chapter treats **how you load associations** as the largest lever: extra selects (N+1) versus extra rows/columns. Prefer **one query that returns what you will use** — `JOIN FETCH`, an entity graph, or a **DTO projection**. **`@BatchSize`** (or `hibernate.default_batch_fetch_size`) loads several uninitialized proxies with an **`IN` list** instead of one select per proxy. That is **better than N+1**, still **worse than a single `JOIN FETCH` or DTO** when the graph is known. Global batch fetch is **off** unless you set the default or annotate; **`hibernate.max_fetch_depth`** caps nested outer-join fetch (default **0** = none). **`hibernate.use_subselect_fetch`** (6.3+) can load collections with a subselect of the owner query; otherwise only `@Fetch(SUBSELECT)`.

```d2
direction: down
sql: "SQL round-trips\nN+1 vs JOIN FETCH / DTO / @BatchSize" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
pc: "Persistence context size\nflush + clear / scroll / StatelessSession" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
jdbc: "JDBC batching\nbatch_size, order_inserts" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
sql -> pc -> jdbc
```

**Fig. 1.** Three official axes: fetch shape, L1 size, JDBC batches. Measure with `Statistics`.

## Batch writes and a bounded Session

JDBC can send many `PreparedStatement`s as **one driver batch**. **`hibernate.jdbc.batch_size`** (`BatchSettings.STATEMENT_BATCH_SIZE`) is the max statements per batch. **Default 0 — disabled.** The 5.2 Batching chapter suggests an integer **between 10 and 50**. Override per session: `session.setJdbcBatchSize(n)`. **`hibernate.order_inserts` / `hibernate.order_updates`** (default **false**) sort by entity type and id so more statements share a batch; **benchmark** — the sort itself costs. **`IDENTITY` generators disable JDBC insert batching.** This setting **does not apply to `StatelessSession`**; do not “fix” that with `setJdbcBatchSize` on a stateless session (it becomes write-behind and fights the model). Prefer `insertMultiple` / `updateMultiple` there.

A stateful `Session` **holds hard references** to every managed entity. Persist 100 000 rows in one context and you keep 100 000 instances until commit — **OOM** and a **pool-held** connection. Pattern: persist a chunk, **`flush()` then `clear()`**, repeat. For huge reads, **`scroll()`** (server-side cursor) plus periodic flush/clear, **`CacheMode.IGNORE`** if L2 would only pollute. Dirty checking **walks every managed instance** at flush — another reason to keep L1 small.

**Bulk HQL/JPQL `UPDATE`/`DELETE`** (`Query.executeUpdate`) rewrites rows **without** loading entities. Joins in the bulk `FROM` are **illegal**; default HQL `UPDATE` **does not bump** `@Version` unless you use **`update versioned`**.

**L2 cache** is a **separate** product: optional, shared, destructured state. It does not shrink a fat Session and it **does not** replace fetch design. See [[What are Hibernate first and second level cache tiers]].

```java
int batchSize = 25; // align with hibernate.jdbc.batch_size
for (int i = 0; i < count; i++) {
    session.persist(new Person("p-" + i));
    if (i > 0 && i % batchSize == 0) {
        session.flush();
        session.clear();
    }
}
```

**Listing 1.** Conceptual: JDBC batching plus `flush`/`clear` so L1 does not grow with the whole job.

> [!warning] IDENTITY and a fat Session silently undo “batching”
> `hibernate.jdbc.batch_size` does **nothing** until it is **> 0**, and **IDENTITY ids still emit one insert round-trip**. `@BatchSize` is **not** a substitute for `JOIN FETCH` when you know the graph. `StatelessSession` has **no** L1, **no** dirty checking, **no** cascade — fast for bulk rows, wrong for a domain graph. Statistics are **off** until you enable them; without `entityFetchCount` you will not see N+1.

> [!tip] Interview answer
> I treat Hibernate tuning as fetch shape, persistence-context size, and JDBC batching, measured with generate_statistics. I kill N+1 with JOIN FETCH, an entity graph, or a DTO, and use @BatchSize only as a lazy-loop mitigation. For writes I set jdbc.batch_size, avoid IDENTITY if I need insert batches, and flush and clear so the Session does not pin every row. Bulk HQL or StatelessSession is for jobs that should not be entities in L1 at all.

See [[What is the N plus one problem in Hibernate]], [[What is lazy fetch in JPA or Hibernate]], [[What is JOIN FETCH and EntityGraph in Spring Data JPA]], [[What are Hibernate first and second level cache tiers]], [[What is Hibernate second level cache and its main components]], [[What is Hibernate dirty checking]], and [[How does the Hibernate first-level cache work in Spring]].
