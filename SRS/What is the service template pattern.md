<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/CrossCuttingConcerns #SRS

# What is the service template pattern

> [!abstract] Short answer
> A service template is a copyable source-code skeleton for a production-ready service: build logic, packaging and the standard cross-cutting concerns - configuration, logging, health checks, metrics, registration - already wired, with a sample of business logic. Richardson's pattern for making "create a new service" a fast, boring, consistent act; related to [[What is the microservice chassis pattern]] as either its alternative or its outer layer.

## Mechanism: copy, rename, start writing business logic

Creating the first microservice is an architecture problem; creating the twentieth is a consistency problem. The template answers the second: a runnable service that already implements the required build logic (compile, test, package into a container image) and the cross-cutting concerns every service needs - externalized configuration, structured logging, health check endpoints, application metrics, service registration. A developer copies the template repository, renames the service, plugs in business logic, and ships - Richardson's stated benefit is that this keeps creating services fast and ensures cross-cutting concerns are implemented the same way everywhere, which is what makes the estate operable: alerting rules, dashboards and on-call runbooks assume every service exposes metrics and health the same way ([[What is the externalized configuration pattern for microservices]] and [[What is the health check API pattern]] are typical template-resident concerns).

```d2
direction: right
tpl: "Service template repo
build + cross-cutting + sample" {style.fill: "#e8f5e9"}
d1: "New service A
copy + business logic" {style.fill: "#eceff1"}
d2: "New service B
copy + business logic" {style.fill: "#eceff1"}
ops: "Ops estate
uniform metrics/logs/health" {style.fill: "#fff3e0"}
tpl -> d1: copy
tpl -> d2: copy
d1 -> ops: same conventions
d2 -> ops: same conventions
```

**Fig. 1.** One template seeds many services with identical operational surfaces; the platform tooling can then treat them uniformly.

## Template versus chassis, and the copy-paste cost

The relationship Richardson draws: the template may be an alternative to the microservice chassis, or - more likely - the template uses a chassis as its framework and adds the code and configuration that does not belong in shared runtime (the service's specific wiring, build, and smoke tests). The chassis centralizes cross-cutting runtime behavior in a framework the services inherit; the template is source you own and copy. Richardson's stated drawback is the trade: it is copy-paste programming at scale - when the template changes, existing services must be updated individually; forking the template repo leverages Git but risks services created at different times diverging. Mitigations in practice: keep the template thin (push as much as possible into the chassis/framework version line), generate rather than copy where feasible, and treat template upgrades as routine dependency bumps with a compatibility promise. The acknowledged issue: you need one template per language/framework, which makes adopting a new stack a deliberate, costed decision - not a developer's afternoon whim.

> [!warning] A stale template rots the whole estate
> The template's worst failure is success while outdated: every service cloned from a three-year-old template inherits its unmaintained build logic and security settings, and the divergence Richardson warns about becomes measurable - services built in Q1 and Q4 speak different logging formats. Treat the template as a product: versioned, owned, with a changelog and an upgrade path. Second trap: gold-plating - stuffing the template with every team's favorite boilerplate; a template nobody wants to copy gets forked-and-pruned, and the consistency benefit is gone.

> [!tip] Interview answer
> A service template is a copyable, runnable skeleton of a production-ready service: build and packaging plus the standard cross-cutting concerns - config, logging, health, metrics, registration - already wired. New services start by copying it, which keeps creation fast and the estate operationally uniform. It is copy-paste by nature - template upgrades are a real maintenance cost - so I keep it thin, often on top of a microservice chassis, and manage it like a product.
