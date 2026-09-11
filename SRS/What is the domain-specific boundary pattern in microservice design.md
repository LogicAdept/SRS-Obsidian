<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What is the domain-specific boundary pattern in microservice design?

> [!abstract] Short answer
> It is the practice of drawing microservice boundaries along domain boundaries - one service per bounded context, each owning its model, its data, and its own ubiquitous language - instead of along technical layers. Microsoft's DDD guidance compresses it to a slogan: "DDD is about boundaries and so are microservices." The service boundary is where a model stops, so data and behavior for one business capability live together, and everything outside is reached through contracts and translation.

## How it works

Strategic DDD first splits the business into bounded contexts ([[What is a bounded context and how do you identify one]]); the pattern then deploys each context - or a deliberate group of contexts - as a service. Inside, the service keeps the full vertical slice: its API, its domain model, its database. No shared enterprise schema, no common `Customer` table across services: other services hold local, slim copies or IDs and translate at the edge. Microsoft's guidance adds the sizing rule - keep boundaries "relatively small", around things that need cohesion, and stop splitting when communication between contexts starts to grow chatty - and the autonomy test: a service that must call another to answer any request "is not truly autonomous".

```d2
direction: right
wrong: "Technical layers" {
  width: 250
  height: 90
  style.fill: "#fde8e8"
}
right: "Domain boundaries" {
  width: 250
  height: 90
  style.fill: "#e8f5e9"
}
w1: "UI svc | Logic svc | Data svc\n(one team per layer)" {
  width: 260
  height: 70
}
r1: "Shipping svc | Billing svc | Identity svc\n(one context each, own DB)" {
  width: 280
  height: 70
}
wrong -> w1
right -> r1
```

**Fig. 1.** Layer-sliced services force every feature change through several teams; domain-sliced services localize a capability - model, data, deployment - in one place.

## Consequences worth naming

Good: independent deploy and scaling per capability; a change to billing rules touches billing only; per-context technology fits (a search-shaped context may pick a different store); teams own a business slice end to end. Cost: cross-context workflows become explicit integrations - events, outbox, sagas - instead of one ACID transaction, and consistency turns eventual, which is the real price of the pattern. The anti-patterns it prevents are the shared-database monolith-in-disguise and the distributed layer cake ([[What is microservices]], [[What advantages do microservices have over a monolith]]).

> [!warning] "One service per subdomain" is not automatic
> The service deploys the bounded context, and contexts align with subdomains only if someone did the strategic work; legacy systems inherit mismatches. The second failure is copying the pattern without the modeling: a "domain" service whose classes are data bags with a shared database across services gives you distribution costs and none of the cohesion - the boundary pattern without DDD is just partitioning ([[What is layered architecture]]).

> [!tip] Interview answer
> The pattern is: service boundaries follow domain boundaries. Each bounded context becomes a service that owns its model, its language, and its database; other contexts integrate through contracts and translation, never through shared tables. It buys cohesion and independent deployment, and it costs you distributed workflows - so I pair it with events and outbox patterns instead of cross-service transactions.
