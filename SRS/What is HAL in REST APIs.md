<!--
reps: 0
priority: 0
-->
#API/REST #SRS

# What is HAL in REST APIs

> [!abstract] Short answer
> HAL (Hypertext Application Language) is a lightweight media type (application/hal+json, draft-kelly-json-hal) that gives hypermedia responses a standard envelope: _links for navigation and affordances, _embedded for included related resources. It fixes the shape of links so generic HAL clients and browsers (via HAL Explorer) can drive any HAL API.

## The two reserved members

HAL defines exactly two reserved keys and leaves the rest of the document to your domain data. _links is an object keyed by relation name: rel -> {href}, with rel being self, a registered IANA relation (curies for namespacing custom rels), or your own namespaced relation; href is the only mandatory member, and extra members (title, type, templated, deprecation) annotate the link. _embedded nests related resources by rel, turning a flat JSON into a navigable document — the order embeds its lines while still linking the full collection. The result: a generic client needs only HAL parsing to follow any HAL API, which is the entire point — the link format stops being an API-specific convention ([[What is HATEOAS]] for the underlying constraint; [[What is the relationship between HTTP and REST]] for why self-describing representations matter).

```json
{
  "orderId": 7,
  "status": "NEW",
  "_links": {
    "self": {"href": "/orders/7"},
    "curies": [{"name": "shop", "href": "/rels/{rel}", "templated": true}],
    "shop:cancel": {"href": "/orders/7/cancellation", "title": "Cancel this order"}
  },
  "_embedded": {
    "shop:lines": [
      {"sku": "BOOK-1", "qty": 2, "_links": {"self": {"href": "/orders/7/lines/1"}}}
    ]
  }
}
```

**Listing 1.** A HAL document: domain fields at the top level, navigation in _links, related resources in _embedded, custom rels namespaced through curies (conceptual, per draft-kelly-json-hal).

```d2
doc: HAL representation /orders/7
doc.data: orderId, status (domain data)
doc.links: _links {
  l1: self -> /orders/7
  l2: curies -> /rels/{rel}
  l3: shop:cancel -> /cancellation
}
doc.emb: _embedded {
  e1: shop:lines -> line 1
(with own _links.self)
}
doc.links.l1: navigation
doc.links.l3: affordance
doc.emb.e1: inclusion
```

**Fig. 1.** Three jobs in one envelope: domain payload, links for navigation and affordances, embedded resources for inclusion.

## Where HAL sits in the ecosystem

HAL is the pragmatic middle of hypermedia: standard enough for generic tooling (Spring HATEOAS emits HAL by default — RepresentationModel with add(link(...)); HAL Browser renders any HAL API), light enough to keep payloads readable, unlike richer formats (Siren, Collection+JSON) that model forms and actions more fully, or plain JSON:API with its own conventions. Spring Data REST exposes repositories as HAL documents out of the box ([[What is Spring Data REST]] shows the ready-made stack). The costs to name: reserved-member discipline (your field named _links collides), the curies indirection that custom rels require, and the evergreen question of whether generic clients fit your frontend's needs ([[What are the key principles of good API design]] — adopt a media type for its tooling, not for fashion). HAL's own status: a draft that never became an RFC, but stable and ubiquitous in the JVM ecosystem.

> [!warning] HAL constrains your field names
> _links and _embedded are reserved in every object, including nested ones and arrays inside _embedded. Accidentally reusing them as domain keys breaks generic clients — namespace or validate before it ships.

> [!tip] Interview answer
> HAL is a minimal hypermedia media type: application/hal+json with two reserved members — _links mapping relation names to hrefs, and _embedded holding related resources. Custom relations get namespaced via curies. It standardizes link shape so generic clients and explorers can drive any HAL API; Spring HATEOAS and Spring Data REST emit it by default. I would pick it when I want real hypermedia without a heavy format.
