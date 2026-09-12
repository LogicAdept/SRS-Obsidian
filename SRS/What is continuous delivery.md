<!--
reps: 0
priority: 0
-->
#DevOps/CICD #SRS

# What is continuous delivery

> [!abstract] Short answer
> **Continuous delivery (CD)** is the discipline of keeping the software **releasable at any moment**: every green build is packaged, verified through increasingly production-like environments, and deployable to production **on demand with a push button**. The button itself is a business decision — continuous *deployment* is the variant where the button is removed and every green build ships automatically.

Continuous delivery builds directly on [[What is CI]]: integration, executables, and automated tests stay, and the pipeline is extended towards production. The defining indicators are pragmatic: the software is deployable throughout its lifecycle, the team prioritizes keeping it deployable over starting new features, anybody can get fast automated feedback on production readiness for any change, and any version can be deployed to any environment on demand. The key test is behavioral, not technical: if a business sponsor asks to deploy the current version to production at a moment's notice, nobody panics.

## What the pipeline guarantees

The mechanism is the **deployment pipeline**: an artifact is built **once** from a green commit, then promoted through stages — unit and integration tests, packaging, a staging environment that mirrors production — with automated verification at every step. Promotion moves the *same artifact*, which is why image digests matter ([[What is the difference between an image tag and a digest]]). Delivery does not decide *when* to release; it decides that releasing is safe, boring, and reproducible. What remains manual in pure delivery is the production decision itself — coordination with marketing, compliance windows, or simply business preference.

```d2
direction: right
commit: "Green commit\non main" {
  width: 220
  height: 90
  style.fill: "#e3f2fd"
}
pipe: "Deployment pipeline\nbuild -> test -> package" {
  width: 320
  height: 100
  style.fill: "#fff3e0"
}
staging: "Staging\nproduction-like checks" {
  width: 280
  height: 100
  style.fill: "#fff3e0"
}
ready: "Releasable artifact\npush-button deploy" {
  width: 260
  height: 100
  style.fill: "#e8f5e9"
}
commit -> pipe
pipe -> staging
staging -> ready
```

**Fig. 1.** The pipeline turns every green commit into a releasable artifact; only the final click is a human decision in continuous delivery.

## What has to be true around the code

Delivering frequently is a property of the whole system, not of the CI server. Database schema changes must be decoupled from application upgrades so an old and a new version can coexist — the expand-and-contract discipline behind [[How do you do blue-green deployments that include a database]]. Incomplete features must be able to ship invisibly, which is exactly what [[What is feature toggling]] provides: deploy and release become independent acts. Trunk-based flow keeps the mainline the single source of releasable truth, because release candidates do not age in long-lived branches.

> [!warning] Delivery is not "we have Jenkins"
> A CI server with a build job is not continuous delivery — the discipline is measured by whether the *output* is always releasable. Two classic lies: calling a pipeline "CD" when artifacts are rebuilt per environment (then no one knows what would actually deploy), and calling it "CD" when releases wait in long-lived release branches that rot for weeks. The other interview trap is word confusion: continuous delivery does **not** mean automatic production deployment — that is continuous deployment, and per the definition you must be doing continuous delivery first before you can do continuous deployment.

> [!tip] Interview answer
> **Continuous delivery means every green build is packaged and verified through production-like environments so it can be released at any time with a manual, push-button decision. It extends CI from "the code works" to "the artifact is releasable", promoting one immutable artifact through a deployment pipeline. Continuous deployment removes the final manual click and ships automatically; delivery keeps the click as a business choice. The prerequisite work is schema decoupling, feature toggles, and trunk-based flow.**
