<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

STOMP stack dump: extend `AbstractSecurityWebSocketMessageBrokerConfigurer`, `configureInbound` with `simpDestMatchers("/user/**").authenticated()` and `anyMessage().authenticated()`, `sameOriginDisabled()` returning true in the sample.

Handshake dump: `HandshakeInterceptor.beforeHandshake` to validate a JWT and reject the upgrade.

Default: the endpoint is open to anyone who can hit the URL.

> [!warning] Unverified traps from the dump
> - HTTP `HttpSecurity` alone does not automatically lock STOMP destinations.
> - Wildcard allowed origins plus no auth is the open-relay setup dumps warn about.

