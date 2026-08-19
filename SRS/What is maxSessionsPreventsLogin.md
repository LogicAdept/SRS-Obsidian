<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: with maximumSessions(n), maxSessionsPreventsLogin(true) keeps the existing session and fails the new login. false (common default in samples) lets the new login in and expires the previous session via ConcurrentSessionFilter.
> [!warning] Unverified traps from the dump
> - Needs a SessionRegistry (usually HTTP session). Broken in multi-instance apps without a shared registry.
