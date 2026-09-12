<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/Testing #Java/Testing #SRS

# What is the service integration contract test pattern

> [!abstract] Short answer
> A service integration contract test is a test suite for a provider service, written and maintained by the team of a consuming service, that verifies the provider meets the consumer's actual expectations. It is the answer to "how do you keep service-to-service integrations working without end-to-end tests" - the consumer-driven contract testing pattern of the microservices testing language, implementable with Spring Cloud Contract or Pact.

## Mechanism: expectations become executable contracts

Each consuming service's team writes a suite against the provider that encodes precisely what the consumer relies on: this endpoint returns 200 with these fields for this input; this error case returns that code and shape. The suite runs against the provider in the provider's CI - the provider now knows, per consumer, which behaviors are load-bearing for whom. The immediate payoff: when the provider wants to change its API, its CI shows exactly which consumers' contracts break and breaks them at build time instead of in production. This closes the hole the component test leaves: there, a stub emulates the provider; here, the stub's assumptions are executed against the real provider ([[What is the service component test pattern]] is the isolated half of the pair). The stated forces and results match the classic argument against end-to-end testing: launching many services is slow, brittle and expensive, and contract tests deliver consumer-specific verification cheaply - the pattern's documented drawback is symmetric: tests can pass while production fails, if a consumer's suite omits something it actually depends on, so the discipline is deriving contracts from real call sites, not from memory.

```d2
direction: right
c: "Consumer team
writes expectations" {style.fill: "#e8f5e9"}
ct: "Contract test suite
consumer's expectations" {style.fill: "#fff3e0"}
pc: "Provider CI
runs all consumers' suites" {style.fill: "#ffe0b2"}
p: "Provider service
real API" {style.fill: "#eceff1"}
c -> ct: codify what we rely on
ct -> pc: submitted to provider
pc -> p: execute against real provider
pc -> c: breakage reported before release
```

**Fig. 1.** Consumer expectations travel to the provider's pipeline; API changes that would break a consumer fail there, at build time.

The tooling question is the natural follow-up: Spring Cloud Contract generates provider-side verification from consumer-written contracts ([[What is the difference between REST and gRPC]]-style protocol choice is orthogonal - contracts describe the API regardless of transport); Pact records actual consumer interactions and replays them as provider tests. Both reduce the pattern to build configuration - the pattern is the org-side contract between teams, the tools are its bookkeeping. Note the ownership directionality, which is the pattern's essence and its most common interview probe: the consumer specifies, the provider verifies - not the other way around. That is also why the suite is defined as "written by the developers of another service that consumes it".

> [!warning] Contracts are not a schema check
> A contract suite that only asserts field names verifies serialization, not behavior - status codes, side effects, ordering guarantees and error semantics are where integrations actually break, and they belong in the contracts. Second trap: provider-side contract sprawl - five consumers with contradictory expectations of one endpoint is a design smell the suites will surface; the resolution is a conversation about the shared API, not a fourth version of the endpoint. And do not let contracts replace collaboration: they codify an agreement, they do not create it.

> [!tip] Interview answer
> Service integration contract testing means each consumer team writes an executable suite of its expectations and the provider runs all consumers' suites in its CI - so an API change that would break a consumer fails at build time. It is consumer-driven contract testing under a different name, implementable with Pact or Spring Cloud Contract, and it verifies exactly the assumptions my component-test stubs make. I derive contracts from real call sites and include error semantics, not just happy-path shapes.
