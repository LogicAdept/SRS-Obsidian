<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/ArchitecturalStyle #Patterns/Architecture/Monolith #SRS

# What advantages do microservices have over a monolith

> [!abstract] Short answer
> Microservices trade the monolith's single deployable for a fleet of independently developable, deployable and scalable services. The advantages are organizational and operational: independent release cadence per team, per-service scaling and technology fit, fault isolation, and small services that are easy to reason about. They are bought with distributed-systems costs — network failure modes, data consistency, operational complexity.

## Where the advantages actually come from

Each advantage follows from one structural fact: services are owned and shipped separately. Independent deployments: a team releases its service without coordinating a shared release train — the monolith's biggest practical pain, merge queues and all-hands regression. Independent scaling: the hot service gets instances; the monolith forces scaling everything together (and its hottest component caps the fleet's density). Independent technology and data fit: a service can pick the storage its access pattern needs and upgrade its stack alone. Fault isolation: a crash or memory leak in one service degrades one capability instead of the whole application. Comprehensibility: a service small enough to fit in one head onboards fast — the "product not project" framing follows from the same ownership split ([[What is the domain-specific boundary pattern in microservice design]] is how boundaries get chosen; [[How do you decompose a monolith into microservices]] is the migration path).

```d2
direction: right
mono: "Monolith
one deployable, one DB
scale: everything" {style.fill: "#eceff1"}
ms: "Microservices
fleet of deployables" {style.fill: "#e8f5e9"}
s1: "Orders
x3" {style.fill: "#e3f2fd"}
s2: "Inventory
x1" {style.fill: "#e3f2fd"}
s3: "Search
x8" {style.fill: "#e3f2fd"}
mono -> ms: split by business capability
ms -> s1
ms -> s2
ms -> s3
```

**Fig. 1.** Same business capability, different scaling axis: the search service runs eight instances, inventory one — impossible with a single deployable.

## The costs that balance the ledger

Every remote call is a network operation that can fail, time out or return a partial answer — resilience patterns ([[How would you explain Circuit Breaker]]) and consistency planning ([[What is BASE as a consistency model]]) become everyday work instead of exotic edge cases. Data consistency across services loses the single ACID umbrella: sagas and outboxes replace local transactions ([[What is a saga and how would you explain one with a real-world example]], [[How would you explain the transactional outbox pattern]]). Operations gain a fleet: service discovery, configuration, observability and deployment pipelines per service — the chassis and observability patterns exist precisely to contain this ([[What is the microservice chassis pattern]], [[What is the application metrics pattern in microservices]]). Distributed debugging replaces stack traces with trace assembly. The honest interview position: microservices are an organizational optimization first — they pay where team autonomy and independent release velocity matter more than they cost; a small team shipping a modest product usually pays more than it gains. The counterweight - when this trade does not pay - is cataloged in [[When should you not use microservices]], and the first cut of the boundaries themselves comes from [[How do you decompose an application by business capability]].

> [!tip] Interview answer
> Microservices win on team autonomy and operational flexibility: independent releases per service, per-service scaling and technology fit, fault isolation, and small comprehensible codebases. The price is distributed systems for real: network failure modes, eventual consistency, sagas instead of ACID transactions, and a fleet to observe and operate. I treat it as an organizational optimization — worth it with enough teams and release pressure, premature for a small product.
