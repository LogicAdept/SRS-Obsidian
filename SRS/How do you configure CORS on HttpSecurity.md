<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# How do you configure CORS on `HttpSecurity`?

> [!abstract] Short answer
> Enable it on the chain with **`http.cors(Customizer.withDefaults())`** and give Spring Security a **`CorsConfigurationSource`**. A **`UrlBasedCorsConfigurationSource` `@Bean`** is enough for auto-wiring. That inserts **`CorsFilter` early**, so browser **preflight** (`OPTIONS`, no cookies) is answered before authentication. MVC `addCorsMappings` alone is not enough once the security chain is in front.

CORS has to run **before** the rest of Spring Security. A CORS preflight has **no** `JSESSIONID` (or other cookies). If the security chain sees that request first, the user looks unauthenticated and the preflight is rejected — the browser never gets `Access-Control-Allow-*`.

```java
@Bean
UrlBasedCorsConfigurationSource corsConfigurationSource(
        @Value("${app.cors.origin}") String spaOrigin) {
    CorsConfiguration configuration = new CorsConfiguration();
    configuration.setAllowedOrigins(List.of(spaOrigin));
    configuration.setAllowedMethods(List.of("GET", "POST"));
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/**", configuration);
    return source;
}
```

**Listing 1.** Spring Security auto-enables CORS when this **`UrlBasedCorsConfigurationSource`** bean is present (`HttpSecurity.cors` then uses a bean named `corsFilter`, else a `corsConfigurationSource`). `app.cors.origin` is the SPA’s origin (scheme, host, port).

```java
@Bean
SecurityFilterChain app(HttpSecurity http) throws Exception {
    http.cors(Customizer.withDefaults())
        .authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated());
    return http.build();
}
```

**Listing 2.** `cors(withDefaults())` on [[How do you configure a SecurityFilterChain bean in Spring Security 6]]. If Spring MVC is on the classpath and you **omit** Listing 1, Security reuses **MVC’s** CORS config. XML is `<cors />` or `<cors configuration-source-ref="…"/>`.

`HttpSecurity.cors(Customizer)` adds [[What is CorsFilter in Spring Security]] (or, if you set `preFlightRequestHandler`, `PreFlightRequestFilter` **before** `CorsFilter`). Do **not** set both `configurationSource` and `preFlightRequestHandler` on the same `CorsConfigurer` — startup fails.

Several `CorsConfigurationSource` beans: Security **will not** pick one automatically. Pass the source on the chain:

```java
http.securityMatcher("/api/**")
    .cors((cors) -> cors.configurationSource(apiConfigurationSource()));
```

**Listing 3.** Per-[[What is SecurityFilterChain]] CORS when one global bean is ambiguous.

```d2
direction: down
browser: "Browser OPTIONS preflight\n(no cookies)" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
cors: "CorsFilter (from http.cors)\nAccess-Control-Allow-*" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
sec: "Rest of SecurityFilterChain\nauthentication · authorization" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
ok: "Real GET/POST with cookies" {
  width: 260
  height: 45
  style.fill: "#fce4ec"
}

browser -> cors
cors -> sec: "preflight handled first"
sec -> ok
```

**Fig. 1.** Preflight must hit `CorsFilter` before authentication, or the browser never sends the credentialed request.

`.cors(CorsConfigurer::disable)` drops **Spring Security’s** CORS support. It does **not** turn off CORS in the browser; cross-origin JS simply cannot talk to the API until you enable a configuration source again.

> [!warning] MVC `addCorsMappings` does not run first
> `WebMvcConfigurer.addCorsMappings` lives in DispatcherServlet. `FilterChainProxy` runs **before** that. Without `http.cors(...)` (and a `UrlBasedCorsConfigurationSource` or MVC integration via `withDefaults()`), Security answers the cookieless preflight and the MVC mapping never sees it.

> [!tip] Interview answer
> Configure CORS on HttpSecurity with cors(withDefaults()) plus a UrlBasedCorsConfigurationSource bean so CorsFilter handles preflight before authentication. Preflight has no session cookie; if Security runs first the call looks anonymous and fails. MVC-only CORS is too late unless you hook it through http.cors.
