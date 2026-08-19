<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump core component: AccessDecisionManager makes the authorization decision (allow or AccessDeniedException). Custom dumps implement decide(...) plus supports(...).

It is the voter-era API behind FilterSecurityInterceptor. Security 6 dumps prefer AuthorizationManager and AuthorizationFilter.
> [!warning] Unverified traps from the dump
> - AffirmativeBased / ConsensusBased / UnanimousBased are the old voter aggregators some dumps still name.
