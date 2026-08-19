<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Properties #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Convention: `application-{profile}.properties` (or `.yml`). `dev-application.properties` is the wrong name.

When `dev` is active, `application-dev.properties` loads on top of `application.properties` and overrides overlapping keys. Dumps: `application-default.*` only when no profile is active.

> [!warning] Unverified traps from the dump
> - Profile files do not replace the base file; they overlay it.
