<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/CrossCuttingConcerns #DevOps/Configuration #SRS

# What is the externalized configuration pattern for microservices

> [!abstract] Short answer
> Externalized configuration moves everything that varies between environments — database locations, credentials, feature endpoints, queue addresses — out of the deployable and into the environment: the service reads configuration at startup from sources like OS environment variables, config files or a config server. It is the 12-factor "config" factor and a core cross-cutting pattern; the artifact must run in dev, QA and production unmodified.

## Mechanics: three layers of sources

The pattern separates three concerns. The artifact holds none of the environment's specifics — the same container image promotes from test to production unchanged. The environment supplies values: process environment variables are the portable floor (12-factor's canonical source); files and startup arguments extend it; a config server (Spring Cloud Config class) centralizes values per environment and per application, versioned in git, and can re-deliver at runtime through refresh endpoints. Secrets are part of configuration but get their own handling — vault-style stores or secret managers, injected at runtime, never baked into images or committed. The binding layer inside the service maps flat keys to typed settings ([[What is the externalized configuration pattern for microservices]]' sibling pattern — the microservice chassis — usually ships this binder).

```d2
direction: down
img: "Immutable artifact
same bytes in every env" {style.fill: "#e8f5e9"}
src1: "Env variables
PORT, DB_URL" {style.fill: "#e3f2fd"}
src2: "Config server
per-env, versioned" {style.fill: "#e3f2fd"}
src3: "Secret store
credentials at runtime" {style.fill: "#f3e5f5"}
app: "Service at startup
bind typed settings" {style.fill: "#fff3e0"}
img -> app
src1 -> app
src2 -> app
src3 -> app
```

**Fig. 1.** One artifact, many environments: differences arrive as injected values, not rebuilds.

## The checks that make it production-grade

Config drift is the classic failure: QA passes with values production will never match. The mitigations are operational: configuration is versioned and reviewed like code; startup validates that required keys resolve and fail fast with a clear error ("missing DB_URL") instead of half-booting; the effective configuration is inspectable at runtime (an endpoint or startup dump — minus secrets) so an operator can see what the process actually believes. Riches-to-rags rule: default values in code are fine for locals, but "it works with defaults" must never be the reason production runs. The pattern's open issue is exactly assurance — verifying that the supplied configuration matches what the deployment expects — which is why config servers keep history and why deployment pipelines print the diff of what changed ([[What is the microservice chassis pattern]] owns the binding mechanics; [[What is the deployment and change logging pattern in microservices]] records which config version shipped when).

> [!warning] Configuration is part of the attack surface
> Credentials pass through this channel, so config handling inherits security obligations: secrets are not logged at startup, not echoed in actuator endpoints, not stored in the repo "temporarily", and rotated like credentials everywhere else. A config server with permissive read is a one-URL breach of every environment at once — scope its access and audit it like production data.

> [!tip] Interview answer
> Externalized configuration keeps the deployable immutable: environment specifics — endpoints, credentials, feature settings — are injected at startup from env variables, config files or a versioned config server, with secrets coming from a vault. I get one artifact promoted across environments and drift made visible. The discipline that makes it work: fail-fast validation of required keys, effective-config inspection minus secrets, and config changes treated like code changes.
