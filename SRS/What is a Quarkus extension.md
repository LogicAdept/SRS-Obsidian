<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.

Draft: an extension is a pair of artifacts: a runtime jar (API, integration classes) and a deployment jar (build steps, recorded bootstrap logic). User projects depend only on the runtime artifact; the build tool plugin pulls the deployment artifact for augmentation.
Extensions "configure, boot and integrate a framework or technology" and provide GraalVM native metadata so applications compile natively without user JSON reflection configs.
Build steps in deployment modules produce/consume build items and are auto-wired; the majority of work should happen at build time.
Maturity statuses: stable, preview, experimental; catalog at quarkus.io/extensions and code.quarkus.io.
Rule: the runtime module must never depend on a deployment artifact.

> [!warning] Unverified traps from the draft
> - Facts above are plausible but unchecked; version numbers and exact API names must be confirmed against official docs before this card is used as a review answer.
> - Comparison cards must keep both sides tagged and avoid absolute always/never claims.
