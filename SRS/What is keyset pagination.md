<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS

# What is keyset pagination

> [!abstract] Short answer
> Keyset (seek, cursor) pagination fetches the next page with a WHERE predicate on the last seen sort key — WHERE (created_at, id) < (:ts, :id) ORDER BY created_at DESC, id DESC LIMIT n — instead of OFFSET. The predicate is a direct index seek, so page N costs the same as page 1, while OFFSET must read and discard all preceding rows.

## The mechanism and why it needs an index

The cursor is the sort tuple of the last row on the previous page; the next-page query asks for rows strictly after that tuple in the same order the index provides. For that to be a seek, the ORDER BY columns must match an index and the row-comparison predicate must be sargable — `(created_at, id) < (:ts, :id)` is row-constructor syntax the planner resolves into the range after the cursor position. This is the ordered-scan property of B-trees combined with early termination, the same machinery as top-N queries in [[How does LIMIT interact with ORDER BY and indexes]] and the ordering design in [[How do you avoid a sort with an index]]. The composite must include a unique tiebreaker (usually the primary key) so the order is total — otherwise equal sort keys make pages unstable and rows can repeat or vanish between pages.

```sql
CREATE INDEX idx_feed ON posts (created_at DESC, id DESC);

-- page 1
SELECT id, title, created_at FROM posts
ORDER BY created_at DESC, id DESC LIMIT 20;

-- next page: cursor = last row's (created_at, id)
SELECT id, title, created_at FROM posts
WHERE (created_at, id) < (:last_ts, :last_id)
ORDER BY created_at DESC, id DESC LIMIT 20;
```

**Listing 1.** Every page is an index range starting at the cursor: constant cost per page, no OFFSET arithmetic.

## Why not OFFSET, and the trade-offs to name

OFFSET n reads and discards n rows before returning the page — at depth 100000 with 20-row pages, that is a hundred thousand ordered reads per request, and concurrent inserts make deep OFFSET pages additionally unstable (rows shift between pages). Keyset pages are stable in that sense (new rows appear ahead of the cursor, not inside it), cost O(page) at any depth, and map naturally to infinite-scroll APIs. The honest trade-offs: no random jump to page 47 (there is no cheap way to seek to the 47th sort position without reading 46 pages worth), cursor encoding becomes part of the API contract, and filters must keep the sort columns in the composite prefix, per [[What is the leftmost prefix rule for composite indexes]]. The same seek predicate shape underlies the design patterns in [[How would you design a 100 million row table with fast lookup by int32]] and [[How do you design indexes for a search API]].

> [!warning] "Cursor pagination works without a matching index" and "row constructors are magic"
> Without an index whose prefix matches ORDER BY, the keyset predicate still forces a full sort of everything after the filter — the cursor syntax alone saves nothing. And the row-constructor comparison must be recognized by the planner (PostgreSQL resolves it into index conditions; some engines or ORMs need the expanded (a < x OR (a = x AND b < y)) form). The tiebreaker omission is the bug that shows up as duplicated rows in production feeds.

> [!tip] Interview answer
> Keyset pagination uses the last row's sort tuple as a cursor: WHERE (created_at, id) < cursor ORDER BY created_at DESC, id DESC LIMIT n. With a matching composite index each page is one index seek plus n rows, constant cost at any depth, unlike OFFSET which reads and discards everything before the page. Requirements: a unique tiebreaker for total order, an index matching the sort, and accepting no random page jumps.
