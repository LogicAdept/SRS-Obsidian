<!--
reps: 0
priority: 0
-->
#Networking/Web/Protocols/HTTP #SRS
# What are the HTTP request methods

> [!abstract] Short answer
> HTTP methods define the action a client requests on a resource (RFC 9110): GET (read, no body semantics), HEAD (GET without the body), POST (process/append — non-idempotent), PUT (replace the whole resource), DELETE (remove), PATCH (partial modification, RFC 5789), OPTIONS (what can I do here? — CORS preflight uses it), TRACE (loopback echo), CONNECT (tunnel — how HTTPS goes through proxies). The two cross-cutting properties: safe (no state change intended: GET/HEAD/OPTIONS/TRACE) and idempotent (repeating changes nothing further: GET/HEAD/PUT/DELETE/OPTIONS/TRACE — not POST, not necessarily PATCH).

## The working set

| Method | Purpose | Safe | Idempotent |
|---|---|---|---|
| GET | retrieve a representation | yes | yes |
| HEAD | like GET, headers only | yes | yes |
| POST | create in a collection, process a form, append | no | no |
| PUT | replace the target with this representation | no | yes |
| DELETE | remove the target | no | yes |
| PATCH | apply a partial change document | no | not guaranteed |
| OPTIONS | capabilities / CORS preflight | yes | yes |
| TRACE | echo the request for diagnostics | yes | yes |
| CONNECT | establish a tunnel (proxy + HTTPS) | no | no |

```d2
direction: down
root: "HTTP methods" { width: 180; height: 60; style.fill: "#e3f2fd" }
safe: "safe: GET, HEAD,\nOPTIONS, TRACE" { width: 250; height: 80; style.fill: "#e8f5e9" }
idem: "idempotent: PUT, DELETE\n(+ all safe ones)" { width: 270; height: 80; style.fill: "#fff3e0" }
nid: "neither: POST\n(uncertain: PATCH)" { width: 250; height: 80; style.fill: "#ffebee" }
root -> safe -> idem
root -> nid
```

**Fig. 1.** The property lattice — every safe method is idempotent; POST is neither; PATCH's idempotency depends on the patch document's semantics.

## The distinctions interviews actually test

- **PUT vs POST:** PUT is "put this resource here" (client chooses the URI, full replacement, idempotent); POST is "process this" (server chooses the URI, may create sub-resources, repeats create duplicates) — expanded in [[What is the difference between POST PUT and PATCH]].
- **GET vs POST:** GET's parameters live in the query string, are cacheable/bookmarkable, and must not change state; POST carries a body, is not cached by default, and performs actions — the full contrast is [[What is the difference between GET and POST]].
- **Idempotency is about repeats, not about "read-only":** DELETE is idempotent although it mutates; a second DELETE yields 404/no-op, not a second deletion ([[What is idempotency in HTTP and in messaging]] extends this to messaging).

> [!warning] Semantics are the contract — proxies and caches rely on them
> A proxy will not cache POST, a browser will prefetch GET, and DELETE is safe to retry after a timeout *because* of its declared idempotency. Breaking the contract (GETs that mutate state, "POST for everything") causes real bugs: link prefetchers firing purchases, retries duplicating orders. Also, method names are case-sensitive uppercase per spec, and custom methods (e.g. WebDAV's PROPFIND) are legal extensions — "only 9 methods exist" is technically false; RFC 9110 defines this core set.

> [!tip] Interview answer
> The core nine: GET, HEAD, POST, PUT, DELETE, PATCH, OPTIONS, TRACE, CONNECT. I organize by properties: GET/HEAD/OPTIONS/TRACE are safe; PUT/DELETE are idempotent but state-changing; POST is neither; PATCH is partial-update by RFC 5789 with no idempotency guarantee. The production angle: caches, proxies and retry logic trust these semantics, so a GET that mutates or a POST treated as retry-safe is a real bug, not a style choice.
