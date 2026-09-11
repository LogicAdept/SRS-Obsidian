<!--
reps: 0
priority: 0
-->
#API/REST #SRS

# What is an API endpoint

> [!abstract] Short answer
> An endpoint is one addressable point of interaction in an HTTP API: a URI path (like /orders/7) combined with an HTTP method and the request/response contract attached to it. GET /orders/7 and DELETE /orders/7 are two endpoints sharing a URI. Endpoints are the concrete surface clients code against; the API is the whole set plus its shared rules.

## Anatomy of the surface

A full endpoint contract covers more than the path: the method (what happens), path parameters (which resource), query parameters (variants of the interaction — filters, pagination, sparse fields), request headers (Content-Type, Accept, auth, preconditions like If-Match), the request body shape, and the response: status codes with their meanings, headers (Location, ETag, RateLimit), and body schema. Frameworks expose this as route tables — Spring maps @GetMapping("/orders/{id}") to a handler; the JDK's com.sun.net.httpserver matches contexts and lets you route by method and path. The endpoint is where versioning, authorization, and rate limiting attach — most API infrastructure keys its policies on endpoint identity ([[How should you version a public API]], [[How do you design rate limiting for a REST API]]).

```d2
e: endpoint GET /orders/7 {
  uri: URI /orders/7 {
    tooltip: path param {id} selects the resource
  }
  m: method GET
  q: query params (?fields=id,status)
  h: headers (Accept, Authorization, If-Match)
  req: request body (usually none for GET)
  resp: response contract {
    r1: 200 + representation
    r2: 404 unknown id
    r3: 412 precondition failed
    r4: headers ETag, RateLimit
  }
}
e.m -> e.uri: operates on
e.resp: 200 + representation
```

**Fig. 1.** An endpoint is method plus URI plus the full request/response contract — not just the path.

## Endpoint vs resource vs operation

The URI designates the resource; the endpoint is the pair of that URI with a method and its contract. Client-side, this distinction matters for code generation and SDKs: an OpenAPI operation IS one endpoint, and tools generate one method per operation ([[What is a resource in a RESTful context]] for the URI side; [[What is OpenAPI and how does Swagger relate to it]] for describing them mechanically). Collection endpoints (POST /orders) and instance endpoints (GET /orders/7) differ in conventions: which statuses they may return (201 + Location versus 200/304/404), which idempotence guarantees apply, and how caching works. Interviewers often probe these conventions as a proxy for real design experience ([[What is REST]] for why the uniform method set makes the difference visible).

```text
POST   /api/orders        -> 201 Location=/api/orders/42 {"id":42}
POST   /api/orders        -> 400 {"error":"body required"}
GET    /api/orders/7      -> 200 {"id":7,"status":"NEW"}
GET    /api/orders/999    -> 404 {"error":"not found"}
DELETE /api/orders/7      -> 204
PUT    /api/orders/7      -> 204
GET    /api/orders        -> 405 Allow=POST   <- collection only accepts POST
```

**Listing 1.** Verified on JDK 21 (com.sun.net.httpserver): one routing table, several endpoints over two URIs; note 405 carrying Allow for the methods that would work (out/A01_EndpointBasics.txt).

> [!warning] An endpoint is not a URL string in a wiki page
> Teams ship "endpoint lists" that omit method, status semantics, or headers — then clients guess. The contract is the method + URI + schemas + status semantics together; anything less leaves behavior undefined and integration bugs inevitable.

> [!tip] Interview answer
> An endpoint is one interaction point of an HTTP API: a URI plus an HTTP method plus the request and response contract — params, headers, body schemas, and which status codes mean what. GET /orders/7 and DELETE /orders/7 are different endpoints over the same resource URI. It is the unit clients code against and the unit infrastructure policies attach to.
