<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What is the difference between a bounded context and a subdomain?

> [!abstract] Short answer
> A subdomain is a part of the business problem; a bounded context is a part of your software solution that models it. Subdomains are identified by asking what the business does and where it differentiates (core, supporting, generic); bounded contexts are drawn where a specific model and its ubiquitous language stay consistent. In an ideal greenfield design they align one-to-one - one context per subdomain - but they are different concepts, and in legacy systems several contexts often share one subdomain or a context spans parts of two.

## Problem space vs solution space

Strategic DDD runs in two spaces. The problem space is decomposed into subdomains with a canonical triage: core subdomains provide a competitive advantage and deserve the deepest modeling investment; supporting subdomains keep the business operational but do not differentiate it from competitors; generic subdomains are problems the industry already solved, to be bought or adopted rather than custom-built. The full classification is [[What are the types of subdomains in DDD]]. The solution space is your set of bounded contexts - each a deliberate boundary around one model. The classification of subdomains tells you where to invest; the bounded context tells you where a model stops.

```d2
direction: right
core: "Core subdomain\n(freight pricing)" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
sup: "Supporting subdomain\n(invoicing)" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
gen: "Generic subdomain\n(user accounts)" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
ctx1: "Bounded context:\nPricing model" {
  width: 240
  height: 70
}
ctx2: "Bounded context:\nInvoicing model" {
  width: 240
  height: 70
}
ctx3: "Bought product:\nIAM vendor" {
  width: 240
  height: 70
}
core -> ctx1: "modeled by"
sup -> ctx2: "modeled by"
gen -> ctx3: "replaced by"
```

**Fig. 1.** Subdomain type drives investment: deep custom modeling for core, modest for supporting, purchase for generic.

## Why they drift apart

In greenfield systems you draw them to coincide, and DDD literature recommends that alignment. Legacy reality rarely cooperates: one monolithic ERP covers three subdomains, so three subdomains share one context's model; or a "context" carved by an old org chart cuts across two subdomains. Refactoring moves the boundaries toward alignment, but the mapping is a decision with cost, not an axiom. This is also why you can have the same entity class in two contexts over one subdomain: the subdomain did not split, the models did ([[What is a bounded context and how do you identify one]]). The decomposition rule built on this distinction is [[How do you decompose an application by subdomain]], and the three-way classification that drives investment is [[What are the types of subdomains in DDD]].

> [!tip] Interview answer
> Subdomain is problem space: a slice of the business classified as core, supporting, or generic, which tells you how much modeling effort it deserves. Bounded context is solution space: the boundary inside which one consistent model and language live. Ideal design gives one context per subdomain, but in legacy systems the mapping drifts, and recognizing that drift is half of strategic design.
