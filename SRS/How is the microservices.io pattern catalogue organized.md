<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices #SRS

# How is the microservices.io pattern catalogue organized

> [!abstract] Short answer
> The microservices.io catalogue — Chris Richardson's pattern language — organizes roughly fifty patterns into fifteen categories, each answering one recurring architecture question: how to decompose, how to keep data consistent, how to communicate, deploy, test, observe. This deck mirrors the taxonomy one-to-one: every card carries its category as a leaf tag under #Patterns/Architecture/Microservices.

## The fifteen categories and their questions

**Architectural style** asks which style to choose at all: [[What is monolithic architecture and when does it make sense]] versus [[What is microservices]], trade-offs in [[What advantages do microservices have over a monolith]] and the counter-case in [[When should you not use microservices]].

**Service boundaries** asks how to split into services: [[How do you decompose an application by business capability]], [[How do you decompose an application by subdomain]], the [[What is the self-contained service pattern]], [[What is the service per team pattern]]; applied version — [[How do you decompose a monolith into microservices]].

**Service collaboration** asks how services stay consistent and answer queries without a shared store: [[How would you explain the database per service pattern]] versus [[What is the shared database pattern in microservices]], consistency via [[What is a saga and how would you explain one with a real-world example]] and [[Why is two-phase commit a poor fit for microservices]], command-path reads via [[What is the command-side replica pattern]], queries via [[What is the API composition pattern in microservices]] and [[What is CQRS]], fed by [[What is the domain event pattern in microservices]] and [[How would you explain the event sourcing pattern]]; ownership shaped by [[How do aggregates shape data ownership between services]].

**Transactional messaging** asks how to publish a message inside an ACID transaction: [[How would you explain the transactional outbox pattern]], [[How would you explain transaction log tailing for integration]], [[What is the polling publisher pattern]].

**Communication styles** asks which mechanism services use: [[What is the remote procedure invocation pattern between microservices]], [[What is the messaging communication style between microservices]], [[What is the domain-specific protocol communication style]], with duplicate deliveries absorbed by [[What is the Idempotent Receiver pattern]]; the survey view is [[Which interaction styles do you know in microservices]], coordination — [[How would you orchestrate communication between multiple services]].

**External API** asks how clients reach services: [[What is the API gateway pattern in microservices]], [[How would you explain the backends for frontends pattern]]. **Service discovery** asks how an RPI client finds an instance: [[How would you explain client side service discovery]], [[How would you explain server side service discovery]], the [[How would you explain the service registry pattern]] fed by [[How would you explain self registration with a service registry]] or [[What is the third-party registration pattern in microservices]].

**Reliability** asks how to stop cascading failures — [[How would you explain Circuit Breaker]]; **security** — how to convey the requestor's identity between services — [[What is the access token pattern in microservices]].

**Observability** asks how to understand production: [[What is the log aggregation pattern in microservices]], [[What is the application metrics pattern in microservices]], [[What is the audit logging pattern in microservices]], [[What is the distributed tracing pattern in microservices]], [[What is the centralized exception tracking pattern in microservices]], [[What is the health check API pattern]], [[What is the deployment and change logging pattern in microservices]].

**Testing** asks how to verify a service without end-to-end suites: [[What is the service component test pattern]], [[What is the service integration contract test pattern]], [[What is the consumer-driven contract test pattern]]. **Deployment** asks how to run instances: [[How would you explain multiple services per host deployment]], [[How would you explain single service per host deployment]], [[What is the service per VM pattern]], [[What is the service per container pattern]], [[What is the serverless deployment pattern]], [[What is the service deployment platform pattern]].

**Cross-cutting concerns** asks where shared logic lives: [[What is the microservice chassis pattern]], [[What is the externalized configuration pattern for microservices]], [[What is the service template pattern]]. **Refactoring to services** asks how to migrate a monolith: [[What is the strangler fig pattern and when do you use it]] guarded by [[What is the anti-corruption layer pattern]]. **UI design** asks how screens combine fragments from many services: [[How would you explain server side page fragment composition]], [[How would you explain client side UI composition for micro frontends]].

```d2
direction: right
lang: "Pattern language" {style.fill: "#e8f5e9"}
lang -> style: "Architectural style"
lang -> boundaries: "Service boundaries"
lang -> collab: "Service collaboration"
lang -> messaging: "Transactional messaging"
lang -> comm: "Communication styles"
lang -> extapi: "External API"
lang -> discovery: "Service discovery"
lang -> ops: "Reliability / Security / Observability"
lang -> xcut: "Testing / Deployment / Cross-cutting"
lang -> refactor: "Refactoring / UI design"
```

**Fig. 1.** The pattern language: fifteen categories, one recurring question each; cards carry the category leaf tag.

> [!warning]
> The categories overlap by design: transaction log tailing and polling publisher surface in both data-consistency and messaging discussions, the idempotent consumer sits under communication styles, deployment constrains observability. Reciting the tree as a rigid hierarchy is the wrong target — learn, per category, the question and the forces, then place a pattern by the force that dominates.

> [!tip] Interview answer
> The microservices.io catalogue groups the microservices vocabulary into fifteen categories: pick the style, split the system (service boundaries), keep data consistent and queries fast (service collaboration, transactional messaging), choose the wire protocol (communication styles), expose and locate services (external API, service discovery), stay reliable, secure and observable, verify without end-to-end grids (testing), run the things (deployment), share boilerplate once (cross-cutting), migrate the monolith (refactoring to services), compose the UI — the order in which interviews usually drill.
