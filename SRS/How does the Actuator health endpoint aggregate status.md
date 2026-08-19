<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Actuator #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Health composes registered `HealthIndicator` beans (db, disk, ping, …). Out-of-the-box statuses dumps name: `UP`, `DOWN`, `OUT_OF_SERVICE`, `UNKNOWN`. Aggregate status is the most severe; dump order `DOWN` > `OUT_OF_SERVICE` > `UP` > `UNKNOWN`.

`DOWN` / `OUT_OF_SERVICE` map to HTTP 503; `UP` to 200. Default JSON shows only overall status. `management.endpoint.health.show-details=always` (or `when-authorized`) shows per-indicator detail.

> [!warning] Unverified traps from the dump
> - Default health JSON hiding details is easy to miss in an interview.
