<!--
reps: 0
priority: 0
-->
#API/REST #SRS

# What is REST

> [!abstract] Short answer
> REST (Representational State Transfer) is an architectural style for networked hypermedia systems, defined by Roy Fielding's dissertation (2000) as a set of constraints: client-server, stateless, cacheable, uniform interface, layered system, and optional code-on-demand. It is not a protocol and not a standard — HTTP APIs that follow these constraints are called RESTful.

## The constraints do the work

Each constraint is a deliberate trade: it gives up something local to gain a system-level property. Client-server separates UI concerns from data storage so each evolves independently. Stateless means every request carries everything needed to serve it — no server-side session chain. Cacheability lets clients and intermediates reuse responses. The uniform interface (identification of resources, manipulation through representations, self-descriptive messages, hypermedia) is the most distinctive and most often violated constraint: it trades efficiency for visibility and generality. Layered systems allow proxies, gateways, and load balancers to sit between client and server invisibly. Code-on-demand (applets, JS) is optional. Together they explain why the web scaled: any component can be swapped, cached, or repeated ([[Why is REST stateless]], [[What is HATEOAS]]).

```d2
v1: client {
  shape: person
}
v2: API layer {
  lb: load balancer (layered)
  proxy: cache/proxy (cacheable)
  api: REST server (stateless)
}
v1 -> v2.lb: request carries
all context (stateless)
v2.lb -> v2.proxy
v2.proxy -> v2.api
v2.api: {
  r: resource /orders/7 {
    shape: document
  }
}
v2.proxy -> v2.api.r: representation
(JSON, self-descriptive)
```

**Fig. 1.** A REST interaction: a stateless request flows through layers to a resource; the response is a self-describing representation.

## Style versus protocol

REST never fixes a wire format. HTTP happens to be the protocol whose verbs, status codes, headers, and caching model line up with the constraints, which is why "REST API" colloquially means "HTTP API done in this style" ([[What is the relationship between HTTP and REST]]). But REST describes the architecture, not the transport — the same style guided early hypermedia systems that predate HTTP. This also means the phrase "REST protocol" is wrong: no document specifies REST the way a document specifies SOAP or gRPC. When an interviewer asks what REST adds over HTTP, the answer is the constraints — HTTP alone does not force statelessness or a uniform interface.

> [!warning] "We use HTTP, therefore we are REST"
> Routing every call through `POST /getUserById` with a JSON body is HTTP RPC, not REST — no uniform interface, no hypermedia, usually no cacheability. Real conformance is judged against the constraints, and most production "REST APIs" implement a pragmatic subset (often Richardson maturity level 2, missing hypermedia). Do not claim purity; claim the properties you actually use ([[What does RESTful mean compared with REST]]).

```text
POST /api/getUser  {"id": 7}          <- HTTP RPC (verb in URL, one method)
GET  /api/users/7                      <- REST: resource URI + uniform method
PUT  /api/users/7  {"name": "Ada"}   <- representation replaces state
```

**Listing 1.** Verified on JDK 21 (com.sun.net.httpserver): both forms run on HTTP, but only the second treats the URI as a resource with uniform manipulation semantics (out/A01_EndpointBasics.txt).

> [!tip] Interview answer
> REST is Fielding's architectural style: a set of constraints — client-server, stateless, cacheable, uniform interface, layered system, optional code-on-demand — that make distributed hypermedia systems scalable and evolvable. It is a style, not a protocol; HTTP is just the most natural carrier. A "RESTful" API names resources with URIs and manipulates their representations through a uniform interface, instead of exposing per-operation endpoints.
