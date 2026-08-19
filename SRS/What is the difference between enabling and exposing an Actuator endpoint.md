<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Actuator #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Enabled means the endpoint bean exists. Exposed means it is reachable over a transport (HTTP or JMX).

Dumps: almost every endpoint is enabled but not exposed by default. Toggle enablement with `management.endpoint.<id>.enabled`. Toggle HTTP exposure with `management.endpoints.web.exposure.include` / `exclude`.

> [!warning] Unverified traps from the dump
> - Mixing up enabled vs exposed is the dump's most common Actuator mistake.
> - `management.endpoints.enabled-by-default=false` flips enablement, not exposure.
