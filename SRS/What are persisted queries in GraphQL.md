<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> Persisted queries store the **document text on the server** (registered by hash), so clients send only the hash plus variables instead of the query text. Benefits: smaller requests, no arbitrary documents at runtime (a hard allowlist that neutralizes cost attacks), versioned operations as build artifacts, and CDN-cacheable GETs. The common extension is **Automatic Persisted Queries (APQ)**: clients first send just the hash; on a miss they register the full document once.

## The mechanisms: registry-first and APQ

**Registry-first**: at build or deploy time, every operation the client ships is registered (by SHA-256 of the document); production traffic carries `{extensions: {persistedQuery: {version: 1, sha256Hash}}}` plus variables; unknown hashes are rejected outright — the strongest rate-limiting posture available, because cost is known at deploy time ([[Why is rate limiting harder in GraphQL than REST]]).

**APQ** inverts registration: the first request sends the hash; the server answers with `PersistedQueryNotFound`; the client resends hash + document, the server stores the pair; subsequent requests go hash-only. This fits apps without a build-time registry but means unknown clients can seed arbitrary documents — so APQ softens, not removes, the allowlist property ([[What is query complexity analysis in GraphQL]]).

```text
# APQ round trip:
# 1) POST /graphql  { "extensions": { "persistedQuery": { "version": 1, "sha256Hash": "abc..." } },
#                     "variables": { "id": "2000" } }
#    -> { "errors": [ { "message": "PersistedQueryNotFound" } ] }
# 2) POST /graphql  same hash + "query": "query D($id: ID!) { droid(id: $id) { name } }"
#    -> server registers (hash, document)
# 3) later: hash + variables only -> {"data":{"droid":{"name":"C-3PO"}}}
```

**Listing 1.** The APQ dance: probe with the hash, register on miss, then hash-only traffic. Registered operation text stays byte-stable, which is what document caches rely on ([[Why prefer GraphQL variables over inlined values]]).

```d2
direction: down
C: "client: sha256(query)" { width: 230; height: 55 }
S: "server registry" { width: 200; height: 55 }
H: "hit: execute stored doc\n+ variables" { width: 280; height: 65 }
M: "miss: PersistedQueryNotFound" { width: 300; height: 60 }
R: "client resends doc -> registered" { width: 320; height: 60 }
C -> S
S -> H: "hash known"
S -> M: "unknown"
M -> R: "APQ only"
```

**Fig. 1.** Registry-first starts from a known map; APQ fills it lazily. Either way the runtime contract becomes "hash plus variables".

> [!warning] Hashes bind documents — change either side deliberately
> First: any **document edit changes the hash** — that is the safety property, but it means operation renames and whitespace edits ship like code: the registry update and the client release must land in the right order, or production 404s on its own queries ([[How do you version a GraphQL schema]]). Second: persisted **does not mean authorized** — the document still selects fields; every enforcement layer (auth, cost limits for unregistered traffic) stays in place ([[How do you authenticate and authorize a GraphQL request]]). Third: caches keyed on hashes must include **variables and user context** in the key — a shared cache replaying user A's response to user B is a data-leak bug, not a caching win ([[Why is HTTP caching harder with GraphQL than REST]]).

Deployment nuance: persisted queries pair naturally with GET — short URLs become CDN-cacheable for shared, non-user-specific operations; user-scoped operations stay POST. Registries also anchor analytics: operation names and hashes give stable metrics where free-form documents give none ([[What is GraphQL introspection]]).

> [!tip] Interview answer
> Persisted queries replace document text with a server-known hash: registry-first (build-time allowlist, known costs, hard rejection of unknown documents) or APQ (hash probe, one-time registration, then hash-only). Wins: small requests, CDN-friendly GETs, operation-level analytics, and an effective abuse ceiling. Costs: hash coupling between client releases and registries, and none of it replaces authorization — documents still resolve through the same enforcement layers.

