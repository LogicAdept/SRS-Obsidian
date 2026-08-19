<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Older dump filter tables: ChannelProcessingFilter / CHANNEL_FILTER enforces requires-channel (HTTP vs HTTPS) from intercept-url requires-channel or HttpSecurity requiresChannel. It runs at the start of the chain so insecure requests redirect before authentication.
> [!warning] Unverified traps from the dump
> - Boot server.ssl.* is the container TLS. ChannelProcessingFilter is the Spring Security redirect/enforce layer on top.
