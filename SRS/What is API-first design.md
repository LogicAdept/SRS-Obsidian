<!--
reps: 0
priority: 0
-->
#API/Contracts #SRS

# What is API-first design

> [!abstract] Short answer
> API-first means the contract comes before the implementation: you design and review the API as a machine-readable artifact (typically OpenAPI), agree on it with consumers, generate mocks and SDKs from it, and only then build the service behind it. It turns the API from a build artifact into the specification of the collaboration.

## The workflow it prescribes

Classic flow: requirements -> code -> API emerges from whatever the code needed. API-first inverts: requirements -> contract draft (OpenAPI) -> consumer review (frontend, partner teams, mobile) -> mock server so consumers build against a stand-in -> parallel implementation of server and clients -> contract tests pinning the implementation to the artifact. The artifact is executable documentation: CI diffs it for breaking changes, generates server stubs and client SDKs, and serves as the published reference ([[What is OpenAPI and how does Swagger relate to it]] for the format; [[What is the difference between contract-first and code-first API development]] for the implementation-side contrast). The payoff is organizational as much as technical: integration questions surface at review time (before code exists), teams parallelize, and the "right API" gets negotiated while changing it is still cheap — which is exactly when consumers can say "this pagination shape does not work for us" ([[What are the key principles of good API design]]).

```d2
req: requirements
spec: contract draft (OpenAPI)
rev: consumer review
(frontend, partners)
mock: mock server from spec
srv: server implementation
cli: client/SDK builds
ct: contract tests
(implementation vs spec)
prod: deploy
req -> spec -> rev -> mock -> srv -> ct -> prod
rev -> cli: parallel
mock -> cli
ct: fails on drift
```

**Fig. 1.** The API-first loop: contract, review, mocks, parallel builds, and contract tests that fail on drift between spec and implementation.

## What it is not, and where it hurts

API-first is not "OpenAPI in the repo" — a spec generated after the fact and never reviewed is code-first with extra steps; the first part is the consumer in the loop. It is also not a law against iteration: exploratory endpoints can start code-first and be retro-specified before publishing — the discipline is that the published contract precedes public consumption, not that no code exists before the first YAML. Costs to acknowledge: the spec becomes a second source of truth that can drift (mitigated by spec-first codegen or contract tests, not by hope), and front-loading design slows small internal endpoints — the pattern pays most at boundaries with external or cross-team consumers ([[What is the difference between an API and a web service]] for why public boundaries demand explicit contracts). Microservice ecosystems adopt it because service interfaces are their integration currency; a monolith's internal API can stay informal ([[What is the API gateway pattern in microservices]] for where published contracts meet routing).

```text
week 0: draft OpenAPI with consumers in the room
week 0: mock server from the spec -> frontend builds against it
week 1: server and clients in parallel
every build: contract tests fail on drift
result: integration surprises surfaced in review, not in UAT
```

**Listing 1.** The process on a timeline: the contract is reviewed and mocked before the implementation exists, then pinned by tests (conceptual).

> [!warning] Drift is the failure mode, not effort
> An API-first program without drift control degenerates: the spec stops matching the service, consumers trust the spec, production behaves differently. Either generate implementation from the spec or run contract tests on every build — pick one mechanically, not culturally.

> [!tip] Interview answer
> API-first treats the contract as the specification of the collaboration: design it in OpenAPI before implementation, review it with actual consumers, hand them a mock server, then build server and clients in parallel and pin both with contract tests. The API stops being an artifact your code emits and becomes the interface you both implement. It pays off at cross-team and public boundaries where negotiation must happen while change is still cheap.
