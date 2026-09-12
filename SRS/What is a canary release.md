<!--
reps: 0
priority: 0
-->
#DevOps/Deployment/Strategies/Canary #SRS

# What is a canary release

> [!abstract] Short answer
> A **canary release** reduces the risk of a new version by rolling it out **gradually**: deploy to a small slice of the infrastructure, route a small percentage of users to it, watch error rates and latency, then widen the exposure step by step — or reroute everyone back if metrics degrade. The name is the miner's canary: an early-warning signal that reacts before the whole system is poisoned.

The mechanics live in routing, not in deployment: the new version runs alongside the old one, and a load balancer, ingress controller, or service mesh assigns traffic by weight — 1%, then 5%, then 25%, then all — with automated promotion gated on the metrics of the canary slice. The user selection can be a random sample, internal employees first, or profile-based cohorts; at geographic scale, one region or brand goes first. Because real production traffic exercises the new version early, a canary doubles as **capacity testing with a safe rollback**, which no pre-production environment reproduces honestly. In Kubernetes the same pattern is expressed through weighted services and progressive-rollout controllers, complementing the platform's own mechanics ([[How do you perform a rolling update and rollback in Kubernetes]] describes the built-in pod-level version of gradual replacement).

```d2
direction: right
lb: "Router / mesh\nweight-based routing" {
  width: 280
  height: 100
  style.fill: "#e3f2fd"
}
old: "Stable v1.4\n95% of users" {
  width: 260
  height: 100
  style.fill: "#fff3e0"
}
canary: "Canary v1.5\n5% of users" {
  width: 260
  height: 100
  style.fill: "#ffebee"
}
metrics: "Error rate, latency\npromote or reroute" {
  width: 300
  height: 100
  style.fill: "#e8f5e9"
}
lb -> old
lb -> canary
canary -> metrics
metrics -> lb: "widen or rollback"
```

**Fig. 1.** Canary routing: a small, measured slice of traffic validates the new version while the majority stays protected.

## Canary versus its neighbors

Against **blue-green** ([[What is blue-green deployment]]): blue-green switches *all* traffic at once between two full environments — rollback is instant but exposure is binary; a canary exposes *fractions* of traffic and can hold at any ratio, at the cost of running two versions concurrently. Against **A/B testing**: the tooling overlaps but the intent differs — a canary detects regressions and should complete in minutes or hours, while an A/B experiment measures a hypothesis and needs statistically significant sample sizes over days; conflating them corrupts both measurements. Against **feature toggles** ([[What is feature toggling]]): a toggle exposes code inside the *same* deployment, while a canary routes between *different* deployments; large organizations combine them — an internal canary with all flags enabled was one well-known company's standard first step.

> [!warning] Two versions are a real cost
> A canary means the old and new versions both serve production simultaneously, so every shared dependency must tolerate both: database schema changes need the expand-contract discipline, message formats need compatibility, and caches must not be poisoned by version-specific shapes. The discipline trap is calling a deploy "canary" while nobody defined the promotion metrics — an unmeasured canary is just a slow, risky rollout. And for client-installed software (mobile apps, desktop agents) canary routing barely applies: version adoption is controlled by the client, so backend compatibility windows matter more than server-side weights.

> [!tip] Interview answer
> **A canary release ships the new version to a small percentage of real traffic, watches error and latency metrics, and progressively widens or reroutes back — phased rollout with production-grade validation. It differs from blue-green, which is an all-or-nothing switch between two environments, and from A/B testing, which measures hypotheses rather than guarding releases. It requires weighted routing, metric gates, and compatibility between concurrent versions, especially for database schemas.**
