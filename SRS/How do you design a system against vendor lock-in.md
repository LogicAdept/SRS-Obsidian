<!--
reps: 0
priority: 0
-->
#SystemDesign/Architecture #SystemDesign/Tradeoffs #SRS

# How do you design a system against vendor lock-in

> [!abstract] Short answer
> Designing against vendor lock-in means keeping the costly-to-migrate assets portable: data in open, documented formats; business logic behind your own interfaces rather than a vendor's SDK; interactions through standard protocols; and infrastructure described in portable definitions (containers, Kubernetes, Terraform). The honest version is selective: fully escaping lock-in everywhere costs performance and speed, so you identify which dependencies are exit-planned (data, core logic) and which are accepted deliberately (edge services, managed conveniences) with a priced exit.

## The four portability layers

Data first, because data outlives vendors: store in standard formats and engines — open table formats, plain SQL dialects over vendor extensions where feasible, exports testable on a schedule; a dataset living only in a proprietary store with a closed format is hostage regardless of code. Second, interfaces: wrap vendor SDKs behind your own abstractions at the architectural boundary — your code depends on `MessageQueue` and `ObjectStore` interfaces; adapters implement them per vendor. The tradeoff is real: wrappers add indirection and often block vendor-specific performance features, so apply them where switching is plausible (databases, queues, object storage), not everywhere. Third, protocols and runtimes: standard protocols (HTTP, SQL, AMQP/[[What is RabbitMQ]]-class open messaging, Kafka's protocol vs proprietary buses) and portable runtimes (containers, Kubernetes) keep the compute layer moving between clouds. Fourth, deployment definitions: infrastructure as code in portable tools, so environment recreation is scripted rather than archaeology. [[What is the difference between a monorepo and a multirepo]]-style repository strategy and build reproducibility complete the picture on the code side.

```text
portability layers (by exit cost):
1 data      -> open formats, tested exports            (hostage risk)
2 logic     -> own interfaces around vendor SDKs       (adapter pattern)
3 protocols -> HTTP/SQL/AMQP/Kafka; containers+k8s     (runtime port)
4 infra     -> IaC (terraform/helm), scripted envs     (ops port)
policy: exit plan per dependency, accepted costs written down
```

**Listing 1.** The portability checklist ordered by how much a vendor exit costs.

## The tradeoff economics

Anti-lock-in is insurance, and insurance has premiums: abstraction layers cost performance (missing vendor features), multi-cloud designs cost operational complexity (the weakest-common-denominator effect), open-source self-hosting costs operational headcount. So the mature design prices exits instead of refusing all lock-in: a dependency gets a documented exit plan (what it would cost in weeks/months to replace — data export, interface rewrites, ops retraining) and a decision — exit-planned (core data, identity, messaging), accepted (a managed edge cache with a 2-week replacement plan), or strategic (deliberate deep integration where the vendor's advantage justifies hostage risk). Standard-protocol choices make most exits boring: PostgreSQL-compatible engines, AMQP/Kafka brokers, S3-compatible object stores mean "migration project", not "rewrite". The failure modes of over-engineering the opposite way are equally real: wrapper abstractions that leak the vendor anyway (the abstraction exposes vendor options), and abstractions maintained for a switch nobody will ever make ([[What is overengineering and how does it affect enterprise software]] is the cautionary frame). For system-level moves (monolith to services, on-prem to cloud), the incremental path is strangler-style ([[How would you briefly describe migrating a project to Java]]), not a flag-day rewrite.

> [!warning] Abstractions that leak the vendor are lock-in with extra code
> If your `StorageService` interface exposes S3-specific options everywhere, you have paid the abstraction tax and kept the hostage risk. The abstraction earns its cost only when the vendor-specific surface is small, documented and actually implemented by a second adapter — even a test double proves the seam.

> [!tip] Interview answer
> I keep exits cheap in layers: data in open formats with tested exports, vendor SDKs behind my own interfaces, standard protocols and portable runtimes, infrastructure as code — and I write down an exit plan per dependency instead of refusing all lock-in. Deep vendor integration is accepted deliberately where its advantage justifies the priced risk.
