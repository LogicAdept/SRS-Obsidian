<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Actuator #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Adding `spring-boot-starter-actuator` does not expose every endpoint. Dumps: by default only `/actuator/health` is exposed over HTTP. Other endpoints may be enabled but not reachable until you opt in, e.g. `management.endpoints.web.exposure.include=health,info,metrics`.

> [!warning] Unverified traps from the dump
> - Dump lists sometimes still mention `/info` as default; treat default exposure as a version-sensitive claim.
> - A star include in production without auth is the open-management setup dumps warn about.
