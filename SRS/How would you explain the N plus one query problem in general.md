<!--
reps: 0
priority: 0
-->
#Problems/Persistence #Databases #SRS

# How would you explain the N plus one query problem in general

> [!abstract] Short answer
> **N+1 is when fetching a list of N parent records takes one query, and then touching a related record of each parent issues one more query per parent — 1 + N round trips where one join or batched fetch would do.** It is the default failure mode of lazy loading in ORMs, and it scales linearly with list size.

## The mechanism, step by step

`orderRepository.findAll()` runs `SELECT * FROM orders` (that is the 1). The view then renders `order.customer.name` for each row; the association is lazy, so the first access per order fires `SELECT * FROM customers WHERE id = ?` — one per order (the N). One thousand orders → one thousand and one statements, each paying network round-trip and planning cost; the page that "should" be one query takes seconds. Hibernate's guide describes the same shape for EAGER associations: a secondary select issued per parent when the association is not covered by the driving query.

Detection is mechanical, not mystical: log or count statements — Hibernate's `generate_statistics`, a datasource proxy that asserts statement counts in tests (fail the build when a repository method issues more than K queries), or simply the slow log filling with one-row selects that repeat with different ids.

```java
List<Order> orders = orderRepository.findAll();      // 1 query
for (Order o : orders) {
    out.add(o.getCustomer().getName());              // +1 query per order
}
```

**Listing 1.** The canonical shape: one list query, then a lazy association touched inside the loop.

The fixes collapse the N into the 1 or into a handful: a join fetch so parents and relations come in one statement (`JOIN FETCH` in JPQL, an `@EntityGraph` on the repository method), batch fetching so Hibernate loads ids 1..1000 in chunks of `@BatchSize` (or the global `default_batch_fetch_size`) with `WHERE id IN (...)`, or a subselect fetch for whole-collection loads. The same problem and the same cures exist outside Java — Django's `select_related`/`prefetch_related`, GraphQL's DataLoader — because the root cause is per-parent round trips, not a particular ORM.

```sql
SELECT o.*, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id;
```

**Listing 2.** The join fetch version: one statement regardless of list size.

> [!warning] EAGER on the association does not fix N+1 — it hides it
> Marking the relation EAGER makes every load of the entity pay for the extra selects even when the caller does not need them, and a JPQL query that omits the association still triggers one secondary select per row. Fetch strategy is a default, not a guarantee; the query must request the join explicitly. Also distinguish N+1 from lazy loading being *wrong* in general — the bug is the per-row round trip, not laziness itself, per [[What are the drawbacks of lazy loading]].

For the JPA mechanics see [[What is lazy fetch in JPA or Hibernate]] and [[What is JOIN FETCH and EntityGraph in Spring Data JPA]]; for counting the damage, [[How do you systematically diagnose a slow SQL query]].

> [!tip] Interview answer
> N+1 is one query for the parents plus one per parent for a lazy or uncovered association, so cost grows with list size. I detect it by counting statements in tests — statistics or a datasource proxy — and fix it by fetching the relation in the driving query: join fetch or an entity graph, batch-size IN-loading as the fallback. EAGER is not a fix; it just moves the extra selects to every load.
