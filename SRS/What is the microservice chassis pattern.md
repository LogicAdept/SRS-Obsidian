<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/CrossCuttingConcerns #SRS

# What is the microservice chassis pattern

> [!abstract] Short answer
> The microservice chassis is a framework or template that every new service starts from, with the cross-cutting concerns already wired: build and packaging, externalized configuration, logging, health checks, metrics, distributed tracing, security token handling, and the boilerplate for infrastructure clients. Richardson contrasts it with the service template — same idea as an in-house copy-paste generator; both serve one goal: a new service is productive in hours, and cross-cutting behavior is uniform across the fleet.

## What goes into the chassis — and why each item is there

Richardson's own list of cross-cutting concerns defines the contents. Build logic: one blessed way to build, test and package (Docker image) with curated dependencies. Externalized configuration: the binding layer for env/config-server values ([[What is the externalized configuration pattern for microservices]]). Observability: structured logging, a metrics facade, a health check endpoint ([[What is the health check API pattern]], [[What is the application metrics pattern in microservices]], [[What is the distributed tracing pattern in microservices]]). Security: token validation and propagation. Infrastructure clients: database and broker connectivity with sane defaults. Transport plumbing: command/reply dispatchers if the CQRS style is standard ([[What is a command handler in CQRS]]). Everything that is not business logic but that every service would otherwise re-implement — differently — lives here.

```d2
direction: down
chassis: "Microservice chassis
config, logging, metrics, health,
tracing, security, infra clients" {style.fill: "#e3f2fd"}
s1: "Orders service
business logic only" {style.fill: "#e8f5e9"}
s2: "Inventory service
business logic only" {style.fill: "#e8f5e9"}
s3: "Next service
clone and add logic" {style.fill: "#e8f5e9"}
chassis -> s1
chassis -> s2
chassis -> s3
```

**Fig. 1.** The chassis is the fleet-wide "everything but the business logic" layer; each service adds only its domain.

## The governance problem the chassis solves — and creates

Without a chassis, cross-cutting behavior drifts: service A logs unstructured lines, service B has no health endpoint, service C validates tokens with its own subtly different rules — and the fleet's observability, security and operability degrade to the weakest service. The chassis makes the right thing the default thing. The same mechanism creates its own risk: the chassis is a shared dependency with real upgrade politics — a breaking change fans out to every service, so its API must be versioned and its upgrades planned like a product release. Two evolution paths: versioned in-house libraries (chassis), or pushing these concerns out of code entirely into platform proxies ([[How would you explain the service mesh pattern]] is the destination — the mesh owns mTLS, retries, tracing headers; the chassis then shrinks to config binding and business-adjacent plumbing). Most real fleets run both: chassis for language-level concerns, mesh for network-level ones.

> [!warning] A chassis is a monolith-shaped trap if it grows domain logic
> The moment the chassis starts exposing "shared" business entities or validators, every service's domain is coupled through the framework — a distributed big ball of mud with a release train. The chassis boundary is strict: technical plumbing only. Domain code that two services both need is either duplication to accept or a design smell to fix, never a chassis feature.

> [!tip] Interview answer
> A microservice chassis is the framework every service starts from: build and packaging, externalized config, structured logging, metrics, health checks, tracing, token handling and infrastructure clients pre-wired. New services are productive in hours and the fleet behaves uniformly — one health endpoint style, one tracing pipeline. Its cost is governance: it's a shared dependency needing versioned releases, and it must stay strictly technical — the moment it hosts domain logic, services are coupled through the framework.
