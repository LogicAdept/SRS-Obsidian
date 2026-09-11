<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> HTTP caching keys on **URLs and methods**; GraphQL collapses every operation onto one endpoint (usually POST), so the cache key degenerates to a single URL and the response to a body that depends on the request body — which HTTP caches cannot key on. Result: standard caching (browsers, CDNs, reverse proxies) goes dark, and caching moves into client libraries keyed on the query *document*, or into carefully engineered GET+APQ setups.

## Why the uniform interface stops helping

REST works with HTTP caching because resource URLs are stable and responses are reusable across clients: `GET /users/1` with `Cache-Control` is cacheable by every intermediary, and mutations invalidate via `POST`/`PUT` semantics. GraphQL's common contract is `POST /graphql` with the operation inside the body: intermediaries see identical URL and headers for *every* operation, and the spec's semantics make response reuse per-URL meaningless — two clients sending different documents to the same URL must get different bodies ([[What is the difference between GraphQL and REST]]). Cache-Control headers still arrive, but the cache cannot answer "which operation was this?".

The client-side replacement: normalized caches (Apollo, Relay) key on **object identity** (`Type:id`) and the selection set, so repeated operations hit a local store, and mutations trigger refetch/invalidation logic driven by `__typename` and ids ([[What is the typename meta field in GraphQL]]). That is a different cache — per-client, in memory, logic-aware — not the shared, TTL-driven, intermediary cache HTTP gives REST.

```d2
direction: down
R: "REST GET /users/1" { width: 240; height: 60 }
H: "HTTP cache hits on URL" { width: 260; height: 60 }
G: "POST /graphql\noperation in body" { width: 240; height: 65 }
C: "cache sees one URL\nfor all operations" { width: 280; height: 65 }
L: "client-side normalized cache\nkeyed Type:id + selection" { width: 320; height: 70 }
R -> H: "cacheable"
G -> C: "degenerate key"
C -> L: "caching moves here"
```

**Fig. 1.** The cache key moves: URL in REST; in GraphQL the URL is constant, so caching relocates to the client's document/object keying.

```text
# REST:            GET /users/1
#                  Cache-Control: max-age=60   -> any CDN/proxy/browser may reuse per URL
# GraphQL (POST):  POST /graphql   body {"query":"{ user(id:"1"){ name } }"}
#                  Cache-Control: max-age=60   -> key is the URL, identical for every operation:
#                  a shared cache cannot tell this document from any other one
```

**Listing 1.** Same cache header, different fate: the REST URL carries identity; the GraphQL URL does not, so the header alone cannot authorize shared reuse.
> [!warning] The workarounds exist — each with a catch
> First: **GET for queries** with the document in the query string restores URL cacheability, but URLs have length limits and mutations are forbidden on GET, so it covers only part of the surface ([[What is the difference between a GraphQL query a mutation and a subscription]]). Second: **automatic persisted queries** send a hash instead of the text, shortening GETs and enabling CDN edges — but they need a registration protocol and a cold-path fallback for unknown hashes ([[What are persisted queries in GraphQL]]). Third: edge caching per operation hash works only for **shared** documents; user-specific responses leak risk if cache keys ignore variables or auth context — a classic cache-poisoning bug ([[How do you authenticate and authorize a GraphQL request]]).

A senior framing: GraphQL trades HTTP's shared cache for **exactness** — the payload matches the view, but the shared-cache layer is forfeit; whether that trade pays depends on how much of your traffic was cacheable anyway ([[When should you not use GraphQL]]). Public, hot, identical-for-everyone data is precisely where GraphQL costs the most; first-party, user-scoped views are where its client cache shines.

> [!tip] Interview answer
> HTTP caches key on URL and method; GraphQL funnels all operations through one endpoint with the operation in the body, so intermediary caching sees a constant key and goes dark. Caching relocates into client-side normalized stores keyed by object id and selection; GET-with-APQ restores partial URL cacheability with registration and size caveats. You trade HTTP's shared cache for exact per-view payloads.

