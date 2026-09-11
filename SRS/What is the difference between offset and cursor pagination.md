<!--
reps: 0
priority: 0
-->
#API/REST #SRS

# What is the difference between offset and cursor pagination

> [!abstract] Short answer
> Offset pagination (page=3&size=20) addresses rows by position — simple, jumpable, but unstable under concurrent inserts and degrading linearly with depth. Cursor pagination (after=opaque-token&size=20) addresses rows by a stable anchor — consistent pages under writes and constant cost via index seek — at the price of no random access and a harder contract.

## The mechanics that decide behavior

Offset pagination translates to LIMIT/OFFSET: the database must produce and discard the first offset rows, so page 1000 costs page 1000's work — linear degradation that hurts exactly the users who scroll deepest ([[What is a database index and why does it speed up queries]] for why seek beats scan). Worse, it is position-under-concurrency: an insert before your window shifts everything — the classic page-boundary duplicate or missed row. Cursor pagination anchors on the last seen sort key: after=`encoded(id,sortvalue)`, translated to a WHERE clause on the sort index (id > last or (created,tiebreak) < last), so every page is an index seek of size N — constant cost — and concurrent inserts cannot shuffle already-delivered windows. Cursors must be opaque to clients (Base64 of the key tuple is standard practice — parseable cursors invite tampering) and always carry a deterministic tiebreaker (the unique id) or equal sort values produce wobble ([[What harmful SQL patterns or pitfalls do you know]] for the query-side view).

```d2
off: offset page=2 size=3 {
  scan: rows 1..3 scanned,
discarded
  row: rows 4..6 returned
  risk: insert before window
shifts pages
}
cur: cursor after=bzoz size=3 {
  seek: index seek from anchor
  row: next 3 by (sort,id)
  stable: concurrent inserts
cannot shift window
}
off.scan: cost grows with depth
cur.seek: cost constant
```

**Fig. 1.** Offset pages walk from the start every time; cursor pages seek straight to the anchor and stay stable under writes.

## The contract trade-offs

Offset's virtues are real: humans can link to page 5, totals are natural (total, page count), and back/forward is trivial. Cursor's costs are the same coin reversed: no total (counting the filtered set defeats the point at scale), no jumping — only next/prev relative to the current window, and the cursor is only valid against the same sort. The standard REST encoding serves both: RFC 8288 Link headers with rel="next" (and "prev") keep clients from constructing URLs at all — a HATEOAS-shaped contract ([[What is HATEOAS]]) — while the body carries data plus a nextCursor (null or absent at the end). Note when each fits: admin consoles and small collections stay offset (cheap, jumpable); feeds, timelines, export streams, and any deep-scroll surface take cursors ([[What are the key principles of good API design]]: one rule per collection type, applied everywhere; [[How do you design filtering and sorting for a REST API]] for the sort grammar the cursor must encode).

```text
page 1: 200 {"data":["a","b","c"],"nextCursor":"bzoz"}  Link: <http://127.0.0.1:18085/items?limit=3&cursor=bzoz>; rel="next"
page 2: 200 {"data":["d","e","f"],"nextCursor":"bzo2"}  Link: <http://127.0.0.1:18085/items?limit=3&cursor=bzo2>; rel="next"
page 3: 200 {"data":["g","h"],"nextCursor":null}  (no next)
```

**Listing 1.** Verified on JDK 21 (com.sun.net.httpserver): Base64 cursor (o:3 -> bzoz), Link rel="next" driving the walk, null nextCursor terminating it (out/A05_LinkPagination.txt).

> [!warning] A cursor is valid only for one sort and one snapshot
> Passing a cursor built for sort=-price into a name-sorted query, or a page-one cursor into a filtered variant, yields garbage or leaks rows across filter boundaries. Bind the cursor to its sort and filter set (sign or embed them), and treat cursor reuse after eviction as an error, not a fallback.

> [!tip] Interview answer
> Offset pages are LIMIT/OFFSET — jumpable and total-friendly, but each page rescans from the start and concurrent inserts shift windows, duplicating or skipping rows. Cursors anchor on the last row's sort key plus a unique tiebreaker, encoded opaquely: every page is an index seek with constant cost and stable windows, but there is no total and no jumping. I ship cursors for feeds and deep scrolls behind Link rel="next", offset only for small admin tables.
