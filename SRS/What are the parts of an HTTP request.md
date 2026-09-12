<!--
reps: 0
priority: 0
-->
#Networking/Web/Protocols/HTTP #SRS
# What are the parts of an HTTP request

> [!abstract] Short answer
> An HTTP request has three parts: a start line (method, request target, version), headers (key/value metadata — Host, Content-Type, Accept, Cookie...), and an optional body (the payload). The start line and headers end with a blank line (CRLF); the body, if present, is described by the headers (Content-Length or Transfer-Encoding). Responses share the same anatomy with a status line instead of a request line.

## Anatomy with a real example

```text
POST /api/orders HTTP/1.1          <- start line: method, target, version
Host: shop.example.com             <- required in HTTP/1.1: virtual hosting
Content-Type: application/json     <- body's media type
Content-Length: 42                 <- body size
Authorization: Bearer eyJhbGci...  <- credentials
Cookie: session=7f3a               <- client state (see the HTTP session card)
Accept: application/json           <- what the client can parse

{"sku":"A-1","qty":2}              <- body (absent in GET, present in POST/PUT/PATCH)
```

**Listing 1.** Request structure: start line, header fields, blank line, body. (Header names are case-insensitive per RFC 9110.)

1. **Start line.** `method SP request-target SP HTTP-version`. The target is usually an origin-form path+query; the Host header (mandatory in HTTP/1.1) completes the address for virtual hosting ([[What is the difference between HTTP 1.1 and HTTP 2]] shows where HTTP/2 replaces this with pseudo-headers like `:authority`).
2. **Headers.** Classified by role: representation metadata (Content-Type, Content-Encoding, Content-Length), negotiation (Accept, Accept-Language), conditionals (If-None-Match — [[How do you make REST API responses cacheable]]), credentials (Authorization, Cookie), connection control ([[What is HTTP]]).
3. **Body.** Any media type; GET/HEAD/DELETE conventionally have none — a GET body has no defined semantics ([[What is the difference between GET and POST]]); POST/PUT/PATCH carry the payload ([[What is a MIME type]] names the types).

```d2
direction: down
start: "Start line\nmethod | target | version" { width: 280; height: 80; style.fill: "#e3f2fd" }
hdr: "Headers\nHost, Content-Type, Accept,\nCookie, Authorization..." { width: 300; height: 100; style.fill: "#fff3e0" }
blank: "blank line (CRLF)" { width: 220; height: 50; style.fill: "#f3e5f5" }
body: "Body (optional)\nJSON, form data, bytes" { width: 260; height: 80; style.fill: "#e8f5e9" }
start -> hdr -> blank -> body
```

**Fig. 1.** Wire order is fixed; the blank line is the delimiter between metadata and payload.

> [!warning] Where the query string lives — and the body-vs-parameter confusion
> Query parameters (`?sort=price`) are part of the *request target*, not the body — a POST can carry both query parameters and a body, and GET carries *only* the query string (practically). Also: header size limits are real (servers cap total header bytes, historically ~8–16 KB), unlike the "URL length" folklore that is actually about browser/server path+query limits. And HTTP/1.1 requires the Host header — a request without one gets 400 Bad Request on any modern server ([[What are the HTTP status code classes]] for where that code lives).

Response mirror: [[Which HTTP status codes matter most in REST API design]] and [[What is HTTP]] for the protocol's contract.

> [!tip] Interview answer
> Three parts: the start line with method, target and version; headers — metadata like Host, Content-Type, Accept, Cookie, Authorization; and an optional body sized by Content-Length or chunked. The nuance I add: query parameters belong to the target, not the body — a POST may have both; GET bodies have no defined semantics; and HTTP/1.1 makes Host mandatory, which is what virtual hosting runs on.
