<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes/Covering #SRS

# What is an index-only scan in PostgreSQL?

> [!abstract] Short answer
> An index-only scan answers a query entirely from the index, skipping the heap — but only if the index contains every column the query needs and the table's pages are marked all-visible in the visibility map. The `EXPLAIN` node is `Index Only Scan`; its effectiveness shows in the `Heap Fetches` counter.

## The two requirements

1. The index must cover all referenced columns — either a B-tree whose key columns include them or an INCLUDE covering index ([[What is the difference between a composite index and an INCLUDE covering index]]).
2. PostgreSQL must prove row visibility without visiting the heap. Visibility lives only in heap tuples, so the engine consults the visibility map: a page with the all-visible bit set needs no heap visit; a page without it forces a heap fetch per row.

```d2
q: "SELECT id, status\nFROM orders WHERE user_id = 42" {width: 330; height: 80}
idx: "Index Only Scan on (user_id, status, id)\nall columns in the index" {width: 360; height: 80}
vm: "Visibility map\nall-visible page? skip heap" {width: 300; height: 80}
heap: "Heap fetch\nper row on not-all-visible pages" {width: 320; height: 80}
q -> idx -> vm
vm -> heap: "bit not set"
```

**Fig. 1.** The visibility map is the third participant: without it index-only scans would be impossible, and with stale bits the scan degrades toward an ordinary index scan.

## Why freshly loaded tables cannot use it

After bulk INSERT/UPDATE, pages are not all-visible — only VACUUM sets the bits ([[How would you explain the SQL VACUUM command in PostgreSQL]]). A table that just received a big COPY runs index-only scans with huge Heap Fetches until autovacuum passes. Append-only tables therefore benefit from the insert-driven autovacuum threshold ([[What is autovacuum in PostgreSQL]]).

## Reading it in a plan

```
Index Only Scan using orders_user_idx on orders
  (cost=0.43..8.45 rows=10 width=8) (actual time=0.03..0.06 rows=10 loops=1)
  Index Cond: (user_id = 42)
  Heap Fetches: 0
```

**Listing 1.** `Heap Fetches: 0` is the perfect case; a large number means the index is being used but the heap is being visited anyway — measure, do not trust the node name alone ([[What is Heap Fetches in an EXPLAIN plan]]).

> [!warning] "Index Only" does not mean no heap access
> The node name describes the theoretical plan; Heap Fetches tells the truth. On a churny table the difference from a plain Index Scan can be negligible, and SELECT-ing wide columns can never be index-only unless those columns are included in the index — which itself costs write amplification ([[How do you decide which database indexes to create]]).

> [!tip] Interview answer
> An index-only scan serves a query from the index alone when the index covers all needed columns and the visibility map marks pages all-visible, so no heap visit is required. Its real-world quality is the Heap Fetches counter: fresh writes make pages not-all-visible, and only VACUUM restores them — that is why bulk-loaded tables lose this optimization until vacuumed.
