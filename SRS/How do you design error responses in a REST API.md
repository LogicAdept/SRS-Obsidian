<!--
reps: 0
priority: 0
-->
#API/REST #SRS

# How do you design error responses in a REST API

> [!abstract] Short answer
> Pick one error envelope for the whole API, encode the outcome class in the HTTP status, and give clients a machine-readable discriminator plus a human explanation. The industry-standard shape is RFC 9457 Problem Details: application/problem+json with type, title, status, detail, and instance, extended by API-specific fields.

## The contract around failures

Errors are API surface with the longest lifetime: every client across every version will meet them, so they need the same rigor as success schemas. RFC 9457 fixes the minimal shape — type is a URI identifying the error class (the default, about:blank, defers to the status code), title is a stable one-line summary, status repeats the HTTP status, detail is a human-readable explanation, instance points at the specific occurrence — and allows extension members like validation field lists. Clients branch on type (or on a code field), never on parsing detail text, which may be localized or reworded freely. Consistency rules that matter in review: every endpoint's failure mode is documented; validation reports all offending fields in one response, not one per call; the same failure yields the same status everywhere (no 400 here, 422 there); and infrastructure errors keep the shape so client parsers never fork ([[What are the key principles of good API design]]).

```d2
c: client
gw: API
svc: business logic
c -> gw: request
gw -> svc: process
svc -> gw: reject: insufficient funds
gw -> c: 422 application/problem+json {
  box: {
    type: .../errors/insufficient-funds
    title: Insufficient funds
    status: 422
    detail: Order total 150.00 exceeds
balance 95.40
    instance: /orders/7
  }
}
c: branches on type,
never on detail text
```

**Fig. 1.** The server classifies the failure once; the problem+json body carries a machine discriminator (type) plus human detail.

```text
client: 422 CT=application/problem+json
  {
    "type": "https://api.example.com/errors/insufficient-funds",
    "title": "Insufficient funds",
    "status": 422,
    "detail": "Order total 150.00 exceeds available balance 95.40",
    "instance": "/orders/7",
    "availableBalance": 95.40
  }

client dispatches on type -> https://api.example.com/errors/insufficient-funds
```

**Listing 1.** Verified on JDK 21 (com.sun.net.httpserver): a hand-written problem+json response; the client's dispatch logic keys on type, and Spring Framework 6 ships this shape as the ProblemDetail abstraction (out/A06_ProblemDetails.txt).

## The operational half

Beyond shape, production error design covers what you must not emit and what you must add for yourself: no stack traces, class names, or internal hosts in bodies (they leak architecture and become attack reconnaissance — [[What is CORS in Spring Boot]] and the security cards cover the boundary hardening; [[How do you secure a REST API]]); a correlation/request id echoed in the body and logs so a user-reported error maps to one trace; correct class per failure (400 versus 422, 401 versus 403, 409 versus 412 — see [[Which HTTP status codes matter most in REST API design]]); and localization discipline — detail is for humans, so version it, but type and extensions are for machines and must be frozen. Deprecations of error codes are breaking changes ([[What changes are breaking for a REST API]]).

> [!warning] detail text is not an API
> Clients that substring-match error messages break the first time a wording changes or a locale appears. If behavior depends on a failure, that behavior must key on type (or an enum code), and the docs must promise its stability — otherwise you have shipped a contract you never controlled.

> [!tip] Interview answer
> I standardize on RFC 9457 problem+json: status carries the class, type is the stable machine discriminator, title and detail are for humans, and extensions carry field-level validation data. All validation fails in one response, the same failure maps to the same status everywhere, bodies never leak internals, and a correlation id ties the response to logs. Clients branch on type — never on message text.
