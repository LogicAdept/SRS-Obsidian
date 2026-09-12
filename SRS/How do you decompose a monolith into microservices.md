<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/ServiceBoundaries #Methodologies/DDD #SRS

# How do you decompose a monolith into microservices

> [!abstract] Short answer
> Decomposing a monolith into microservices is the discipline of carving the deployable along business seams so each extracted service can be developed, deployed and scaled independently: pick boundaries by business capability or subdomain (DDD), extract data ownership first, strangle the routes incrementally, and keep every step reversible. Richardson's two decomposition patterns — by business capability, by subdomain — are the scoping tools; the strangler fig is the execution vehicle.

## Step 1: find the seams before cutting

Boundaries come from the business, not from technical layers. Decompose by business capability: enumerate what the organization does — catalog management, ordering, invoicing, shipping — and map capabilities to candidate services, so service ownership aligns with team ownership (Conway's law made an asset). Decompose by subdomain: within the DDD strategic design, core domain (differentiating) gets the best boundaries and attention; supporting and generic subdomains can stay coarser or even remain bought software. The two views cross-check each other ([[What is the domain-specific boundary pattern in microservice design]] covers the pattern form; [[What is the difference between a bounded context and a subdomain]] fixes the vocabulary). Practical heuristic for the first cut: start where the code changes fastest and the data has a clear owner; a seam that requires two services to commit one transaction in lock-step is a seam in the wrong place.

```d2
direction: down
mono: "Monolith
UI + logic + data in one deployable" {style.fill: "#eceff1"}
cap: "Capability map
catalog | ordering | invoicing | shipping" {style.fill: "#fff3e0"}
svc1: "Catalog service
owns catalog data" {style.fill: "#e8f5e9"}
svc2: "Ordering service
owns orders data" {style.fill: "#e8f5e9"}
svc3: "Invoicing + Shipping
later waves" {style.fill: "#f3e5f5"}
mono -> cap
cap -> svc1: wave 1
cap -> svc2: wave 1
cap -> svc3: wave 2
```

**Fig. 1.** Capability mapping produces the extraction order: clear-owner, high-change areas first; entangled domains last.

## Step 2: extract with data first, routes second, integration third

The working order per wave: give the target capability its own schema — copy or carve out the tables it owns, with the monolith accessing them through the new service's API or a synced replica during transition ([[What is the shared database pattern in microservices]] is the debt being paid down here). Move the routes: the strangler facade shifts traffic feature by feature ([[What is the strangler fig pattern and when do you use it]]). Replace in-process calls that crossed the seam with APIs, and in-process events with messages — this is where cross-service consistency work appears: sagas for multi-service invariants, outbox for atomic state-plus-event ([[What is a saga and how would you explain one with a real-world example]], [[How would you explain the transactional outbox pattern]]), and read models or composition for former JOINs ([[What is the API composition pattern in microservices]]). Ship the observability and deployment plumbing with the first wave, not after it — chassis, health checks, tracing ([[What is the microservice chassis pattern]]); retrofitting operations onto a fleet is far more expensive than bootstrapping it. The two named strategies for choosing the new boundaries are [[How do you decompose an application by business capability]] and [[How do you decompose an application by subdomain]].

> [!tip] Interview answer
> I decompose by business seams, not technical layers: map capabilities or DDD subdomains, pick boundaries where data ownership is clear and change is frequent, then extract in waves — data ownership first, strangler routing second, replacing in-process calls with APIs and events third, with sagas and outbox for the consistency the monolith got for free. Every wave is reversible and shippable; the stop condition is a boundary that can't change independently — that's a module, not a service.
