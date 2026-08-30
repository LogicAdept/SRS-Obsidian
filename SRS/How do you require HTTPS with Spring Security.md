<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

This is channel security, not keystore setup. Dumps force HTTPS in HttpSecurity:

```java
http.requiresChannel().anyRequest().requiresSecure();
```

The servlet container still needs a TLS listener (Boot: server.ssl.*). Spring Security then redirects HTTP to HTTPS (or rejects the channel).
> [!warning] Unverified traps from the dump
> - requiresSecure() does not create a certificate. Without server TLS the redirect loops or fails.
> - Behind a reverse proxy you often need forwarded headers so Spring sees the original scheme.
