<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate/IdGeneration #Java/Persistence/JPA #SRS

# Why does GenerationType.IDENTITY disable JDBC batching?

> [!abstract] Short answer
> With **`IDENTITY`** the database assigns the key **inside the `INSERT` statement**, and the entity needs that key back immediately. So Hibernate must **run each insert right away** (on `persist`, not at flush) and **read the generated key** before it can continue — there is no queue of pending inserts to group, and **`hibernate.jdbc.batch_size` is ignored for entity inserts**. Batching needs *pending actions with known-in-advance SQL*; `IDENTITY` produces *immediate, key-dependent* inserts. The fix is **`SEQUENCE`** (id allocated **before** the insert from a database sequence, so inserts stay write-behind and batchable), ideally with the **pooled optimizer** so one sequence round trip covers a whole range of ids. **`TABLE`** is portable but serializes allocators on a lock row — the worst choice at load.

## The mechanism: when the id is known, the insert can wait

JDBC batching means handing the driver **several statements** for one round trip (`addBatch`/`executeBatch`). For that, Hibernate must have several inserts **queued at flush time**. Queuing is only possible when the **id is generated outside the row**:

| Strategy | Where the id comes from | Insert timing | Batchable inserts |
| --- | --- | --- | --- |
| **`IDENTITY`** | auto-increment column, returned by the insert | **immediately on `persist`** | **no** |
| **`SEQUENCE`** | `next value for seq` before the insert | flush, write-behind | **yes** |
| **`TABLE`** | a lock row in an id table, updated before the insert | flush, write-behind | yes, but allocator is a bottleneck |
| **`AUTO`** | dialect picks (sequence if available, else identity) | — | only when a sequence exists |

With **`SEQUENCE`**, `persist` only does one cheap sequence call (or none, see optimizers below); the insert itself joins the **`ActionQueue`** and is emitted at flush together with its siblings. **JDBC batch_size** then groups them. Updates and deletes batch regardless of id strategy — the restriction is on **inserts of `IDENTITY` entities**.

```java
@SequenceGenerator(name = "order_seq", sequenceName = "order_seq",
                   allocationSize = 50)          // pooled range
@Entity
class Order {
    @Id @GeneratedValue(strategy = GenerationType.SEQUENCE,
                        generator = "order_seq")
    Long id;
}
```

**Listing 1.** Sequence with a 50-wide allocation: ids are handed out in memory, one sequence round trip per 50 inserts.

## The optimizers: make the sequence cheap too

A naive sequence mapping costs **one extra round trip per insert** (`select nextval` before every insert). Id generators solve this with **in-memory allocation**:

- **`hi/lo`** — fetch one high value, derive `lo` ids in memory. Safe, but the visible ids have gaps and the algorithm is fiddly to retrofit.
- **`pooled`** (Hibernate default for nonzero `allocationSize`) — the sequence's `nextval` *is* the start of the range; the next `allocationSize − 1` ids come from memory. No extra table, no lock row, gaps on restart — acceptable for a surrogate key.

`allocationSize` **must match the database sequence `INCREMENT BY`**, otherwise two application instances hand out overlapping ranges. Sequences are non-transactional by design: a rolled-back transaction burns ids — that is the price of not serializing inserts.

## Consequences beyond batching

With `IDENTITY`, because the insert already ran, **`persist` hits the database** — flush-time reordering ([[How does Hibernate order SQL statements on flush]]) cannot help it, a rollback still consumed the id, and the action is *already* in the database even if the surrounding transaction later rolls back (fine for atomicity, but it changes error timing). Batch inserts, `StatelessSession` bulk loads, and import scripts all degrade to row-at-a-time. On dialects without sequences (MySQL, MariaDB) there is **no sequence option** — the realistic choices are `IDENTITY` + slower bulk load, or an application-side generator (UUID, snowflake-style) that bypasses the database entirely and batches freely.

> [!warning] "I set batch_size but inserts are still one-by-one"
> Check the id strategy first. `IDENTITY` silently disables insert batching while `UPDATE`/`DELETE` still batch — the config "works" but the hottest path gains nothing. Second suspect: `allocationSize` ≠ sequence increment, which shows up as duplicate-key errors under concurrency, not as slow inserts.

> [!tip] Interview answer
> `IDENTITY` hands the id back from the insert row itself, so Hibernate cannot queue inserts — `persist` must execute them one at a time and `jdbc.batch_size` does nothing for them. With `SEQUENCE` the id exists before the insert, inserts stay on the `ActionQueue` until flush and batch fine; the pooled optimizer makes the sequence cost one round trip per allocation range instead of per row. I pick sequences wherever the dialect has them, keep `allocationSize` equal to the sequence increment, and reserve UUIDs for services that need keys before any database round trip.

See [[What is the JPA Id annotation]], [[What is Hibernate performance tuning]], [[What is Hibernate entity lifecycle states]], and [[How does Hibernate order SQL statements on flush]].
