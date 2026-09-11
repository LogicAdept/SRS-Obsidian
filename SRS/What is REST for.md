<!--
reps: 0
priority: 0
-->
#API/REST #SRS

# What is REST for

> [!abstract] Short answer
> REST was derived to explain why the web scales, and it exists to buy specific system properties: independent evolution of components, horizontal scalability through statelessness, latency reduction through caching, and visibility for intermediaries. You reach for it when many untrusted or long-lived clients must talk to a service whose implementation you want to change freely.

## The properties, and what they cost

Fielding's dissertation evaluates REST against the needs of distributed hypermedia: low entry barrier, extensibility, distributed hypermedia spanning trust boundaries, and Internet scale. Statelessness plus the uniform interface give visibility — any intermediary can read a self-describing message and route, cache, retry, or reject it without understanding your business logic. Cacheability cuts latency and load. Layering lets you insert CDNs, gateways, and auth proxies. The price is real: the uniform interface is less efficient than a bespoke RPC contract (you cannot collapse ten fetches into one call without inventing it), statelessness repeats context on every request, and hypermedia is costly to build properly ([[Why is REST stateless]], [[What is HATEOAS]]). REST is therefore for systems where client diversity, longevity, and scale matter more than raw per-call efficiency — public APIs, web backends behind browsers and mobile apps ([[What is the difference between REST and gRPC]] shows the RPC side).

```d2
goal: REST constraint -> property
style: dashed container {
  s1: stateless {
    tooltip: no server session chain
  }
  s2: uniform interface
  s3: cacheable
  s4: layered
}
p1: horizontal scaling (any node
serves any request)
p2: visibility for
proxies/gateways
p3: latency + load cut
by reuse
p4: swap/insert components
freely
style.s1 -> p1
style.s2 -> p2
style.s3 -> p3
style.s4 -> p4
```

**Fig. 1.** Each constraint exists to produce a system-level property; the properties together are what REST is "for".

## When the properties do not fit

If the consumer set is closed, known, and versioned in lockstep with the server — service-to-service calls inside one system — the uniform interface mostly adds overhead: you end up with chatty calls, over-fetching, and hand-rolled batching. That is the niche where binary RPC styles win ([[What is the difference between GraphQL and REST]] shows the query-shaped alternative). A useful interview line: REST optimizes for ecosystem properties (evolution, cache, scale of clients), RPC optimizes for per-call properties (latency, payload, typing). Pick per boundary, not per fashion.

```text
stateless          -> any node serves any request     cost: context repeats
uniform interface  -> proxies route/inspect/retry     cost: less efficient
cacheable          -> latency + load drop             cost: invalidation care
layered            -> swap components freely          cost: indirection
```

**Listing 1.** Constraint to property to price: REST is for the properties, and the costs are the design budget (conceptual).

> [!warning] REST is not automatically the "simple" option
> The visible simplicity of `GET /users/7` hides the engineering behind it: real cacheability needs ETags and Vary discipline, real evolvability needs hypermedia or careful contract governance, and real statelessness moves state to the client (tokens, request context). A mature REST API is engineered, not free.

> [!tip] Interview answer
> REST exists to make systems scale and evolve: statelessness gives horizontal scaling and visibility, cacheability cuts latency, the uniform interface and layering let clients and intermediates evolve independently of the server. You pay with chattiness and per-request context, so it fits open, long-lived, client-diverse boundaries — public APIs and web backends — while closed internal meshes often prefer RPC.
