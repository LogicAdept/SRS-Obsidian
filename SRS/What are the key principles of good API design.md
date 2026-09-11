<!--
reps: 0
priority: 0
-->
#API/REST #SRS

# What are the key principles of good API design

> [!abstract] Short answer
> Design the contract for the client that will consume it for years: model resources, not internal objects; keep the surface small and uniform; make consistent choices (naming, errors, pagination, idempotence) once and reuse them everywhere; make it evolve safely (additive changes, versioning policy); and document the contract as a first-class artifact, not an afterthought.

## The principles behind the checklist

Consistency is the load-bearing one: an API is a language, and every ad-hoc decision (names for the same concept in different endpoints, two pagination styles, per-endpoint error shapes) taxes every client forever. Resource orientation keeps URIs as stable nouns with uniform methods and pushes state semantics into the protocol instead of bespoke verbs ([[What is a resource in a RESTful context]]). Predictability of failure and success — one error envelope, one status discipline ([[Which HTTP status codes matter most in REST API design]], [[How do you design error responses in a REST API]]) — turns clients into simple, testable code. Evolution safety means assuming yesterday's clients live for years: additive changes, deprecation with deadlines, no silent semantic flips ([[What changes are breaking for a REST API]], [[How should you version a public API]]). Consumability closes the loop: the API should be explainable in one page and testable with curl; if integration requires reading your source, the design failed ([[What is API-first design]] makes this a process instead of a hope).

```d2
consistency: one way
to do each thing
resources: stable nouns,
uniform methods
failure: predictable errors
and statuses
evolution: additive first,
deprecate with deadlines
doc: contract as artifact
(OpenAPI, examples)
good: clients that are simple,
correct, and cheap to onboard
consistency -> good
resources -> good
failure -> good
evolution -> good
doc -> good
```

**Fig. 1.** The five working principles and the property they jointly produce: cheap, correct clients.

## Principles applied, not listed

Interviewers want the trade-offs, so have the concrete applications ready: filtering, sorting, and pagination follow one parameter grammar across every collection endpoint ([[How do you design filtering and sorting for a REST API]], [[What is the difference between offset and cursor pagination]]); writes state their idempotence story — which methods are safe to retry and how clients make POST retries safe ([[How do you design idempotent REST API operations]], [[What is the Idempotency-Key header used for in HTTP APIs]]); cacheability is designed per resource, not discovered in an outage ([[How do you make REST API responses cacheable]]); long operations do not block connections ([[How do you handle long-running operations in a REST API]]). The negative test for every principle: "what happens when we add the next hundred endpoints?" — if the answer is more one-off decisions, the principles are slogans.

```text
one decision, reused everywhere:
  errors    -> RFC 9457 problem+json on every endpoint
  pagination-> cursor + Link rel=next on every collection
  idempotence-> methods by spec, keys for POST
  naming    -> plural nouns, no verbs in paths

the negative test: endpoint #101 reuses decisions 1..100
```

**Listing 1.** Consistency as a practiced rule set, plus its test: the next hundred endpoints must not create new decisions (conceptual).

> [!warning] Internal objects are not API resources
> Exposing your JPA entities one-to-one couples every client to your schema and turns each refactor into a breaking change. The API models its own resource shapes (DTOs), even when the first version looks identical — that distance is what buys evolution freedom.

> [!tip] Interview answer
> I design the API as a language for its clients: model resources rather than entities, keep the surface small and uniform, and make each decision once — one error envelope, one pagination style, one idempotence story. I assume old clients live for years, so changes are additive with explicit deprecation, and I treat the contract (OpenAPI, examples) as the deliverable. The test: adding the hundredth endpoint should reuse the first one's decisions.
