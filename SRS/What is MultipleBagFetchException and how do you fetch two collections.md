<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate/Fetching #SRS

# What is MultipleBagFetchException and how do you fetch two collections?

> [!abstract] Short answer
> Join-fetching **two `List`-typed (bag) collections** in one query — `select o from Order o join fetch o.lines join fetch o.payments` — fails at execution with **`MultipleBagFetchException`**. The SQL itself (a cartesian join) would run, but Hibernate cannot deduplicate the result: a bag has **no identity/order column**, so duplicated parent rows from the cartesian product cannot be collapsed reliably. Fixes, in order of preference: **two queries in one transaction** (each fetches one collection; the first-level cache merges them into one object graph — no cartesian product, no exception), **`Set` instead of `List`** for genuinely unordered collections, or a **DTO projection** that selects exactly what the screen needs. Related trap with any single fetched collection: **`setFirstResult`/`setMaxResults` on a collection-fetch query applies pagination in memory** after loading the whole joined result (warning **HHH000104**) — page the parent ids first, then fetch collections for that page.

## Why two bags break

A bag is a `List` without an index column: duplicates are meaningful to the provider only through entity identity. Fetch **one** bag with a join and the result has duplicated parent columns (one row per child); Hibernate collapses them because each child row maps to exactly one entity instance and the parent object appears once per its children. Fetch **two** bags and the rows multiply: a parent with 3 lines × 4 payments yields **12 rows**, and no child row uniquely identifies which line–payment pair produced it — reconstructing two independent bags from a flat cartesian result is ambiguous, so the provider refuses up front.

| Approach | SQL cost | Result | Verdict |
| --- | --- | --- | --- |
| Two `join fetch` in one query | parent_count × lines × payments rows | `MultipleBagFetchException` | broken by design |
| **Two queries, one session** | parent + lines + payments (3 round trips) | L1 identity merges into one graph | **default fix** |
| `Set`-typed collections | cartesian still, but dedupable | works, single query | OK for small bounded sets |
| DTO projection | exactly the needed columns | no entity graph to merge | best for read screens |

```java
// two round trips, no exception, one graph in memory
List<Order> orders = em.createQuery(
        "select distinct o from Order o left join fetch o.lines where o.id in :ids",
        Order.class).setParameter("ids", ids).getResultList();
orders = em.createQuery(
        "select distinct o from Order o left join fetch o.payments where o in :os",
        Order.class).setParameter("os", orders).getResultList();
// both collections are now initialized on the same managed instances
```

**Listing 1.** The split-fetch pattern. The second query returns the *same* managed `Order` instances (first-level cache identity), with their payments initialized — the two graphs are one.

## The pagination gotcha rides on the same mechanics

Limit/offset in SQL applies to **rows**; with a join-fetched collection the rows are the cartesian product, so `setMaxResults(20)` would silently cut a parent's children. Providers therefore **apply the limit after loading the full result in memory** and log the **HHH000104** warning — firstResult/maxResults were applied in memory. With a large parent set that is an OOM with a warning in the log as its only marker. The stable pattern: page the **parent ids** (a plain entity or DTO query with limit/offset, or keyset pagination), then run the fetch queries for that id batch — [[What is the N plus one problem in Hibernate]]'s fix toolkit with pagination discipline on top.

## Choosing per use case

The exception is a **design signal, not an obstacle**: if two collections are needed for one screen, either the screen needs a **projection** (flat rows — build the DTO in one query and skip entity graphs entirely), or the aggregate is being fully loaded for mutation, where **two fetches in one transaction** are honest about the round trips. Rewriting `List` to `Set` "to silence the exception" changes the domain model to satisfy a fetch strategy — defensible only when the collection truly is unordered and duplicate-free, which for payments or lines it usually is not. Note also that `@OrderColumn`-indexed lists are **indexed collections, not bags** — they can be fetched together, at the price of the order-column rewrite costs covered in [[What is ElementCollection and how does it differ from OneToMany]].

> [!warning] The exception is loud; HHH000104 is quiet
> `MultipleBagFetchException` fails fast and forces a redesign. In-memory pagination does the **opposite**: the query succeeds, tests pass on small data, and the cost appears as heap pressure in production on the first large page. Grep the logs for `HHH000104` as part of the release checklist for any repository method combining `Pageable` with a `join fetch` on a collection.

> [!tip] Interview answer
> Two bag-typed collections cannot be join-fetched in one query: the cartesian rows cannot be reconstructed into two independent bags, hence `MultipleBagFetchException`. My default fix is two queries in one transaction — the first-level cache identity merges them into a single graph — with a DTO projection when the use case is a read screen. The adjacent trap is pagination over a collection fetch: limits apply in memory after the full result is loaded, the HHH000104 warning is the only trace, so I page parent ids first and fetch collections for that page only.

See [[What is JOIN FETCH and EntityGraph in Spring Data JPA]], [[What is the N plus one problem in Hibernate]], [[What are JPA fetch types for entity associations]], and [[What is ElementCollection and how does it differ from OneToMany]].
