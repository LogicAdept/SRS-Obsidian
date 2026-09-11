<!--
reps: 0
priority: 0
-->
#API/REST #SRS

# How do you design filtering and sorting for a REST API

> [!abstract] Short answer
> Keep collection queries in the query string with one grammar for every endpoint: dedicated parameters for field filters (category=books, maxPrice=3000), a sort parameter with a direction convention (sort=-price,name), and pagination parameters. Document which fields are filterable and sortable — the allowed set is a contract, not whatever the database happens to do.

## The parameter grammar

Filter parameters name the field and the value; comparison operators become distinct parameters (maxPrice, minPrice, createdAfter) or an operator suffix when the surface grows (price[lte]=100). Sorting uses a comma-separated field list with a minus prefix for descending — sort=-price,name — which keeps the common case one token long. Every collection endpoint reuses the same pagination parameters so clients compose them uniformly ([[What is the difference between offset and cursor pagination]]). Sparse fieldsets (fields=id,name) trim payload width for mobile clients. The server, not the client, owns validity: unknown filter fields must fail fast (400) rather than silently match nothing, and the response should state which filters and sorts were applied — it makes debugging and caching keys honest ([[What are the key principles of good API design]]).

```text
category=books:            [{"id":2,"name":"Book REST","price":1800},{"id":4,"name":"Book HTTP","price":2900}]
maxPrice=3000 sort=-price: [{"id":4,"name":"Book HTTP","price":2900},{"id":1,"name":"Mouse","price":2500},{"id":2,"name":"Book REST","price":1800}]
sort=name limit=2:         [{"id":4,"name":"Book HTTP","price":2900},{"id":2,"name":"Book REST","price":1800}]
```

**Listing 1.** Verified on JDK 21 (com.sun.net.httpserver): one in-memory catalog served through the grammar — multi-field sort with -price descending and name ascending tie-break, plus a limit parameter (out/A11_FilterSort.txt).

## Where the designs go wrong

Each deviation from the grammar becomes a support burden: SQL fragments in query values invite injection — translate parameters into safe, allow-listed queries and never interpolate them ([[What harmful SQL patterns or pitfalls do you know]]); unbounded sort/filter fields turn into full-table scans, so allow-list fields that have indexes and reject the rest ([[What is a database index and why does it speed up queries]]); and deep ad-hoc query languages in URLs (homegrown RSQL/SQL-where dialects) grow into unmaintainable, cache-hostile monsters — if clients genuinely need arbitrary queries, that is a sign to consider a dedicated query surface ([[What is the difference between GraphQL and REST]] for the query-shaped alternative). POST-based search bodies (POST /products/search) are the accepted escape hatch when filter sets get too large or sensitive for URLs — it forfeits cacheability and bookmarkability, so it is a deliberate trade ([[What is content negotiation in REST APIs]] and caching interplay).

```d2
q: query string
v: validate + allow-list fields
f: filter stream
s: sort (multi-field, -desc)
pg: paginate (shared params)
r: response + echo applied filters
q -> v
v: unknown field -> 400
v -> f -> s -> pg -> r
```

**Fig. 1.** The collection pipeline: strict validation, allow-listed filtering, deterministic sort, shared pagination, honest echo.

> [!warning] Unknown filter parameters must not be ignored
> Silently ignoring a mistyped filter returns unfiltered data — a privacy incident dressed as a convenience bug (clients see other tenants' rows because tenantId=123 was misspelled). Validate strictly and fail with 400 naming the unknown parameter.

> [!tip] Interview answer
> One grammar for all collections: field filters as named parameters or operator suffixes, sort as a comma list with minus for descending, the shared pagination parameters, and optional sparse fieldsets. Unknown or non-indexed fields fail with 400, parameters never reach SQL untranslated, and the response echoes the applied filters and sort. Large or sensitive filters move to a POST search endpoint as a conscious trade against caching.
