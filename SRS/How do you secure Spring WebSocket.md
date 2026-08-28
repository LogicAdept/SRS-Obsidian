<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Spring/Security #SRS

# How do you secure Spring WebSocket?

> [!abstract] Short answer
> **Authentication is the HTTP handshake:** the WebSocket `Principal` is the `HttpServletRequest` principal. Secure the HTTP app with Spring Security; that identity is reused. **Authorization of STOMP destinations is separate.** From Security **5.8**, use **`@EnableWebSocketSecurity`** and an **`AuthorizationManager<Message<?>>`** bean (`simpDestMatchers`, `anyMessage()`, …). **`HttpSecurity` alone does not lock `/app` or `/user`.** Spring Security **does not** secure JSR-356/`TextWebSocketHandler` message bodies — intercepting those needs the STOMP/`clientInboundChannel` model (or a handshake interceptor).

## Handshake identity, then inbound messages

`@EnableWebSocketSecurity` (javadoc since **5.8**): CONNECT needs a **CSRF token** (same-origin defense — browsers **do not** apply SOP to WebSockets). `SecurityContextHolder` is filled from the **`simpUser`** header. Match destinations with `MessageMatcherDelegatingAuthorizationManager.Builder`. Deny **MESSAGE** to broker prefixes (`/topic`, `/queue`) so clients cannot impersonate the broker; deny **SUBSCRIBE** to raw `/queue/*` so one user cannot read another’s unique queue. Security secures **`clientInboundChannel` only**, not outbound. CSRF on CONNECT is **not** tunable via `@EnableWebSocketSecurity`; to skip CSRF, omit that annotation and wire `AuthorizationChannelInterceptor` yourself. SockJS: ignore HTTP CSRF on the handshake path only, put the token in **STOMP CONNECT headers**, set **`X-Frame-Options` SAMEORIGIN**. Handshake reject: [[What is a HandshakeInterceptor for WebSocket]]. Origins: [[How do you register a STOMP endpoint with CORS]]. STOMP: [[What is STOMP in Spring WebSocket]]. Legacy class: [[What is AbstractSecurityWebSocketMessageBrokerConfigurer]]. User dest: [[How do you send a message to one user with Spring WebSocket]].

```java
@Configuration
@EnableWebSocketSecurity
public class WebSocketSecurityConfig {

	@Bean
	AuthorizationManager<Message<?>> messageAuthorizationManager(
			MessageMatcherDelegatingAuthorizationManager.Builder messages) {
		messages.simpDestMatchers("/user/**").hasRole("USER");
		return messages.build();
	}
}
```

**Listing 1.** Conceptual: Security 6.x `@EnableWebSocketSecurity` sample. Advanced chains typically `nullDestMatcher().authenticated()`, permit `/user/queue/errors`, `hasRole` on `/app/**`, then **`anyMessage().denyAll()`**.

```d2
direction: down
http: "HTTP SecurityFilterChain\nPrincipal" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
hs: "WebSocket handshake" {
  width: 220
  height: 40
  style.fill: "#fff3e0"
}
in: "clientInboundChannel\nAuthorizationManager" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}

http -> hs
hs -> in
```

**Fig. 1.** Filter-chain login is not destination authorization. Outbound MESSAGE frames are not re-checked.

> [!warning]HttpSecurity does not lock STOMP destinations
> An authenticated handshake plus `setAllowedOriginPatterns("*")` and no message `AuthorizationManager` is an **open broker** for whoever can CONNECT. `@SendTo("/topic")` privacy is not security. `sameOriginDisabled() == true` on the **legacy** configurer **turns CSRF off** for CONNECT.

> [!tip] Interview answer
> **Reuse HTTP authentication on the handshake, then authorize STOMP with `@EnableWebSocketSecurity` and `AuthorizationManager<Message<?>>`.** Match `/app` and `/user` separately; deny client MESSAGE to `/topic`. CSRF on CONNECT enforces same origin. `HttpSecurity` is not enough. The old `AbstractSecurityWebSocketMessageBrokerConfigurer` is deprecated (gone in Security 7).
