<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.

Draft: in dev and test mode Quarkus automatically provisions unconfigured services — databases, brokers, keycloak — usually via Testcontainers, and wires the generated config (connection URL, credentials) into the application.
Trigger: you include an extension that supports Dev Services and do not configure the service yourself; explicit configuration disables the Dev Service automatically.
Requires a container environment (Docker/Podman); without one you must configure services normally.
Defaults: startup timeout 60s (quarkus.devservices.timeout); containers shared via label-based discovery across restarts; testcontainers reuse possible.
Not active in production mode.

> [!warning] Unverified traps from the draft
> - Facts above are plausible but unchecked; version numbers and exact API names must be confirmed against official docs before this card is used as a review answer.
> - Comparison cards must keep both sides tagged and avoid absolute always/never claims.
