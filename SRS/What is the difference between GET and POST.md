<!--
reps: 0
priority: 0
-->
#Networking/Web/Protocols/HTTP #SRS
# What is the difference between GET and POST

> [!abstract] Short answer
> GET retrieves a resource: parameters travel in the query string, the request has no meaningful body, it is safe and idempotent, cacheable and bookmarkable. POST sends data for the server to *process* — a body with any content, not safe, not idempotent, not cached by default: repeats can create duplicates. Choosing wrong is not a style issue — caches, retries, logs and browser behavior all key off the method's semantics.

## Side by side

| Aspect | GET | POST |
|---|---|---|
| Purpose | read a representation | submit data for processing / create |
| Parameters | URI query string (length-limited in practice) | request body (any MIME type) |
| Safe / idempotent | yes / yes | no / no |
| Cacheable | yes (with validators) | by default no |
| Bookmark/history | yes (URL contains state) | no (re-submit warnings on refresh) |
| Visible in | URL, server access logs, proxy logs | body (HTTPS-protected) |
| Retrying after timeout | harmless | dangerous — may double-submit ([[What is idempotency in HTTP and in messaging]]) |

```d2
direction: right
q: "Intent?\nread vs process" { width: 240; height: 80; style.fill: "#e8f5e9" }
g: "GET /items?sort=price\nquery string, cacheable" { width: 290; height: 90; style.fill: "#e3f2fd" }
p: "POST /orders\nbody: JSON, side effects" { width: 270; height: 90; style.fill: "#fff3e0" }
q -> g
q -> p
```

**Fig. 1.** The intent split drives every consequence: reads are repeatable, processes are not.

## Consequences worth naming

- **Caching and CDNs:** GET responses can be stored and revalidated ([[How do you make REST API responses cacheable]]); POST responses generally bypass shared caches (except explicit `Cache-Control` with 303/307 redirect patterns).
- **Logging/privacy:** URLs with query strings end up in access logs and browser history — tokens in GET parameters leak routinely; POST bodies do not appear in logs (but are still plaintext without HTTPS — [[What is the difference between HTTP and HTTPS]]).
- **URL length limits:** practical browser/server caps (~2 KB to 8 KB) hit long GET parameter lists — that is a convention/implementation limit, not an RFC one ([[What are the parts of an HTTP request]] for where the query string lives).
- **REST mapping:** GET reads collections/items; POST creates in a collection or runs an action endpoint ([[Which HTTP status codes matter most in REST API design]] for the matching response codes).

> [!warning] "GET cannot have a body" — the RFC nuance
> RFC 9110 says a GET request body has *no defined semantics*; servers may ignore or reject it — which is exactly why sending one is wrong in practice, but the absolutist claim "GET bodies are forbidden" fails a precise interviewer ([[Can a GET request include a body]] is the dedicated drill). And the classic security misuse: state changes on GET (delete via link) get triggered by prefetchers, crawlers and CSRF — actions always go through POST/PUT/DELETE with CSRF protection.

> [!tip] Interview answer
> GET is the safe, idempotent read: parameters in the query string, cacheable, bookmarkable, retryable. POST is processing: data in the body, side effects, no caching, repeats duplicate. The consequences I cite: retries are safe on GET and dangerous on POST, query strings leak into logs, and practical URL length caps push big payloads to POST — while remembering that per RFC 9110 a GET body is undefined-semantics, not forbidden.
