<!--
reps: 0
priority: 0
-->
#Networking/Web/Protocols/HTTP #SRS
# What are the HTTP status code classes

> [!abstract] Short answer
> The status line's three-digit code is grouped by its first digit (RFC 9110): 1xx informational, 2xx success, 3xx redirection, 4xx client error, 5xx server error. The class tells the *kind* of outcome — clients and proxies act on the class (retry, follow, cache, fail), while the specific code refines it.

## The five classes with their load-bearing members

| Class | Meaning | Codes you must know |
|---|---|---|
| 1xx Informational | interim — keep waiting / protocol talk | 100 Continue, 101 Switching Protocols (WebSocket upgrade) |
| 2xx Success | the request was received, understood, acted on | 200 OK, 201 Created (+Location), 202 Accepted, 204 No Content |
| 3xx Redirection | further action needed (usually another URI) | 301/308 permanent, 302/307 temporary, 304 Not Modified (cache validator hit) |
| 4xx Client error | the request is at fault | 400 Bad Request, 401 Unauthorized (auth missing/invalid), 403 Forbidden, 404 Not Found, 409 Conflict, 410 Gone, 415 Unsupported Media Type, 422 Unprocessable Content, 429 Too Many Requests |
| 5xx Server error | the server failed handling a valid request | 500 Internal Server Error, 501 Not Implemented, 502 Bad Gateway, 503 Service Unavailable (+Retry-After), 504 Gateway Timeout |

```d2
direction: right
req: "Request processed" { width: 200; height: 60; style.fill: "#e3f2fd" }
cls: "First digit = class\n1 keep going | 2 done | 3 go elsewhere\n4 your fault | 5 my fault" { width: 360; height: 100; style.fill: "#fff3e0" }
act: "Client/proxy behavior:\nretry (1xx), use (2xx), follow/validate (3xx),\nfix request (4xx), back off (5xx)" { width: 400; height: 110; style.fill: "#e8f5e9" }
req -> cls -> act
```

**Fig. 1.** The class is the instruction; the code is the detail. Proxies and browsers mostly read the class.

## The distinctions interviews test

- **301/308 vs 302/307:** the 30x "x8" pair preserves the HTTP method and body on redirect; 301/302 historically let clients switch POST→GET (the de-facto behavior the spec regularized).
- **401 vs 403:** 401 = "authenticate first" (WWW-Authenticate present); 403 = "authenticated, but not allowed — and re-authenticating will not help."
- **404 vs 410 vs 403-as-privacy:** 404 = not found (existence may be hidden); 410 = gone permanently; hiding 403 behind 404 is a deliberate choice.
- **400 vs 422:** malformed syntax vs syntactically-valid-but-unprocessable content.
- **500 vs 502 vs 504:** own failure vs upstream returned garbage vs upstream timed out — the reverse-proxy trio ([[What is a web server]]).

> [!warning] Codes are a public contract with caches, browsers and retry logic
> 301 is cached aggressively by browsers — a wrong permanent redirect haunts users after the fix (308 exists to be method-preserving and cacheable deliberately). 429 without Retry-After and 503 without it starve well-behaved clients; a 200 body carrying {"error": ...} breaks every intermediary that only sees the class — the REST-relevant list with rationale is in [[Which HTTP status codes matter most in REST API design]]. And the classic lie: "404 means the resource never existed" — it deliberately means "not found *here, now*", which is why 410 exists.

Semantics context: [[What is HTTP]], [[What is idempotency in HTTP and in messaging]] for which classes are retry-safe.

> [!tip] Interview answer
> Five classes by the first digit: 1xx informational (100, 101), 2xx success (200, 201+Location, 204), 3xx redirection (301/308 permanent method-preserving variants, 302/307 temporary, 304 cache hit), 4xx client error (400/401/403/404/409/429), 5xx server error (500/502/503/504). The nuance I lead with: intermediaries act on the class — that is why 301's aggressive caching and 200-with-error-body are real production bugs.
