<!--
reps: 0
priority: 0
-->
#Databases/NormalForms #Databases/SQL #SystemDesign/Tradeoffs #SRS

# What is database denormalization for

> [!abstract] Short answer
> Denormalization deliberately re-introduces redundancy — precomputed joins, aggregated columns, duplicated attributes — so reads avoid JOINs and recalculation at query time. It exists for read speed: fewer round trips, simpler plans, smaller scan sets. The price is paid on writes, which must now update several copies, and in consistency risk if those updates are not managed.

## What it buys on the read path

A normalized schema stores each fact once, so answering "order total with customer name and product category" joins four tables. A denormalized schema stores order total, customer name and category right on the order row or a read-optimized table, and the query becomes one indexed lookup. That removes join latency, planner risk on wide joins, and the CPU cost of aggregating on every read — which is why reporting tables, materialized views, and read models (the query side of CQRS) are all denormalization in different costumes. The trigger is measured, not aesthetic: a JOIN that dominates query time, an aggregation recomputed identically on every request, or a query-side model that wants a shape the normalized core cannot serve. [[How would you explain denormalization tradeoffs in relational databases]] develops the cost side; [[How do database indexes work at a high level]] is the complementary read accelerator that does not duplicate rows.

```sql
-- normalized: aggregate on every read
SELECT c.name, SUM(o.total)
FROM customers c JOIN orders o ON o.customer_id = c.id
GROUP BY c.id;

-- denormalized: maintained on write, read is a scan-free lookup
-- orders_agg(customer_id, name, order_count, total_sum)
SELECT name, total_sum FROM orders_agg WHERE customer_id = 42;
```

**Listing 1.** The same read answered by a runtime JOIN versus a maintained aggregate row.

## The maintenance contract

Every denormalized copy is a second fact that must be kept true. Three maintenance strategies cover the field: application-side updates in the same transaction (simple, but the writer must remember every copy), triggers or rules inside the database (keeps copies near the data, harder to observe), and asynchronous rebuilds — materialized view refresh or a CDC/event pipeline that updates the read model shortly after the write (eventual consistency, but writes stay cheap). The chosen strategy defines the staleness budget readers must accept. [[What is the difference between atomicity and consistency]] frames why multi-copy updates need transactional care, [[What is eventual consistency]] the async variant, and [[How does an aggregate persist and publish events without a distributed transaction]] shows the outbox pattern that feeds event-driven read models.

> [!warning] Denormalization without a maintenance path is corruption on a timer
> A duplicated column updated by some writers but not others produces silently wrong answers — not errors. Before adding redundancy, name the mechanism that keeps it true and what staleness is acceptable.

> [!tip] Interview answer
> Denormalization trades write cost and redundancy for read speed: precomputed joins or aggregates so queries skip JOINs and recalculation. I use it when measurements show joins or aggregation dominating reads, and I pay for it with transactional or event-driven maintenance of every copy.
