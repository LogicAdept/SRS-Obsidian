<!--
reps: 0
priority: 0
-->
#API/REST #SRS

# Can a GET request include a body

> [!abstract] Short answer
> The protocol does not forbid it, but gives the body no semantics: a GET request body has no generally defined meaning, servers are not required to read it, and clients should not generate one. If the query does not fit the URI, the standard answers are query parameters or a POST search endpoint — not a GET body.

## What the spec actually says

RFC 9110's method definitions for GET say a client should not generate content in a GET request, and content received in one has no generally defined semantics; a server that cannot use it may reject it with an error (4xx) or ignore it — both are compliant. The method's contract is about the target resource's state, addressed by the request target; the body simply has no defined role in that contract. The practical consequence is exactly the spec's indifference: intermediaries and implementations disagree. Some stacks pass the body through; some proxies and caches drop or reject it; some client libraries refuse to build the request at all. java.net.http.HttpClient lets you construct one (method("GET", publisher)) and the JDK server can read it — that is per-implementation tolerance, not a portable contract ([[What is the relationship between HTTP and REST]]: self-descriptive messages cannot carry un-defined parts).

```text
server GET /search: body=12 bytes, ignored
client GET-with-body: 200 {"hits":[1,2,3]}
server PATCH /docs/7 -> 200
client PATCH: 200 {"title":"v2","tags":["a","b"]}
```

**Listing 1.** Verified on JDK 21 (com.sun.net.httpserver + java.net.http): HttpClient builds the GET-with-body, the server reads 12 bytes and ignores them — legal, but only because this particular server chose to tolerate it (out/A14_GetBodyAndPatch.txt).

## The design answers that keep you portable

Large or sensitive query state should not ride the URL anyway (length limits, logging, leakage into referrers), so the standard solutions: split the query into indexed parameters that fit ([[How do you design filtering and sorting for a REST API]]); use POST /search with a request body when the filter set is genuinely large — accepting the documented cost (not cacheable, not idempotent by default, needs its own idempotency story for retries); or model the query itself as a resource — POST a query document, then GET the result URI, which restores cacheability. The same indifference explains why GET with a body is not a security guarantee either way: anything in it may be logged or stripped unpredictably, so it is neither a secret channel nor a reliable input ([[What is the difference between GET and POST]] covers the sibling comparison — and the answer there is about semantics, not body transport). PATCH's arrival via a custom method in the same demo underlines the boundary: method semantics are fixed by the registry, bodies are not ([[How do you design idempotent REST API operations]] for the retry side).

```d2
c: client
p: proxy / CDN on the path
s: server
c -> p: GET /search + body
p: may forward, strip,
or reject the body
p -> s: body may arrive... or not
s: no defined semantics:
use, ignore, or 4xx
s -> c: 200 (this server ignored it)
```

**Fig. 1.** Nobody on the path is obliged to treat the body as meaningful — which is why a design must not depend on it.

> [!warning] "It works on my stack" is not a contract
> A GET body that survives your dev proxy may be stripped by a corporate middlebox, a CDN, or the next framework upgrade — silently changing the request from "filtered search" to "unfiltered listing". Design as if the body will be dropped, because some compliant component will drop it.

> [!tip] Interview answer
> It is tolerated, not defined: the spec says a client should not generate content in a GET and gives it no semantics, so servers may ignore or reject it and intermediaries may strip it. I never build a feature on it — small queries go in query parameters, large ones go to a POST search endpoint or become a stored query resource. The demo shows HttpClient can even build such a request; that is implementation tolerance, not a contract.
