<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Framework/WebMvc #Java/Annotations #Java/Spring/Boot #SRS

# What is CORS in Spring Boot?

> [!abstract] Short answer
> **CORS is a browser rule:** scripts on origin A may not read responses from origin B unless the **server** sends CORS headers (`Access-Control-Allow-Origin`, …). Spring MVC applies that after **`HandlerMapping`** (`@CrossOrigin` and/or **`WebMvcConfigurer.addCorsMappings`**). With **Spring Security**, CORS must run **before** authentication: declare a **`UrlBasedCorsConfigurationSource`** bean or **`http.cors(withDefaults())`** so **OPTIONS preflight** (no cookies) is not treated as anonymous and rejected.

## Browser policy, then Spring headers

Without an explicit CORS config, MVC **does not** add CORS headers; the browser **rejects** the call. Preflight is handled on the mapping; simple/actual requests get headers if config matches.

**`@CrossOrigin`** (4.2): class or method. Defaults: **all origins**, all headers, methods **the handler is mapped to**, **`allowCredentials` off**, **`maxAge` 1800s**. Local + global config is **additive** on lists; **`allowCredentials` / `maxAge`** use the **local** value. Credentials + origin `"*"` is invalid — use **`originPatterns`** or explicit hosts.

Global MVC: implement **`WebMvcConfigurer.addCorsMappings`** (not deprecated `WebMvcConfigurerAdapter`). Global defaults: all origins, all headers, **GET / HEAD / POST**.

```java
@CrossOrigin(origins = "https://app.example.com")
@GetMapping("/account/{id}")
public Account retrieve(@PathVariable Long id) { … }
```

**Listing 1.** Conceptual method-level permit. MVC config: [[What is WebMvcConfigurer in Spring MVC]]. Filters vs interceptors: [[How do servlet filters interceptors and AOP differ in Spring]]. Annotations overview: [[What do common Spring Web MVC annotations do]].

```java
@Bean
UrlBasedCorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration configuration = new CorsConfiguration();
    configuration.setAllowedOrigins(List.of("https://example.com"));
    configuration.setAllowedMethods(List.of("GET", "POST"));
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/**", configuration);
    return source;
}
```

**Listing 2.** Conceptual Security integration: this bean type is what Security auto-wires into **`CorsFilter`** (preflight has **no** `JSESSIONID`). If you only use MVC CORS, `http.cors(Customizer.withDefaults())` reuses MVC’s map.

```d2
direction: down
br: "browser\nOrigin: https://app.example.com" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
opt: "OPTIONS preflight" {
  width: 220
  height: 40
  style.fill: "#fff3e0"
}
sec: "CorsFilter\nbefore Security auth" {
  width: 260
  height: 50
  style.fill: "#fce4ec"
}
mvc: "HandlerMapping CORS\n@CrossOrigin / CorsRegistry" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}

br -> opt
opt -> sec
sec -> mvc
```

**Fig. 1.** Security CORS first so OPTIONS is not a 401. MVC CORS still stamps headers on mapped controllers.

> [!warning] `WebMvcConfigurerAdapter` is gone
> Dump samples extend it. Since Spring 5.0 implement **`WebMvcConfigurer`** (default methods).

> [!warning] Credentials + `"*"`
> `allowCredentials(true)` with `allowedOrigins("*")` fails the CORS contract. List hosts or use **`allowedOriginPatterns`**.

> [!warning] Security without CORS
> A filter chain that authenticates **before** CORS rejects cookie-less preflight. Enable **`cors()`** and a **`CorsConfigurationSource`**. Disabling `.cors()` does **not** turn off the browser; it only stops Spring from answering CORS.

> [!tip] Interview answer
> **CORS is the server telling the browser which other origins may call it.** In Boot: `@CrossOrigin` and/or `addCorsMappings`, and with Security a **`CorsConfigurationSource`** so **OPTIONS** never hits auth. It is a **browser** check — tools that are not browsers do not enforce it.
