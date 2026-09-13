<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate/Fetching #Java/Persistence/JPA/Fetching #SRS

# What are the Hibernate fetching strategies?

> [!abstract] Short answer
> Fetching strategy = **the SQL shape** used to load an association. Four shapes exist: **SELECT** (the default — one query per association access; fine alone, an N+1 generator in loops), **JOIN** (fetch in the same query as the parent — one query, one result set; impossible on `List` collections without breaking pagination), **BATCH** (`default_batch_fetch_size` / `@BatchSize` — lazy SELECTs are grouped into `IN (…) : size` queries; measured: touching the lazy collections of **25 parents issued 3 SELECTs instead of 25**), and **SUBSELECT** (one query reusing the query that loaded the parents — best when you iterate collections of every parent from one selection). The senior framing: these are **two orthogonal knobs** — *when* (lazy/eager) and *how* (SQL shape) — and the modern workflow is: keep associations lazy, then pick the shape per use case with query-level tools (`JOIN FETCH`/`@EntityGraph`) and batch size as the safety net for the rest. Without that safety net, N+1 is the default outcome of any loop over lazy collections.

## The four shapes and their measured SQL

| Strategy | How selected | SQL issued to touch 25 lazy collections | Best for | Watch out |
| --- | --- | --- | --- | --- |
| **SELECT** (default) | nothing — lazy access | **25 queries** (`where parent_id = ?` each) | single-parent drilldowns | N+1 in loops |
| **JOIN** | `JOIN FETCH`, `@EntityGraph` | 1 query with a join | one aggregate + children in one round trip | row multiplication on two `List`s (`MultipleBagFetchException`); paging breaks — in-memory pagination |
| **BATCH** | `hibernate.default_batch_fetch_size=10`, or `@BatchSize(size=10)` on the association | **3 queries** — `where parent_id in (?,?,?,?,?,?,?,?,?,?)` ×3 (10+10+5) | default safety net for everything lazy | still several queries; IN padding matters for statement caches |
| **SUBSELECT** | `@Fetch(FetchMode.SUBSELECT)` | 1 query — `where parent_id in (select …)` (the original parents query reused) | all parents from one query, iterate every collection | only helps when parents came from **one** query; harmless otherwise |

The measured batch run shows the mechanism precisely: after loading 25 parents, touching all their lazy tag collections issued exactly three queries with ten-slot `IN` lists (the last holding five), each returning the tag rows for ten parents at once. Total SQL dropped from 26 (parents + 25 collections) to 4 (parents + 3 batches) without changing a single query in the application — which is why batch size is the highest-leverage **one-line** tuning in Hibernate for read paths that were not worth hand-optimizing.

```java
// global safety net
spring.jpa.properties.hibernate.default_batch_fetch_size=10

// per-association override
@OneToMany(mappedBy = "order", fetch = FetchType.LAZY)
@BatchSize(size = 25)
private List<Item> items;

// per-query precision where it matters most
@Query("select o from Order o join fetch o.items where o.id = :id")
Order findWithItems(@Param("id") Long id);
```

**Listing 1.** The layered setup: lazy everywhere, batch size as the global floor, explicit `JOIN FETCH` for the hot paths that deserve exact control.

## Choosing a shape per access pattern

The decision is about **cardinality of parents and reuse of their collections**. One parent, its children needed → `JOIN FETCH` (one query, no multiplication). A handful of parents from arbitrary access paths (second-level cache, different queries) → batch, because you cannot predict which collections will be touched and the `IN` grouping catches whatever set materializes. All parents from one named query, all collections needed → SUBSELECT, which is the only strategy whose SQL *reuses* the parent query rather than listing ids — valuable when the parent selection is an expensive filter, since batch would re-list thousands of ids as literals in `IN`. And the default SELECT remains correct for associations that are usually not touched: the strategy with zero upfront cost and one query on demand is exactly right for the cold path. Two senior caveats: EAGER (`FetchType.EAGER`) forces the JOIN-ish behavior globally and permanently, taking the decision away from every use site — which is why eager-by-annotation is treated as an anti-pattern; and batch/SubSelect only apply to lazy associations — with EAGER, the multiplication happens at load time instead.

> [!warning] Batch size is not a license to stop looking
> Three `IN`-queries of ten slots still fetch **every** row of **every** collection of **every** parent in the result — batching reduces round trips, not data volume. For wide results with big collections the correct fix is still a DTO projection that fetches only what the response needs; batch merely turns "unusable" into "tolerable" while you measure.

> [!tip] Interview answer
> Four SQL shapes: SELECT per association — the N+1 default; JOIN through fetch joins and entity graphs — one query but row multiplication on two lists and pagination gotchas; BATCH — lazy loads grouped into IN-lists, measured 25 collections in 3 queries at batch size 10; SUBSELECT — one subquery reusing the parents' query when all collections of one selection are iterated. Lazy/eager decides when, the strategy decides how, and they compose: keep everything lazy, set default_batch_fetch_size as the global safety net, and use JOIN FETCH or entity graphs on the hot paths where exact control matters. EAGER-by-annotation removes the per-use-case choice, which is the real argument against it.

See [[What is the N plus one problem in Hibernate]], [[What is JOIN FETCH and EntityGraph in Spring Data JPA]], [[What is MultipleBagFetchException and how do you fetch two collections]], [[What is the difference between JPA FetchType lazy and eager]], and [[What is the Hibernate query plan cache]].
