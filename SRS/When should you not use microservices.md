<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/ArchitecturalStyle #Patterns/Architecture/Monolith #SRS

# When should you not use microservices

> [!abstract] Short answer
> Do not adopt microservices when the organization cannot cash the check they write: small team, unproven product, weak operational maturity, or domain boundaries you do not yet understand. Microservices trade local simplicity for distributed complexity - unclear operations, eventually consistent data, complex troubleshooting - and that trade pays off only with many autonomous teams and a stable enough understanding of the domain. Richardson's drawback list maps one-to-one onto these disqualifiers.

## The disqualifiers, concretely

Richardson's microservice drawbacks are the checklist. Distributed operations are complex and hard to troubleshoot: a use case that was one stack trace in a monolith becomes a chase across services, logs and queues - without strong observability (tracing, correlation) the team is slower after the migration, not faster. Some operations become inefficient: what was an in-process call is now network hops with serialization and failure modes. Transactions go from ACID to eventually consistent sagas - the business must genuinely tolerate visible intermediate states ([[What is eventual consistency]] frames the posture; [[What is a saga and how would you explain one with a real-world example]] shows what replaces rollback), and writing compensations is real engineering, not ceremony. Tight runtime coupling sneaks in and multiplies unavailability, and design-time coupling produces lockstep releases - microservices that always deploy together are a monolith with network overhead. Each drawback is survivable with maturity: platform automation, tracing culture, event-driven design skills. Each is a disqualifier when the maturity is absent.

The organizational tests are the sharpest. Team size: a two-pizza team - or five of them - shipping one product does not have a coordination problem microservices can solve; it has a modularity problem a well-structured monolith solves better. Domain understanding: decomposition requires knowing where the seams are ([[How do you decompose an application by business capability]] needs a business analysis; [[What is the difference between a bounded context and a subdomain]] needs modeling skills) - cutting services over an ununderstood domain freezes today's guesses into network walls. Operations: no Kubernetes competence, no tracing, no on-call rotation means adopting the architecture that produces distributed failures nobody can debug. Speed of change: a pre-product-market-fit startup changes its domain model weekly; each model change across service boundaries costs migrations and compatibility shims instead of a refactor.

```d2
direction: right
q1: "Many autonomous teams?" {style.fill: "#fff3e0"}
q2: "Stable domain seams?" {style.fill: "#fff3e0"}
q3: "Ops + observability maturity?" {style.fill: "#fff3e0"}
yes1: "yes" {style.fill: "#e8f5e9"}
no1: "no -> modular monolith
+ strangler exit path" {style.fill: "#ffcdd2"}
ms: "microservices justified" {style.fill: "#e8f5e9"}
q1 -> yes1
q2 -> yes1
q3 -> yes1
q1 -> no1
q2 -> no1
q3 -> no1
yes1 -> ms
```

**Fig. 1.** Three no-nonsense gates; failing any one means the monolith serves the team better today.

The balanced closing position - and the one Richardson himself takes: monolith first is a legitimate default, with a modular internal structure and a clean extraction path ([[What advantages do microservices have over a monolith]] weighs the upside; [[What is monolithic architecture and when does it make sense]] is the counter-card). The senior-sounding answer in interviews is neither dogma: name the specific maturity signals you would check before adopting, and the price you accept by adopting.

> [!warning] Resume-driven decomposition
> The most expensive failure mode is adopting microservices as a fashion statement: a small team inherits distributed transactions, partial failures and a service mesh it cannot operate - and delivers features slower than the monolith it abandoned. The second trap is the half-migration: one or two services extracted over a shared database, which adds network failure modes while keeping the data coupling - the costs of both architectures, the benefits of neither. If you cannot name the coordination pain you are solving, you are not solving it with services.

> [!tip] Interview answer
> I do not reach for microservices when a small team ships an unproven product, when the domain seams are not yet understood, or without operational maturity - tracing, automation, on-call. Microservices trade local simplicity for distributed complexity: eventual consistency, sagas, partial failures, lockstep-release risk. That trade pays with many autonomous teams and clear bounded contexts; otherwise a modular monolith with a clean strangler exit path wins.
