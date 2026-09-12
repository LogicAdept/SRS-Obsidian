<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/Testing #Java/Testing #SRS

# What is the consumer-driven contract test pattern

> [!abstract] Short answer
> The consumer-driven contract test pattern — from the Testing group of the microservices.io catalogue — makes the consumer of a service author a test suite that encodes exactly the requests and responses it depends on, and makes the provider run that suite in its own pipeline. The contract becomes the provider's obligation: if a change breaks any consumer's expectations, the provider's build fails before the change can ship. It converts "will this break the client?" from a deployment-time surprise into a build-time signal.

## Problem: integration testing at deployment time is too late

In a system built from independently deployable services, each team can break the others without touching their code. The [[What is the service integration contract test pattern]] verifies a consumer against a stub of the provider — the consumer learns immediately if its client no longer matches the expected responses — but the provider itself has no visibility into what any consumer actually depends on. End-to-end integration tests give that visibility, but across dozens of services they are slow, brittle and cannot run on every commit, so breaking changes are discovered in a shared staging environment, by another team, hours or days after the offending commit.

## Solution: the consumer writes the contract, the provider verifies it

Each consumer team writes a suite expressing the interactions it relies on: this request against the provider must yield this response shape and status. The suite is published to a contract repository (in tooling such as Pact, a broker); the provider's CI fetches all consumer contracts and replays the provider against them on every change. A provider that satisfies all contracts is, by construction, safe to deploy for the consumers that wrote them — this is the property that makes the pattern a pillar of independent deployability alongside the [[What is the service component test pattern]], which tests a service in isolation against stubs of its own dependencies. Spring Cloud Contract implements the same loop, though its contracts are traditionally authored provider-side; the direction of authorship is a detail, the verified mutual obligation is the essence.

```d2
direction: right
consumer: "Consumer team" {
  suite: "contract suite: request -> expected response"
}
broker: "Contract broker" {shape: queue}
provider: "Provider CI" {
  verify: "verify all consumer contracts"
  api: "provider API"
}
consumer.suite -> broker: "publish pact"
broker -> provider.verify: "fetch contracts"
provider.verify -> provider.api: "exercise"
provider.verify -> broker: "verification results"
```

**Fig. 1.** Consumer expectations flow through a broker into the provider's pipeline; a failing contract blocks the provider's release.

## Forces and failure modes

The pattern rebalances test ownership: consumers specify needs without access to the provider's code, providers evolve without guessing who depends on what. Its costs are real. Contracts can over-specify — pinning headers, field order or incidental values turns cosmetic provider refactors into false breakages and trains teams to weaken contracts. A green contract suite proves shape compatibility, not business correctness: the provider may satisfy every expectation while implementing the wrong behaviour, so a thin layer of end-to-end tests still has a place. The loop also depends on process discipline — a broker nobody consults, or consumers who stop updating their contracts, silently degrades the safety net.

> [!warning]
> Do not treat consumer contracts as a full integration substitute. They verify structure, not semantics, and they are only as current as the consumer team keeps them. Over-specified contracts are the commonest failure: assert the fields the consumer truly uses, and nothing more, or the provider becomes afraid of every refactor.

> [!tip] Interview answer
> Consumer-driven contract testing: consumers publish suites describing the exact provider interactions they depend on, and the provider replays all consumer contracts in its own CI, so a breaking change fails the provider's build instead of the consumer's deployment. Compared with service integration contract tests — which protect the consumer against provider drift — the consumer-driven variant protects the provider's independence by making every consumer's expectations explicit and machine-checkable.
