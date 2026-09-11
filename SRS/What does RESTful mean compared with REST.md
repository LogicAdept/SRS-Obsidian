<!--
reps: 0
priority: 0
-->
#API/REST #SRS

# What does RESTful mean compared with REST

> [!abstract] Short answer
> REST is the architectural style — the set of constraints from Fielding's dissertation. "RESTful" is the adjective applied to an API or service that conforms to those constraints in practice. So REST names the style, RESTful names a conformance claim about a concrete system.

## Degrees of conformance, not a boolean

Because the constraints are a design discipline rather than a testable standard, "RESTful" is a matter of degree, and the Richardson Maturity Model is the usual vocabulary for how far along a service is. Level 0: one URI, one verb (HTTP as tunnel — remote procedure invocation style). Level 1: individual resource URIs (nouns). Level 2: uniform HTTP verbs and status codes, plus content negotiation and caching headers. Level 3: hypermedia controls — responses advertise what you can do next (HATEOAS). Most production APIs called "RESTful" sit at level 2; level 3 is rare outside hypermedia-first projects. That is legitimate: each level adds decoupling but also complexity ([[What is HATEOAS]], [[What is a resource in a RESTful context]]).

```d2
l0: Level 0 {
  ex: POST /api (one URI,
one verb)
}
l1: Level 1 {
  ex: resource URIs
/api/orders/7
}
l2: Level 2 {
  ex: verbs + status codes
+ headers
}
l3: Level 3 {
  ex: hypermedia controls
(links in responses)
}
l0 -> l1 -> l2 -> l3: increasing
decoupling
```

**Fig. 1.** The Richardson Maturity Model: RESTfulness as levels, from HTTP-as-tunnel to hypermedia.

## Where the word earns its keep

In interviews the term is a trap-detector. "Is your API RESTful?" should be answered with the constraints you honor and the ones you consciously skip — for example: resources and verbs at level 2, JSON without hypermedia, caching via ETags, stateless tokens. That answer shows you know the style governs architecture choices, not URL cosmetics. What disqualifies an API from the adjective is not missing hypermedia alone; it is violating the base constraints — server-side sessions, verbs-in-URLs, one endpoint that tunnels everything, ignoring status codes ([[What is REST]] lists the constraints).

```text
L0  POST /api  {"op":"getUserById","id":7}   -> 200 (one URI, one verb)
L1  GET  /orders/7                           -> 200 (resource URIs)
L2  GET    /orders/7                         -> 200/404
    DELETE /orders/7                         -> 204 (uniform verbs + statuses)
L3  GET  /orders/7 -> {"links":[{"rel":"cancel",
        "href":"/orders/7/cancellation"}]}   (affordances in responses)
```

**Listing 1.** The maturity levels on the wire: tunnel, resources, uniform interface with real statuses, hypermedia (conceptual).

> [!warning] No certificate exists
> Nothing issues a "RESTful" seal: no RFC defines it, and vendors use the word loosely in marketing. Treat every claim as "level 2-ish until proven otherwise" — check for statelessness, uniform verbs, real status codes, and hypermedia before believing it.

> [!tip] Interview answer
> REST is the style — the constraints Fielding derived. RESTful is the adjective for a concrete API that follows them. Conformance is a spectrum, usually measured by the Richardson Maturity Model: resource URIs, then uniform verbs and status codes, then hypermedia. Most real-world RESTful APIs are level 2; I would name the constraints I honor and the ones I deliberately skip.
