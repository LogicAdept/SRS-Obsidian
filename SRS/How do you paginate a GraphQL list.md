<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> GraphQL has **no built-in pagination** — the schema designs it, and the de-facto standard is the Relay **Connection** pattern: a field takes `first`/`after` (and `last`/`before`), returns `edges` (each wrapping a `node` plus an opaque `cursor`) and a `pageInfo` block (`hasNextPage`, `hasPreviousPage`, `endCursor`). Cursors make paging stable and direction-agnostic; offset paging stays possible but inherits its classic problems — instability under inserts and linear cost at depth.

## The Connection pattern mechanically

A cursor encodes a **position in the underlying ordering** — commonly Base64 of something like `cursor:<index>` or a keyset value; clients treat it as opaque and echo it back via `after:`. The resolver slices `first` entries starting after that position and reports the page's first/last cursors plus neighbor flags. Because the cursor embeds ordering, a page fetched after an insert lands on the *same logical position* rather than shifting — the property offset pagination lacks ([[Why is OFFSET pagination slow]]).

```java
// graphql-java 26.1: friends(first: Int, after: String) with cursor:<index> in Base64.
// p1: { friends(first: 2) { edges { cursor node { name } } pageInfo { hasNextPage } } }
// {"data":{"friends":{"edges":[
//   {"cursor":"Y3Vyc29yOjA=","node":{"name":"Luke"}},
//   {"cursor":"Y3Vyc29yOjE=","node":{"name":"Leia"}}],
//   "pageInfo":{"hasNextPage":true}}}}
// p2 echoes endCursor into $after -> {"edges":[{"node":{"name":"Han"}},{"node":{"name":"Chewbacca"}}],
//                                     "pageInfo":{"hasNextPage":true,"hasPreviousPage":true}}
```

**Listing 1.** Verified on graphql-java 26.1: page two was requested by echoing the opaque cursor from page one's `pageInfo` — the client never decoded anything ([[How do you pass arguments to a GraphQL field]]).

```d2
direction: down
Q: "friends(first: 2, after: $cursor)" { width: 320; height: 60 }
E: "edges[] = { cursor, node }" { width: 280; height: 60 }
PI: "pageInfo { hasNextPage, endCursor }" { width: 330; height: 60 }
N: "next request: after: endCursor" { width: 310; height: 60 }
Q -> E
Q -> PI
PI -> N: "echo"
N -> Q: "next page" 
```

**Fig. 1.** The pagination contract: slice by cursor, report neighbor state, let the client chain pages without understanding the encoding.

> [!warning] Cursor design mistakes that surface in production
> First: **keyset over index** at the store level — a cursor resolving to `OFFSET 100000` keeps offset's linear scan cost; encode the last-seen sort key (`(created_at, id)`) so the store seeks ([[What is keyset pagination]]). Second: **ordering must be total** — ties break cursors; include a unique tiebreaker (primary key) in the sort, or pages can skip or repeat rows ([[What is the difference between PRIMARY KEY and UNIQUE]]). Third: **clients decoding cursors** couples them to internals; changing the encoding breaks old clients mid-flight — version the cursor format or keep it truly opaque. Also: `edges` wrapping seems redundant until per-edge data appears (cursors, permissions, extra fields) — flattening early is a classic refactor trap ([[Which GraphQL schema changes are breaking]]).

Alternatives worth naming: plain `limit/offset` arguments for admin screens and tiny datasets (simple, cache-friendly, unstable under writes); and keyset arguments (`after_created_at`, `after_id`) when clients benefit from explicit filtering. Connections win because they are uniform, direction-capable, and carry pagination metadata in-band — which is why generated clients and caches special-case them ([[What is global object identification in GraphQL]]).

> [!tip] Interview answer
> GraphQL leaves pagination to the schema; the Relay Connection pattern is the standard: first/after arguments, edges holding node plus opaque cursor, and pageInfo with hasNextPage/hasPreviousPage. Cursors encode a position in the ordering — ideally a keyset value, never a raw offset — giving stability under inserts and direction-agnostic paging. Keep cursors opaque, make ordering total with a unique tiebreaker, and reserve offset for small static lists.

