<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What is `intercept-url` in Spring Security?

> [!abstract] Short answer
> The XML **`<intercept-url>`** child of **`<http>`**: one **pattern** (and optional **method**) plus **`access`** attributes. The namespace builds an ordered `RequestMatcher` list (`FilterInvocationSecurityMetadataSource` for [[What is FilterSecurityInterceptor]]; today XML can drive [[What is AuthorizationFilter in Spring Security]]). **First match wins** — specific patterns before `/**`. Java’s `authorizeHttpRequests` / `requestMatchers` / `hasRole` is the same idea, not a different security model.

## Pattern → access, in document order

```d2
direction: down
xml: "<http>\n<intercept-url> lines" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
map: "ordered RequestMatcher → access" {
  width: 280
  height: 40
  style.fill: "#fff3e0"
}
enf: "FilterSecurityInterceptor\nor AuthorizationFilter" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}

xml -> map
map -> enf
```

**Fig. 1.** Namespace: matching is **declaration order**. `requires-channel` on any line also adds [[What is ChannelProcessingFilter]]. See [[Does intercept-url order matter in Spring Security]] and [[Why does authorization matcher order matter in Spring Security]].

`access` is a comma-separated list of **config attributes** (role names like `ROLE_ADMIN`, or expressions `hasRole('ADMIN')`, `permitAll`, `authenticated`, `denyAll`). `IS_AUTHENTICATED_ANONYMOUSLY` needs the `<anonymous>` filter. `pattern` uses the `<http request-matcher>` strategy (MVC/`PathPattern` when Spring MVC is on the classpath). Optional `method="GET"`; a **method-specific** line beats the same pattern without a method.

```xml
<http>
    <intercept-url pattern="/static/**" access="permitAll"/>
    <intercept-url pattern="/admin/**" access="hasRole('ADMIN')"/>
    <intercept-url pattern="/**" access="denyAll"/>
</http>
```

```java
http.authorizeHttpRequests((authorize) -> authorize
        .requestMatchers("/static/**").permitAll()
        .requestMatchers("/admin/**").hasRole("ADMIN")
        .anyRequest().denyAll());
```

**Listing 1.** Same first-match list. `hasRole("ADMIN")` still means authority **`ROLE_ADMIN`**. See [[How do you configure authorizeHttpRequests in Spring Security 6]] and [[How do you restrict URL access by role in Spring Security]].

> [!warning] Read the pattern, not the filename
> `admin.jsp` is not “admin-only” unless a matching `<intercept-url>` says so. A leading `/**` makes every later line dead. Unmatched requests are **deny**, not public. Java `antMatchers` / `authorizeRequests` is the old spelling.

> [!tip] Interview answer
> intercept-url is the XML way to map URL patterns to access attributes, first-match in document order. Put /admin/** above /**. In Spring Security 6 Java config the same list is authorizeHttpRequests plus requestMatchers. It is authorization inside one http/SecurityFilterChain, not which chain FilterChainProxy picks.
