<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Actuator #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Implement `HealthIndicator` and return a `Health` object. Dump sample: a `@Component` that returns `Health.down().withDetail(...)` or `Health.up().withDetail(...)`.

The bean name minus the `HealthIndicator` suffix becomes the key in the aggregated health JSON.

> [!warning] Unverified traps from the dump
> - A custom indicator still only shows in `/health` details if show-details is on.
