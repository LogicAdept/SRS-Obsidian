<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What is `CorsFilter` in Spring Security?

> [!abstract] Short answer
> **`org.springframework.web.filter.CorsFilter`** — Spring Framework’s CORS filter — inserted **early** in the `SecurityFilterChain` by **`http.cors(...)`**. It answers browser **preflight** (`OPTIONS`, **no cookies**) **before** CSRF and authentication. **`http.cors(Customizer.withDefaults())`** uses a bean named **`corsFilter`**, else a **`CorsConfigurationSource`**. Without it, an SPA on another origin fails preflight even when JWT/form login is correct. CORS is **not** authentication.

## Before CSRF and login

```d2
direction: right
hdr: "HeaderWriterFilter" {
  width: 180
  height: 40
  style.fill: "#eceff1"
}
cors: "CorsFilter" {
  width: 140
  height: 40
  style.fill: "#e8f5e9"
}
csrf: "CsrfFilter" {
  width: 120
  height: 40
  style.fill: "#fff3e0"
}
auth: "login / Bearer / AuthorizationFilter" {
  width: 280
  height: 40
  style.fill: "#fce4ec"
}

hdr -> cors
cors -> csrf
csrf -> auth
```

**Fig. 1.** `FilterOrderRegistration` puts `CorsFilter` after headers and **before** `CsrfFilter`. A preflight has **no** `JSESSIONID`; if Security authenticates first, the user looks anonymous and the browser never gets `Access-Control-Allow-*`. See [[How do you configure CORS on HttpSecurity]] and [[What is FilterChainProxy and DelegatingFilterProxy]].

```java
@Bean
UrlBasedCorsConfigurationSource corsConfigurationSource(
        @Value("${app.cors.origin}") String spaOrigin) {
    CorsConfiguration cfg = new CorsConfiguration();
    cfg.setAllowedOrigins(List.of(spaOrigin));
    cfg.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
    cfg.setAllowedHeaders(List.of("*"));
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/**", cfg);
    return source;
}

http.cors(Customizer.withDefaults());
```

**Listing 1.** `withDefaults()` picks up that `CorsConfigurationSource` (or a `corsFilter` bean). XML `<cors>` is the same: supply a `CorsFilter` or `CorsConfigurationSource`; with MVC it can reuse MVC’s source. `addCorsMappings` **alone** is too late once `FilterChainProxy` sits in front. See [[What is BearerTokenAuthenticationFilter]].

A `@Component` `CorsFilter` can run **twice** (container + chain) unless `FilterRegistrationBean.setEnabled(false)` — same Boot trap as other servlet `Filter` beans.

> [!warning] CORS does not log anyone in
> `Access-Control-Allow-Origin` is a **browser** gate. A valid Bearer token still fails if preflight never leaves `CorsFilter` with the right headers. `allowCredentials(true)` cannot be paired with origin `*` (use an explicit origin list). `permitAll` on `OPTIONS` is not a substitute for `http.cors`.

> [!tip] Interview answer
> CorsFilter is Spring Framework’s CORS filter, added early by http.cors so OPTIONS preflight is handled before CSRF and authentication. Wire a CorsConfigurationSource or a corsFilter bean. MVC CORS mappings are too late if Spring Security is first. CORS is not login.
