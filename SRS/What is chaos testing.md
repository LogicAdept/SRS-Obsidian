<!--
reps: 0
priority: 0
-->
#Testing #SystemDesign/Reliability #SRS

# What is chaos testing

> [!abstract] Short answer
> Chaos testing (chaos engineering) is the practice of deliberately injecting real-world failures — killing instances, adding latency, cutting network links, exhausting resources — into a system to verify that its resilience mechanisms actually work. It treats failure as an experiment: define the steady state, hypothesize it will survive the injected fault, run the experiment in as production-like an environment as possible, and automate the blast-radius control.

## The method: hypothesis, not tantrum

The discipline is codified in the principles of chaos engineering: build a hypothesis around a steady state — some measurable output (success rate, latency percentile, queue depth) that indicates normal behavior; introduce real-world events (instance death, latency, packet loss, clock skew, dependency failure) in control and experimental groups; verify the steady state did not actually change; and minimize blast radius — start small (one instance, one canary), abort automatically if the steady state breaks. The point is falsification: a graceful-shutdown path, a retry policy or a failover script that was never exercised is a hypothesis, and chaos testing is the experiment that either confirms it or finds the bug in production-like conditions rather than during an incident. The classic origin is Netflix's Chaos Monkey (terminating random instances in production so engineers build services that survive it), and the method has since formalized around those four principles.

```text
steady state:  p99 < 300ms, success rate > 99.9%
experiment:    inject 2s network delay service B -> A (1 canary)
hypothesis:    circuit breaker opens, fallback serves, p99 holds
abort:         auto-rollback if success rate < 99% during run
outcome A:     steady state held     -> resilience verified
outcome B:     steady state broke    -> a real bug found, before an outage
```

**Listing 1.** A chaos experiment as a structured test case with an abort condition.

## Where it fits and what it requires

Chaos testing complements the rest of the testing pyramid rather than replacing it: unit and integration tests verify logic, load tests ([[What is load testing]]) verify capacity, chaos verifies resilience mechanisms under failure — the two-second-outage drill ([[How do you handle a two second network outage]]), circuit breakers ([[How would you explain Circuit Breaker]]), and failover of replicated stores ([[How would you explain database replication strategies]]) are exactly the behaviors it exercises. It requires prerequisites to be worth anything: observability that can actually see the steady state metrics ([[How do you monitor an application with Spring Boot Actuator]]-style), controlled blast radius (canary scopes, automatic abort), and a system whose failure modes someone has at least enumerated. Running chaos on a system with no timeouts and no fallbacks does not test resilience — it just produces an outage with extra steps; the maturity order is measure, harden, then break.

> [!warning] Chaos without an abort condition is self-inflicted downtime
> Injecting failures into production with no automatic rollback and no blast-radius limit is not engineering. The experiment must be falsifiable (defined steady state) and reversible (auto-abort) — otherwise it is an outage with a calendar entry.

> [!tip] Interview answer
> Chaos testing injects real failures — instance kills, latency, network partitions — to verify resilience mechanisms work, as a controlled experiment: define a measurable steady state, hypothesize it survives, run on a small blast radius with automatic abort, and learn. It originated with Netflix's Chaos Monkey and complements load tests by testing failure handling, not capacity.
