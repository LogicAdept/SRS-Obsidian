<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What is context mapping in DDD?

> [!abstract] Short answer
> A context map is the working document that says how bounded contexts relate: for every pair of contexts that integrate, it names who is upstream and who is downstream and which relationship pattern governs the exchange. The pattern set covers nine named relationships - partnership, shared kernel, customer-supplier, conformist, anti-corruption layer, open host service, published language, separate ways, big ball of mud. Mapping is what turns a set of models into a system plan.

## What actually gets mapped

Two contexts are not "just connected" - they are connected under a contract with an owner, a translation cost, and a release discipline. The map records that contract. An upstream context produces a model that downstream contexts consume; the interesting decision is how much each side bends. If both teams negotiate jointly, that is partnership or customer-supplier. If the downstream simply adopts the upstream's vocabulary, that is conformist. If the downstream deliberately translates to protect its own model, that is an anti-corruption layer. If the upstream offers a stable protocol described in a shared format, that is open host service plus published language. If a subset of the model is genuinely owned together, that is a shared kernel. Each choice has a different ongoing cost, and the map's job is to make those costs visible and named. The individual agreements are covered in [[What is the shared kernel pattern in DDD context mapping]], [[What are customer supplier and conformist relationships in a context map]], and [[What are the open host service and published language patterns]].

```d2
direction: right
up: "Upstream context\nproduces the model" {
  width: 250
  height: 90
  style.fill: "#e3f2fd"
}
down: "Downstream context\nconsumes and translates" {
  width: 250
  height: 90
  style.fill: "#e8f5e9"
}
up -> down: "relationship pattern:\nnegotiate / conform / translate"
kernel: "Shared kernel:\na subset owned jointly" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
up -> kernel: "owns half"
kernel -> down: "owns half"
acl: "Anti-corruption layer:\ntranslation at the edge" {
  width: 240
  height: 80
  style.fill: "#ffebee"
}
down -> acl: "protects model"
```

**Fig. 1.** A context map records, for each pair of contexts, the relationship pattern - who owns the model, where translation happens, and which subset is shared.

## Why the map matters more with scale

With two contexts the map is a conversation; with twenty it is the only place where the true system shape lives. Integration decisions made silently by whoever wrote the first client tend to ossify: a temporary consumer of a legacy system's JSON becomes a decade-long dependency, and nobody remembers the model was supposed to be translated. Naming the pattern per integration makes the review question mechanical: "this integration is conformist - did we decide that, or did it just happen?" The same discipline underlies microservice integration, where the bounded context is the service boundary and the map becomes the inter-service contract overview ([[What is the domain-specific boundary pattern in microservice design]]). When two contexts have nothing to say to each other, the map should say that too - separate ways is a decision, not an oversight.

The translation side is not hypothetical: when integration crosses a model boundary, someone writes the translator, and its output is tested like any other code.

```java
// Upstream published contract -> local model (anti-corruption flavor).
CustomerTranslator.apply(new UpstreamCustomerDto("Ada", "Lovelace", "A", 500000), local);
System.out.println(local.standing());    // TRUSTED
CustomerTranslator.apply(new UpstreamCustomerDto("Ada", "Lovelace", "Z", 0), local);
System.out.println(local.standing());    // BLOCKED  - unknown upstream codes fail closed
```

**Listing 1.** Verified on JDK 21.0.12.1: the translator keeps upstream codes out of the local model - an unknown code becomes `BLOCKED` instead of leaking through.

> [!warning] The map rots silently
> Context maps decay faster than models, because integration points change whenever either side ships. A map drawn once at architecture kickoff is fiction within months. The map survives only if every integration change updates the corresponding relationship - ideally in the same pull request that changes the contract.

> [!tip] Interview answer
> Context mapping is the DDD tool for relationships between bounded contexts: each integration gets a named pattern - partnership, shared kernel, customer-supplier, conformist, anti-corruption layer, open host service, published language, separate ways, or big ball of mud. The pattern states who leads, where translation happens, and what coupling you accepted. It turns implicit integration habits into explicit, reviewable decisions.

