<!--
reps: 0
priority: 0
-->
#DSA/DataStructures/Tree/BTree #SRS

# What is a B-tree

> [!abstract] Short answer
> A **wide, shallow, always-balanced search tree** built for block storage: each node holds **many** sorted keys and spans one disk page, all leaves sit at the **same depth**, and splits on insert keep it that way. Branching in the hundreds makes the tree a few levels tall even for millions of rows, so a lookup costs a handful of page reads. It is the **default index** of `CREATE INDEX` in PostgreSQL and the workhorse index in MySQL/InnoDB and most databases.

## Shape and lookup

A B-tree of large order packs up to hundreds of keys per node, and each key acts as a routing boundary: a search descends from the root, choosing between the key ranges of child links, and every path from root to leaf has exactly the same length — the balance invariant. Because keys are kept sorted, the structure answers anything order-based: `=`, `<`, `<=`, `>`, `>=`, `BETWEEN`, `IN`, `IS NULL`, and `ORDER BY` can be served straight from the index; for text, a `LIKE` pattern anchored at the front (`LIKE 'pre%'`) still works because the prefix narrows a range. Sorted-keys-ON-disk is the family trait it shares with the LSM world's [[What are SSTables and LSM trees]] — the B-tree keeps its order in place, the LSM side rewrites it in levels. Node = one page is the design point: the fewer pages touched, the fewer disk (or cache-miss) reads.

```sql
CREATE INDEX idx_orders_customer ON orders (customer_id, created_at);
-- order-preserving range read straight from the B-tree:
SELECT * FROM orders
WHERE customer_id = 42
  AND created_at >= '2026-01-01'
ORDER BY created_at DESC
LIMIT 20;
```

**Listing 1.** A composite B-tree index serving equality on the leading column, a range and sort on the second — in one structure, top to bottom. When the tree's order already matches the query's `ORDER BY`, the sort step disappears entirely — [[How do you avoid a sort with an index]].

## Inserts and how balance survives

An insert lands in a leaf page; when the page overflows it **splits** around the median key and pushes the middle key up into the parent, and a parent overflow splits again — the split propagating upward is the only rebalancing mechanism, and it preserves the equal-depth-leaves invariant. Deletions merge or redistribute between sibling pages. This is why the structure needs no global reorganization: pages are mutated in place and the tree grows sideways from the root. The flip side of sorted-on-disk storage shows up in EXPLAIN plans: reading the whole row still costs a visit to the table, the gap measured in [[What is Heap Fetches in an EXPLAIN plan]].

> [!warning] A B-tree is not a binary tree, and it cannot search mid-string
> The "B" confused generations of interviewees — order is measured in *hundreds of keys per node*, not 2. And the prefix trick stops at anchors: `LIKE '%foo%'` or `'%infix%'` cannot use a B-tree on the pattern column (that is trigram/GIN territory, as is JSONB containment), and the hash index type answers equality only. A composite index also follows the **leftmost prefix** rule — skipping the leading column leaves the rest unusable for range narrowing.

> [!tip] Interview answer
> A B-tree is a balanced multi-way search tree where each node holds many sorted keys and maps to a storage page; all leaves are at the same depth because splits push medians up to the parent. Sorted, order-preserving pages give equality, ranges, sorting and anchored LIKE in a few page reads — that's why PostgreSQL's CREATE INDEX defaults to it. Not to be confused with a binary tree, and useless for infix search — that needs GIN or trigrams.
