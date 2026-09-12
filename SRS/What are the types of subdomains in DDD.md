<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What are the types of subdomains in DDD?

> [!abstract] Short answer
> DDD splits a business into three kinds of subdomains. A core subdomain is what makes the company money differently than its competitors - it deserves the deepest modeling and the best people. A supporting subdomain is needed for the business to run but does not differentiate it. A generic subdomain is a solved problem - identity, billing, mailing - where buying a product beats building. The classification exists to decide where modeling effort goes, not to describe org structure.

## How the classification works

A subdomain is a slice of the business domain - what the company does, not how software represents it. The sorting question for each slice is: if we did this worse than our competitors, would the company lose anything? If yes, it is core. If it must exist but nobody wins business by doing it well, it is supporting. If the whole industry does it the same way and vendors sell it as a product, it is generic. A drone delivery company would land shipping and drone fleet management in core, invoicing and returns in supporting, and user accounts or call center tooling in generic.

Each type implies an investment strategy. Core subdomains get the senior engineers, the deep model, iterative refinement, and the bulk of design attention - this is where [[What is domain driven design]] pays for itself. Supporting subdomains get just enough model to serve the core; building them extravagantly is a classic over-investment. Generic subdomains argue for buying or adopting: the less code you own there, the more attention your core gets. A card that captures this mapping in runnable form is a one-line switch from classification to strategy.

```java
enum SubdomainType { CORE, SUPPORTING, GENERIC }

static String strategy(SubdomainType type) {
    return switch (type) {
        case CORE       -> "build with the best team, deep model, protect it";
        case SUPPORTING -> "build minimally, accept a lighter model";
        case GENERIC    -> "buy or adopt an off-the-shelf solution";
    };
}
```

**Listing 1.** Verified on JDK 21.0.12.1: the classification maps directly to an investment decision - the `CORE` branch builds, the `GENERIC` branch buys.

```d2
direction: right
core: "Core subdomain\ncompetitive advantage" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
supporting: "Supporting subdomain\nrequired, not differentiating" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
generic: "Generic subdomain\nsolved problem" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
deep: "deep model,\ntop team" {
  width: 150
  height: 70
  style.fill: "#e8f5e9"
}
light: "lightweight\nmodel" {
  width: 150
  height: 70
  style.fill: "#fff3e0"
}
buy: "buy or adopt\na product" {
  width: 150
  height: 70
  style.fill: "#e3f2fd"
}
core -> deep
supporting -> light
generic -> buy
```

**Fig. 1.** Subdomain type drives investment: the three types sit at different distances from the money, so they deserve different treatment.

## Subdomains vs bounded contexts

The classification is an input to boundary drawing, not the boundary itself. Subdomains live in the problem space; bounded contexts live in the solution space where a concrete model holds. Ideally one context models one subdomain, but real systems start with legacy contexts that span several, and the mismatch is where design pain concentrates. The interplay between the two is unpacked in [[What is the difference between a bounded context and a subdomain]], and the discovery procedure for the contexts themselves in [[What is a bounded context and how do you identify one]]. When the same drift shows up in microservice design, [[How do you decompose an application by subdomain]] reuses exactly this vocabulary.

> [!warning] Misclassification cuts
> Teams habitually label their own area "core", which inflates the modeling budget everywhere and starves nothing. The honest test is competitive: would doing this worse than competitors cost the company? The reverse error is deadlier - misclassifying a real core subdomain as generic and outsourcing it hands the differentiating knowledge to a vendor. Review the classification when strategy shifts: yesterday's supporting function, say delivery scheduling, can become today's core.

> [!tip] Interview answer
> There are three subdomain types: core - the competitive advantage, supporting - necessary but not differentiating, generic - a solved problem you can buy. The point is resource allocation: deep modeling for core, light models for supporting, and off-the-shelf solutions for generic. Subdomains are problem-space; bounded contexts are the solution-space models that implement them.

