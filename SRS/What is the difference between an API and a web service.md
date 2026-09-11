<!--
reps: 0
priority: 0
-->
#API/REST #SRS

# What is the difference between an API and a web service

> [!abstract] Short answer
> An API is any defined surface another program can call — a library's methods, an OS's system calls, an HTTP API. A web service is a specific kind of API: one offered over the network using web protocols, historically SOAP/XML or REST/JSON. Every web service is an API; most APIs are not web services.

## The set and its subset

API is the umbrella: interface definitions that let software components interact without knowing each other's internals. That covers in-process interfaces (Java interfaces, DLL exports), platform APIs, and remote ones. A web service narrows two dimensions at once: it is remote (a network boundary, with everything that implies — partial failure, latency, serialization) and it rides web infrastructure (HTTP/HTTPS with XML or JSON payloads). The classic pre-REST web service stack was SOAP plus WSDL plus WS-* standards ([[What is SOAP]], [[What is WSDL used for]]); the REST style then won by reusing HTTP itself instead of layering a messaging protocol on top ([[How does SOAP differ from REST style web services]]). The network boundary is the practically important difference: in-process API errors are exceptions, web service calls need status codes, timeouts, idempotence, and retries ([[What is idempotency in HTTP and in messaging]]); and their contracts must be explicit because callers cannot see your source ([[What is OpenAPI and how does Swagger relate to it]] as the machine-readable contract layer).

```d2
api: API (any program surface) {
  lib: library / SDK (in-process)
  os: OS system calls
  ws: web services (over network) {
    rest: REST/HTTP + JSON
    soap: SOAP + WSDL
  }
}
api.lib: in-process calls
api.os: local calls
api.ws: remote calls ->
network semantics
```

**Fig. 1.** Web services are the remote, web-protocol-flavored subset of APIs; the API umbrella also covers in-process interfaces.

## Why interviewers draw this line

The question tests whether you model boundaries consciously. When you "expose an API" as a web service you inherit distributed-systems obligations that a library API never has: versioning across deployments you do not control, security at the boundary (authn/z on every call), rate limiting, and backward compatibility pressure measured in years. Library APIs evolve with your release train; web services must serve old clients indefinitely or negotiate version upgrades ([[What changes are breaking for a REST API]], [[What is the difference between an API and a web service]] is itself the standard opener for REST/SOAP comparisons). Answering with "REST is an API, SOAP is a web service" is the common wrong shortcut — SOAP web services are APIs too, and modern HTTP APIs are web services as well.

```text
in-process API : service.getLocalPrice(id)   -> throws PriceUnavailableException
web service API: GET /prices/42              -> 200 {"price":9.99} | 4xx/5xx + retry story
                 timeouts, idempotence, versioning, authn on every call
```

**Listing 1.** The boundary that defines a web service: same operation, but the network adds status semantics, failure modes, and contract obligations (conceptual).

> [!warning] Not every HTTP API is a "web service" in the strict sense
> Legacy literature reserves "web service" for the SOAP/WS-* stack, and some shops still mean exactly that. Clarify the sense before agreeing or disagreeing — the argument dissolves once the term's scope is fixed.

> [!tip] Interview answer
> An API is any callable surface between software — a library, an OS, or a remote service. A web service is the specific case of an API delivered over a network using web protocols: SOAP with WSDL historically, HTTP with JSON today. So every web service is an API, but a web service additionally carries distributed-systems obligations: explicit contracts, versioning, timeouts, and retries across a boundary you do not control.
