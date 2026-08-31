<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# How do you require HTTPS with Spring Security?

> [!abstract] Short answer
> Call **`http.redirectToHttps(Customizer.withDefaults())`** on the `SecurityFilterChain` (XML: `requires-channel="https"`). That **redirects HTTP to HTTPS**. It does **not** terminate TLS — the servlet container or a reverse proxy still needs a certificate. `requiresChannel().anyRequest().requiresSecure()` is the **deprecated** spelling of the same channel check.

## Redirect, then TLS somewhere else

Spring Security **does not open HTTPS sockets**. It looks at the request scheme and, if you asked for HTTPS, issues a redirect. Default `PortMapper`: **80→443**, **8080→8443**.

```java
@Bean
SecurityFilterChain app(HttpSecurity http) throws Exception {
    http.redirectToHttps(Customizer.withDefaults());
    return http.build();
}
```

**Listing 1.** Current DSL (`HttpsRedirectConfigurer`). Require HTTPS for **every** request; mixing HTTP and HTTPS on purpose is supported but a bad default (session cookies on HTTP). See [[How do you configure a SecurityFilterChain bean in Spring Security 6]].

```java
http.requiresChannel((channel) -> channel.anyRequest().requiresSecure());
```

**Listing 2.** Pre-`redirectToHttps` API ([[What is ChannelProcessingFilter]]). Same idea; javadoc says use Listing 1. XML: `<intercept-url pattern="/**" … requires-channel="https"/>`.

**HSTS** (`Strict-Transport-Security`) is **on by default** via header writers — that tells browsers to stick to HTTPS **after** they have already used it. It is not a substitute for the redirect.

```d2
direction: down
client: "Client HTTP" {
  width: 160
  height: 40
  style.fill: "#e3f2fd"
}
sec: "redirectToHttps\n302 to HTTPS port" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
tls: "Container or proxy TLS\ncertificate lives here" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}

client -> sec
sec -> tls
```

**Fig. 1.** Security redirects; TLS is a listener (or the load balancer) in front.

> [!warning] No certificate, no HTTPS
> `requiresSecure()` / `redirectToHttps` never create a keystore. If nothing listens on the mapped HTTPS port, the redirect **fails or loops**. Terminate TLS on the server or the proxy, then let Security see `https`.

> [!warning] Proxies must pass the original scheme
> A load balancer that talks HTTP to the app makes every request look like `http` unless **`Forwarded` / `X-Forwarded-Proto`** (and host) are applied **and** untrusted copies are stripped at the edge. Use `ForwardedHeaderFilter` or Boot `server.forward-headers-strategy`. Trusting those headers **without** a proxy lets clients spoof HTTPS.

> [!tip] Interview answer
> Require HTTPS with redirectToHttps on HttpSecurity — that redirects HTTP; it does not install TLS. The old requiresChannel anyRequest requiresSecure is the same channel rule. Behind a proxy, forwarded headers have to show the original scheme or you redirect forever.
