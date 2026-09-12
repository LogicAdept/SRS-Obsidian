<!--
reps: 0
priority: 0
-->
#DevOps/Configuration #DevOps/Deployment #SRS

# What is feature toggling

> [!abstract] Short answer
> **Feature toggling** (feature flags) puts a runtime `if` around a codepath: the code ships — deployed — but the **toggle router** decides at execution time whether anyone reaches it. This decouples *deployment* from *release*: incomplete features ride along in every build of main, invisible, and are switched on by configuration, not by a new build.

The mechanism is small: a toggle point (`if featureIsEnabled("new-algorithm")`) asks a **toggle router** backed by configuration — from a static config file to a distributed admin service. The taxonomy matters more than the plumbing, because the four categories have opposite lifecycles. **Release toggles** enable trunk-based development: unfinished code merges to main and ships dark; the decision is static per release and the flag should live days to weeks before removal. **Experiment toggles** run A/B testing: a cohorting router sends each user consistently down one path, the flag is highly dynamic and must stay until statistical significance. **Ops toggles** are operational kill switches — disable an expensive or misbehaving feature under load without a redeploy; a few long-lived ones function as manually managed circuit breakers and must be reconfigurable in seconds. **Permissioning toggles** shape experience per user (premium features, alpha cohorts — "champagne brunch" for internal users, which differs from a [[What is a canary release]] by using specific users rather than a random sample).

```java
// Conceptual: toggle router and toggle point
Map<String, Boolean> flags = configService.load();
ToggleRouter router = new ToggleRouter(flags);

if (router.isEnabled("checkout-v2")) {
    return checkoutV2.pay(order);   // new path, shipped dark
} else {
    return legacyCheckout.pay(order);
}
```

**Listing 1.** The minimal shape: configuration-backed router, one toggle point, both codepaths testable by flipping configuration in the test.

## Why it is the enabler of everything else in this deck

Continuous delivery asks for "always releasable" even when features are half-done — release toggles are the answer, which is why the practice sits beside [[What is CI]] and [[What is continuous delivery]] rather than beside deployment tooling. For progressive exposure, toggles compose with routing: a [[What is blue-green deployment]] switches environments, a canary switches traffic weights, a toggle switches *behavior inside* a deployment — three axes that answer different questions.

> [!warning] Toggle debt compounds silently
> Every surviving flag multiplies the states the system can be in: the matrix of flag combinations explodes test scope, hides dead branches, and turns code into archaeology — so release toggles are transitionary by nature and must be removed on a schedule, with the test for both paths written *while* the toggle exists. The operational trap is the static router used for an ops toggle: if flipping requires a redeploy, the kill switch does not kill anything during the incident it was built for. The interview trap is the swap error — claiming toggles exist to "avoid merging branches": they avoid *releasing* merged code; branching strategy and toggles solve different halves of integration.

> [!tip] Interview answer
> **A feature flag is a runtime conditional backed by a toggle router that decouples deploying code from releasing it. Four categories with different lifecycles: release toggles ship incomplete work dark and die in weeks, experiment toggles drive A/B cohorts, ops toggles are kill switches reconfigurable without redeploy, permissioning toggles gate features per user. Flags are the enabler of trunk-based development and continuous delivery — and their cost is real: a combination-testing burden and toggle debt that must be paid by scheduled removal.**
