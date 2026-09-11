<!--
reps: 0
priority: 0
-->
#API/Contracts #SRS

# How should you version a public API

> [!abstract] Short answer
> Version at the contract level with one scheme and a published policy: major versions in the URI (/v1/) are the pragmatic default; dated or media-type versioning serve specific needs. Treat additive changes as non-breaking, break only with a new version, and deprecate explicitly — Sunset headers, announcements, usage monitoring — before removal.

## Choosing where the version lives

URI path versioning (/v1/orders) is the default for a reason: visible in logs and browsers, trivially routed at the gateway, and unambiguous when a client holds two versions in flight. Its cost is cosmetic (a URI is opaque, so "v1 in the path is impure" is not an argument) and operational (two trees to maintain). Header-based schemes move the choice off the wire path: a custom Accept-Version header (Stripe-style, often with dated versions like 2026-06-01) or a versioned media type (application/vnd.api.v2+json) keeps URIs stable — versions become negotiation ([[What is content negotiation in REST APIs]]) — but they hide from logs, complicate browser debugging, and need client library support. The version unit is the major: within a version, changes are additive (new optional fields, new endpoints, new error types); breaking changes are new versions, full stop. Semantic versioning inside a public contract rarely helps clients — they cannot opt into minor fixes — so publish compatibility instead ([[What changes are breaking for a REST API]] for the classification; [[What are the key principles of good API design]] for consistency).

```d2
u1: /v1/users {
  flat: {"name":"Ada"}
}
u2: /v2/users {
  nested: {"profile":{"name":"Ada"}}
}
h: /users + Accept-Version {
  dflt: default -> v1 shape
  dated: 2026-06-01 -> v2 shape
}
u1 -> u2: breaking shape change
= new major
h: header versioning keeps
one URI
```

**Fig. 1.** The same breaking change as two URI trees versus one URI with a version header — both are valid; only mixing is wrong.

## The policy is the actual product

Schemes fail without policy, so publish: what counts as breaking, how long versions live (support windows measured in years for public APIs), the deprecation ladder — announce, mark responses (Sunset header with the removal date, RFC 8594; Deprecation header in drafts), watch actual usage per version (gateway metrics), remind laggards, then remove. Date-based versions (Stripe) trade "one number forever" for "your pin defines a feature snapshot" and a documented upgrade path per date. Internally, version at the boundary even for private APIs — service-to-service contracts age the same way, just faster ([[What is the difference between an API and a web service]] for boundary obligations). The gateway routes /v1 and /v2 to different deployments during overlap; the overlap window is the whole point — clients migrate on their schedule ([[What is the API gateway pattern in microservices]]).

```text
path:    GET /v1/orders        GET /v2/orders
header:  GET /orders + Accept-Version: 2026-06-01
media:   GET /orders + Accept: application/vnd.api.v2+json
policy:  additive inside a version; breaking = new version
         announce -> Sunset: <date> (RFC 8594) -> monitor usage -> remove
```

**Listing 1.** The three schemes on the wire, and the policy that actually governs them (conceptual).

> [!warning] Do not version what you have not broken
> A "v2" that is only v1 plus optional fields splits your client base, doubles testing, and signals that your compatibility policy is fear, not classification. Reserve versions for breaking changes; ship everything else in place.

> [!tip] Interview answer
> One scheme, published policy. Default is major versions in the path — visible, routable, unambiguous — with header or media-type versioning where URI stability matters more than debuggability. Within a version everything is additive; breaking changes mean a new version, never a silent flip. Deprecation is explicit: announcement, Sunset header with a date, usage monitoring per version, then removal after a real support window.
