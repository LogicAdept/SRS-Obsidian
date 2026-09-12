<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/Testing #SRS

# What is the service component test pattern

> [!abstract] Short answer
> A service component test tests one service in isolation: the service runs for real, while every other service it depends on is replaced by a test double emulating its contract. It is the middle layer of the microservices testing pyramid - much faster and stabler than end-to-end tests, at the price of trusting the doubles, which contract tests then verify.

## Mechanism: real service, fake world

End-to-end tests that launch many services are slow, brittle and expensive to keep green - the pattern's stated motivation. The component test narrows the blast radius: deploy one service (in-process for pure logic, or in a container for the full HTTP stack), stand in doubles for its collaborators, drive its API, and assert on its behavior. The design question the pattern must answer: which dependencies get doubles and which stay real. Owned infrastructure - a real database in a container ([[How would you explain Testcontainers]] is the standard mechanism) - is usually kept, because the service's persistence behavior is part of what is being tested. Foreign services are replaced: a stub Payment Service returns scripted auth codes, a stub Inventory Service returns scripted stock levels. My verified micro-case runs exactly this shape: OrderService wired to a stub gateway, asserting the auth-code path, the contract-violation path and that the real gateway was never touched (MS05 in empirics).

```d2
direction: right
t: "Component test
drives service API" {style.fill: "#e8f5e9"}
svc: "Service under test
real code, real DB" {style.fill: "#fff3e0"}
db: "Real database
(Testcontainers)" {style.fill: "#e8f5e9"}
pay: "Stub payment service
scripted responses" {style.fill: "#ffe0b2"}
inv: "Stub inventory service" {style.fill: "#ffe0b2"}
t -> svc: HTTP calls
svc -> db: real writes
svc -> pay: stub
svc -> inv: stub
```

**Fig. 1.** One live service in a scripted world: infrastructure stays real where the service owns it, collaborators are replaced where it does not.
```java
StubPaymentGateway stub = new StubPaymentGateway();
OrderService svc = new OrderService(stub);   // isolation: no network, no other services
check("checkout returns provider auth code", svc.checkout(7, 1999).equals("AUTH-7-1999"));
check("stub called exactly once", stub.calls == 1);
```

**Listing 1.** Verified on JDK 21 (MS05_ComponentTestStub in empirics): `4/4 component checks green against test doubles` — the real gateway is never wired in, so its failure modes cannot even execute; only the contract the stub emulates is exercised.


The suite inherits the speed of unit tests and much of end-to-end confidence: the service's real routing, serialization, validation and persistence run; only the cross-service seams are scripted. That residual seam risk is precisely what [[What is the service integration contract test pattern]] exists to cover - the doubles are verified against the providers they imitate, closing the gap between "passes with stubs" and "works in production".

## The standing risk and the discipline

The stated drawback: tests might pass while the application fails in production - if a double's scripted behavior drifts from the real provider, the component test keeps green over a broken integration. The discipline that makes the pattern honest: doubles live in versioned, shared fixtures owned next to the contract, every production incident involving a provider gets a failing-double regression, and the contract-test layer runs against real providers in CI. When those hold, component tests become the workhorse of a microservice team: every story gets a component-level test of the service's actual API, and the end-to-end suite shrinks to a few smoke journeys.

> [!warning] Doubles drift, tests keep lying
> The killer failure: a stub that still emulates last year's provider behavior - a new required field, a changed error contract - and a green pipeline shipping an integration that 500s in staging. Doubles are hypotheses about providers; unverified hypotheses rot. Second trap: doubling the wrong seam - stubbing the service's own database makes the test assert against fiction, since persistence is the service's real responsibility; infrastructure the service owns stays real in a component test.

> [!tip] Interview answer
> A component test tests one service in isolation: the service itself runs for real - ideally with a real database via Testcontainers - and every collaborating service is a scripted test double. It gives near-unit speed with real API coverage, replacing slow end-to-end suites. The risk is doubles drifting from real providers, so I pair the suite with contract tests that verify the doubles against the real services.
