<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Spring/Security #SRS

# What is `AbstractSecurityWebSocketMessageBrokerConfigurer`?

> [!abstract] Short answer
> **`AbstractSecurityWebSocketMessageBrokerConfigurer`** (Security **4.0**, `org.springframework.security.config.annotation.web.socket`) is the **legacy** Java config base for **STOMP inbound authorization**. Subclasses override **`configureInbound(MessageSecurityMetadataSourceRegistry)`** (`simpDestMatchers`, `anyMessage()`, …) and optionally **`sameOriginDisabled()`**. It implements Framework **`WebSocketMessageBrokerConfigurer`**. **Deprecated — use `@EnableWebSocketSecurity` instead.** **Removed in Spring Security 7.**

## What the subclass actually did

`configureClientInboundChannel` is **`final`**. It always adds **`SecurityContextChannelInterceptor`**. Unless **`sameOriginDisabled()`** is true, it adds **`CsrfChannelInterceptor`** (CSRF token required on **CONNECT**; default **`sameOriginDisabled()` is `false`**). If `configureInbound` registered matchers, it adds **`ChannelSecurityInterceptor`**. Extra interceptors go in **`customizeClientInboundChannel`**. `@Order(HIGHEST_PRECEDENCE + 100)`. Handshake CSRF token copy: **`CsrfTokenHandshakeInterceptor`**. Replacement and full model: [[How do you secure Spring WebSocket]]. STOMP enablement: [[What is the EnableWebSocketMessageBroker annotation]]. Configurer SPI: [[What is WebSocketMessageBrokerConfigurer]]. Handshake: [[What is a HandshakeInterceptor for WebSocket]].

```java
@Configuration
public class WebSocketSecurityConfig extends AbstractSecurityWebSocketMessageBrokerConfigurer {

	@Override
	protected void configureInbound(MessageSecurityMetadataSourceRegistry messages) {
		messages.simpDestMatchers("/user/queue/errors").permitAll()
				.simpDestMatchers("/admin/**").hasRole("ADMIN")
				.anyMessage().authenticated();
	}
}
```

**Listing 1.** Conceptual: Security 6.4 javadoc sample (class still present, **`@Deprecated`**). Security 7: this type is **gone**; use `@EnableWebSocketSecurity` + `AuthorizationManager<Message<?>>`.

`sameOriginDisabled() { return true; }` **disables** CSRF on CONNECT so other origins can connect — it is **not** “enable security.” Empty `configureInbound` registers **no** destination rules.

```d2
direction: down
legacy: "AbstractSecurityWebSocketMessageBrokerConfigurer" {
  width: 340
  height: 40
  style.fill: "#fff3e0"
}
now: "@EnableWebSocketSecurity\nAuthorizationManager<Message>" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}

legacy -> now: "5.8+ / required in 7"
```

**Fig. 1.** Interview dumps that stop at `configureInbound` are describing the **pre-5.8** API. Security 6.4 still compiles it as deprecated.

> [!warning]sameOriginDisabled true turns CSRF off
> Override returning **true** skips `CsrfChannelInterceptor`. Combined with open CORS this is the **cross-site WebSocket** case Security is trying to prevent. Do not treat the class as current API on Security **7**.

> [!tip] Interview answer
> **`AbstractSecurityWebSocketMessageBrokerConfigurer` was the Security 4–6 way to authorize STOMP: `configureInbound` matchers plus CSRF on CONNECT unless `sameOriginDisabled()`.** It is deprecated for `@EnableWebSocketSecurity` and removed in Security 7. `HttpSecurity` still does not replace `configureInbound` / `AuthorizationManager`.
