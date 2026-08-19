<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Admin #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Spring Boot Admin is a community UI for managing and monitoring Spring Boot applications. It shows status of registered apps (typically via Actuator: health, metrics, env, loggers).

You run an Admin **server** and add the **client** (or use discovery) so instances register. It is not part of Spring Boot core.

> [!warning] Unverified traps from the dump
> - Exposing Actuator to Admin without auth leaks env/heapdump-style data.
> - Interviewers may still say “Boot Admin” when they mean Actuator endpoints — Admin is the dashboard on top.
