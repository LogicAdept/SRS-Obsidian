<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What are the open host service and published language patterns?

> [!abstract] Short answer
> Open host service (OHS) is an upstream team's commitment to expose its functionality as a stable, documented protocol designed for many consumers, instead of ad-hoc point-to-point integrations. Published language (PL) is the agreed interchange format that protocol speaks - a documented schema expressing the domain information, independent of any consumer's internal model. The two travel together: OHS is the door, PL is the language spoken through it.

## How the pair works

When an upstream context has many downstream consumers, per-customer negotiation stops scaling: every new consumer would pull the upstream team into bespoke work. The open host service answers by publishing one protocol - versioned, documented, tested - and treating it as a product. The published language under it expresses the domain facts in a form no consumer is forced to share internally: DTOs with a schema, an event payload format, an industry interchange standard. Consumers translate the published language into their own model at the edge; the upstream's internal model stays free to evolve as long as the published language holds. This is why OHS+PL is the natural contract form for the customer-supplier relationship at scale and the default integration style between microservices - one bounded context speaks, many listen ([[What is the domain-specific boundary pattern in microservice design]]).

Versioning is part of the deal: adding optional fields is compatibility, removing or narrowing them is a new major version with a deprecation window. The published language is a promise with a calendar attached.

```java
// Published language: upstream contract with its own field names and codes.
record UpstreamCustomerDto(String first_name, String last_name, String status_code, long credit_limit_minor) {}

// A downstream translates PL into its local model - never shares the internal model with it.
CustomerTranslator.apply(new UpstreamCustomerDto("Ada", "Lovelace", "A", 500000), local);
System.out.println(local.standing());    // TRUSTED
CustomerTranslator.apply(new UpstreamCustomerDto("Ada", "Lovelace", "P", 100000), local);
System.out.println(local.standing());    // PROBATION
```

**Listing 1.** Verified on JDK 21.0.12.1: the published language uses upstream vocabulary (`first_name`, `status_code`), and each consumer maps it to its own model - two consumers can hold two different translations of the same payload.

```d2
direction: down
ohs: "Upstream context\nopen host service" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}
pl: "Published language\nversioned interchange schema" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
d1: "Downstream A\ntranslates to its model" {
  width: 250
  height: 90
  style.fill: "#e8f5e9"
}
d2: "Downstream B\ntranslates to its model" {
  width: 250
  height: 90
  style.fill: "#e8f5e9"
}
d3: "Downstream C\nconforms, no translation" {
  width: 250
  height: 90
  style.fill: "#ffebee"
}
ohs -> pl: "speaks"
pl -> d1
pl -> d2
pl -> d3
```

**Fig. 1.** One published protocol serves many consumers; each decides whether to translate the published language into its own model or conform to it.

## When to publish

The trigger is consumer count: one known consumer justifies a negotiated contract; several consumers with independent roadmaps justify OHS+PL. The upstream pays with protocol stewardship - schema governance, version discipline, deprecation handling - and recovers it in not writing N bespoke integrations. Inside one context the pattern is overkill: an application service calling domain objects needs no published language. On the context map ([[What is context mapping in DDD]]), OHS+PL describes the upstream offer; the downstream's own choice - conform or translate - is a separate decision ([[What are customer supplier and conformist relationships in a context map]], [[What is the anti-corruption layer pattern]]).

> [!warning] The internal model is not the published language
> The tempting shortcut is exposing internal aggregates over the host service and calling it a published language. Then every internal refactor becomes a breaking change for every consumer, and the upstream model ossifies under the weight of its clients. The published language exists precisely so the internal model and the wire format can evolve separately; merging them couples every consumer to your refactors - the leak the pattern was invented to prevent.

> [!tip] Interview answer
> Open host service is the upstream commitment: one stable, documented, versioned protocol for all consumers instead of bespoke integrations. Published language is the schema that protocol speaks - a shared interchange format independent of anyone's internal model. Consumers either conform or translate it into their own model. The pair decouples many downstreams from one upstream's internal evolution.

