<!--
reps: 0
priority: 0
-->
#API/REST #Caching #SRS

# How do you make REST API responses cacheable

> [!abstract] Short answer
> Cacheability is designed per resource: fresh responses declare Cache-Control (max-age, and no-store for anything private), and revalidation rides validators — ETag with If-None-Match answering 304 for the cheap update check. Conditional PUT uses If-Match as an optimistic-locking precondition. Authenticated responses default to private, and anything negotiated must carry Vary.

## The freshness model, then the validators

RFC 9111 splits caching into freshness and validation. Freshness is declarative: Cache-Control: max-age=60 lets any client or proxy reuse the response without asking; no-cache means "revalidate before reuse" (not "do not store"), no-store means never persist, and private keeps shared caches out. When freshness expires, the validator answers whether the cached copy still matches: the server returns ETag (a version token for the representation), the client re-sends it in If-None-Match, and a match gives 304 Not Modified with no body — saving the transfer, not the request. The same ETag reversed into If-Match protects writes: PUT with a stale tag fails 412 instead of clobbering a concurrent change. Last-Modified/If-Modified-Since is the timestamp alternative with one-second granularity ([[What is the relationship between HTTP and REST]] — this mechanism is REST's cacheability constraint made concrete).

```text
server: fresh GET -> 200 + ETag "rev-1"
client GET#1: 200 ETag="rev-1" Cache-Control=max-age=60, must-revalidate body={"title":"draft","rev":1}
server: If-None-Match match -> 304 (no body, cache reuse)
client GET#2 (If-None-Match): 304 bytes=0 (served from local cache copy)
server: If-Match "stale-rev" != current "rev-1" -> 412
client PUT (stale If-Match): 412 {"error":"precondition failed"}
```

**Listing 1.** Verified on JDK 21 (com.sun.net.httpserver): GET#1 stamps ETag and freshness; GET#2 revalidates to 304; a stale If-Match write fails 412 (out/A03_ConditionalGet.txt).

```d2
c: client (cache copy)
s: server
c -> s: GET /doc
s -> c: 200 + ETag rev-1
Cache-Control: max-age=60
c -> s: (after expiry) GET + If-None-Match: rev-1
s -> c: 304, no body -> reuse copy
c2: other client wins
c2 -> s: PUT + If-Match: rev-1
s -> c2: 412 (stale precondition)
```

**Fig. 1.** 304 is the read-side validator flow; 412 is the same validator protecting a write against lost updates.

## Designing per resource, not globally

Cacheability is a per-resource contract: a product catalog wants max-age plus stale-while-revalidate; a balance read wants no-store or private max-age=0; a report endpoint might be immutable (max-age=31536000, immutable). Authenticated APIs must set Cache-Control explicitly — absent directives on authorized responses historically leaked into shared caches, so default private and allow-list what intermediaries may keep. Anything negotiated needs Vary (Accept, Accept-Language — [[What is content negotiation in REST APIs]]). GET bodies with credentials, per-user data behind the same URI, and POST responses (cacheable only when explicit freshness and Content-Location appear) are the traps; when caching is genuinely hard — per-user aggregation in one round-trip — that is a real cost of query-shaped APIs ([[Why is HTTP caching harder with GraphQL than REST]] for the contrast; [[What is caching used for]] for the general taxonomy; [[How would you explain HTTP]] for where this sits in the protocol).

> [!warning] no-cache and no-store are opposites people swap
> no-cache stores the response but requires revalidation before reuse (usually saving bytes, not round-trips); no-store forbids storage entirely. Swapping them either leaks private data (no-cache intended as no-store) or destroys your hit rate (no-store intended as no-cache).

> [!tip] Interview answer
> I declare freshness per resource with Cache-Control — max-age for shareable data, private or no-store for per-user — and add validators: ETag for 304 revalidation on reads, and If-Match so writes fail 412 instead of clobbering concurrent updates. Negotiated responses carry Vary, authenticated APIs set explicit directives so nothing sensitive lands in shared caches. Done right, this cuts latency and load without a line of application cache code.
