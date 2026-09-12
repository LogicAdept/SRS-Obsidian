<!--
reps: 0
priority: 0
-->
#DevOps/CICD #SRS

# What is the difference between continuous delivery and continuous deployment

> [!abstract] Short answer
> **Continuous delivery** ends at a releasable artifact: every green build *can* go to production, and a human presses the button. **Continuous deployment** removes the button: every green build goes to production automatically, which yields many production releases per day. Deployment presupposes delivery — a team that cannot keep software releasable has nothing safe to automate shipping.

Both share the same pipeline up to the same point — the one [[What is continuous delivery]] builds: integrate, build once, test automatically, verify in production-like environments. They diverge at the last gate. In delivery the final production decision stays with a person — usually because release timing is a business matter: marketing campaigns, contractual windows, or regulated processes. In deployment that decision is encoded in the pipeline itself: when the artifact passes all gates, it ships. The practical consequence is that continuous deployment demands *more* machinery than delivery, not less: trustworthy automated tests, post-deploy verification, automated rollback, and a way to decouple deploy from release, such as [[What is feature toggling]], so a shipped-but-unreleased feature harms nobody. Progressive exposure techniques — a [[What is a canary release]] or a blue-green switch — are the traffic-side tools that make frequent automatic shipping survivable.

```d2
direction: right
artifact: "Green build\nverified in staging" {
  width: 260
  height: 100
  style.fill: "#e3f2fd"
}
gate: "Manual approval\n(business decision)" {
  width: 260
  height: 100
  style.fill: "#fff3e0"
}
prod1: "Production\n(delivery)" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}
auto: "Automated ship\n(no gate)" {
  width: 240
  height: 100
  style.fill: "#ffebee"
}
prod2: "Production\n(deployment)" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}
artifact -> gate -> prod1
artifact -> auto -> prod2
```

**Fig. 1.** The two practices share everything up to a verified artifact; they differ only in who or what closes the final gate.

## Choosing between them

The choice is organizational before it is technical. Continuous deployment maximizes user feedback velocity and keeps batches small — small changes mean reduced deployment risk and believable progress. Delivery fits teams whose release cadence is externally constrained: release trains, customer-owned install dates, or change-approval processes where a human sign-off is mandated. Many organizations run both modes for different services in the same company, which is a strong hint that this is a policy dial, not a religion.

```yaml
# Conceptual: the same pipeline, two final stages
stages:
  - build
  - test
  - deploy-staging
  - deploy-prod
deploy-staging:
  stage: deploy-staging
  script: ["promote --env staging"]
deploy-prod:
  stage: deploy-prod
  script: ["promote --env prod"]
  when: manual     # delivery: remove this line for continuous deployment
```

**Listing 1.** In a YAML pipeline the whole difference is often the `when: manual` gate on the production job.

> [!warning] Interview traps
> Treating "CI vs CD" as the fundamental split is the common muddle: CI answers "does the integrated code work", and both delivery and deployment sit beyond it — the sharp technical boundary is **delivery vs deployment**. Equally wrong is claiming continuous deployment means "deploying continuously to staging" — the defining property is *automatic production* releases. And never present deployment as the strictly better maturity level: for regulated or customer-paced products, automatic shipping is a liability, and keeping the manual gate is the correct engineering choice, not a lagging indicator.

> [!tip] Interview answer
> **Continuous delivery keeps every green build releasable and leaves the production release as a manual business decision; continuous deployment automates that last step so every green build ships to production. Deployment requires delivery plus stronger safety machinery — automated rollback, post-deploy checks, and feature toggles. The boundary is policy: how much release timing is a business decision versus an automated pipeline property.**
