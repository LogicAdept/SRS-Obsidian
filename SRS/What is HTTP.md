<!--
reps: 0
priority: 0
-->
#Networking/Web/Protocols/HTTP #SRS
# What is HTTP

> [!abstract] Short answer
> HTTP (HyperText Transfer Protocol, now specified by RFC 9110/9112 for versions 1.x) is the application protocol of the web: a stateless, text-based (in 1.x) client-server protocol where a client sends a request — method, target, headers, optional body — and a server returns a response — status code, headers, optional body. It is resource-oriented: everything is addressed by a URI, and caching, content negotiation and method semantics are part of the protocol itself.

## The request/response shape

```text
GET /search?q=http HTTP/1.1
Host: example.com
Accept: text/html
User-Agent: curl/8.5

HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 1256
Cache-Control: max-age=60

<!doctype html>...
```

**Listing 1.** A minimal exchange: start line, headers, blank line, optional body — that structure is the whole of HTTP/1.x's on-the-wire shape.

Core properties:

1. **Client-server and stateless.** Each request is self-contained; the server owes the client no memory between requests — sessions are layered on top ([[What is an HTTP session]]).
2. **Resource-oriented.** Methods act on resources identified by URIs: GET reads, PUT replaces, POST processes, DELETE removes ([[What are the HTTP request methods]]).
3. **Self-describing payloads.** MIME types (Content-Type), encodings (Content-Encoding), languages, and content negotiation let one resource serve many representations ([[What is a MIME type]]).
4. **Caching built in.** Cache-Control/Expires, ETag/If-None-Match, validators — caches live in browsers, proxies, CDNs ([[How do you make REST API responses cacheable]]).
5. **Extensible transport story.** HTTP/1.1 (RFC 9112) added keep-alive and chunked transfer; HTTP/2 re-encodes the same semantics into binary multiplexed frames; HTTP/3 moves the transport to QUIC ([[What is the difference between HTTP 1.1 and HTTP 2]], [[What is HTTP 3 and why does it use QUIC]]).

> [!warning] HTTP is not "the web protocol with GET and POST only", and 80/443 are conventions
> The method set and their semantics are richer ([[Which common HTTP methods are not idempotent]]), and ports 80/443 are just defaults — an HTTP server can run on any port, and HTTPS is the *same* HTTP inside a TLS tunnel ([[What is the difference between HTTP and HTTPS]]). Another persistent confusion: "HTTP is TCP-only" — HTTP/3 runs over QUIC/UDP; the semantics (RFC 9110) are transport-independent, only the mapping differs.

Where it sits: [[What is the TCP IP protocol suite]] (application layer), [[What is the World Wide Web]] (the service it carries), [[What happens when you type a URL into a browser and press Enter]] (the full journey).

> [!tip] Interview answer
> HTTP is the web's stateless client-server, resource-oriented protocol: requests with method/target/headers/body, responses with status/headers/body, payloads self-described by MIME types, caching and negotiation built into the spec. Versions share those semantics — 1.1 text with keep-alive, 2 binary multiplexing, 3 over QUIC. The line that shows depth: statelessness is a feature — it is why HTTP scales horizontally, with sessions layered above as application state.
