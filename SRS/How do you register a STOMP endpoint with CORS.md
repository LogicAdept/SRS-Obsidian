<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #SRS

# How do you register a STOMP endpoint with CORS?

> [!abstract] Short answer
> In **`registerStompEndpoints`**, **`registry.addEndpoint("/portfolio")`** then **`setAllowedOriginPatterns`** (5.3.2+) or **`setAllowedOrigins`**. Default (Framework **4.1.5+**) is **same-origin** for WebSocket and SockJS — a browser on another origin will not complete the handshake. **`"*"`** allows all origins. This is the **handshake `Origin` check**, not authorization of STOMP **`/app`** destinations.

## Handshake CORS, not message security

`StompWebSocketEndpointRegistration.setAllowedOrigins`: scheme-qualified origins; CORS does **not** allow `"*"` together with **`allowCredentials=true`** — use **patterns** instead. If **both** are set, **patterns win**. Restricted origins **disable SockJS iframe** transports (IE 6–9). Optional **`.withSockJS()`**. Handshake: [[How does the WebSocket handshake work in Spring]]. SockJS: [[What is SockJS]]. Enable STOMP: [[How do you configure a STOMP broker in Spring]]. Annotation: [[What is the EnableWebSocketMessageBroker annotation]].

```java
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfiguration implements WebSocketMessageBrokerConfigurer {

	@Override
	public void registerStompEndpoints(StompEndpointRegistry registry) {
		registry.addEndpoint("/portfolio")
				.setAllowedOriginPatterns("*");
	}
}
```

**Listing 1.** Conceptual: allow any browser origin. Prefer an explicit pattern list in production. Do **not** paste `setAllowedOrigins` with a full URL in a flashcard if you need a credentials-friendly setup — that is what **patterns** are for.

The check is aimed at **browsers**. Non-browser clients can spoof `Origin` (RFC 6454). Spring Security **`simpDestMatchers("/app/**")`** is a **different** layer after CONNECT.

```d2
direction: down
ep: "addEndpoint /portfolio" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
cors: "setAllowedOriginPatterns / Origins" {
  width: 300
  height: 40
  style.fill: "#fff3e0"
}
hs: "HTTP Upgrade 101" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}

ep -> cors
cors -> hs
```

**Fig. 1.** Origin policy applies to the **handshake URL**, not to `/topic` strings inside STOMP frames.

> [!warning]Star is not `/app` authorization
> `setAllowedOrigins("*")` only relaxes **browser Origin** on the socket URL. Anyone who can open the socket still SEND to `/app` unless you add **message** security. Same-origin default also means a local HTML file or another port is a **cross-origin** request.

> [!tip] Interview answer
> **CORS for STOMP is `addEndpoint(…).setAllowedOriginPatterns(…)` (or `setAllowedOrigins`).** Default is same-origin since 4.1.5. `*` allows all handshake origins and is not a substitute for authenticating destinations. SockJS plus a tight origin list drops iframe transports.
