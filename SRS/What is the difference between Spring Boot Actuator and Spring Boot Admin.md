<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Admin #Java/Spring/Boot/Actuator #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Actuator (Boot module): production endpoints (`/health`, `/metrics`, …) over HTTP or JMX. You still curl or scrape them.

Admin (community UI, not Boot core): a dashboard that registers Boot apps and shows their Actuator data (status, health, metrics, env, loggers).

> [!warning] Unverified traps from the dump
> - Interviewers often say Admin when they mean Actuator endpoints.
> - Admin without exposing Actuator on the client has nothing to display.
