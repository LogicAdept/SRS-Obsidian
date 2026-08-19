<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: session fixation is an attacker planting a session id. Spring Security’s SessionFixationProtectionStrategy creates a new session id after successful authentication so the planted id is useless.

sessionManagement().sessionFixation().migrateSession() is the HttpSecurity spelling of the same idea.
> [!warning] Unverified traps from the dump
> - STATELESS APIs have no session id to rotate.
