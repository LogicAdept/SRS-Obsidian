<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Spring/Framework/Testing #Java/Spring/Framework/WebMvc #Testing/Mocking #SRS

# What is SecurityMockMvcRequestPostProcessors?

> [!abstract] Short answer
> **`SecurityMockMvcRequestPostProcessors`** (`org.springframework.security.test.web.servlet.request`, module **`spring-security-test`**, since **4.0**) is a factory of MockMvc **`RequestPostProcessor`s**. Static import **`SecurityMockMvcRequestPostProcessors.*`**, then **`.with(csrf())`**, **`.with(user("admin").roles("ADMIN"))`**, **`.with(httpBasic("user","password"))`**, **`.with(anonymous())`**, plus JWT / OAuth2 helpers. **`user(…)`** plants a fake **`User`** on **this request**. **`httpBasic`** only sets the **`Authorization`** header and lets the **filter chain** authenticate.

## Per-request, not class-level annotations

MockMvc’s **`RequestPostProcessor`** mutates the **`MockHttpServletRequest`** after builders finish. Security’s processors cover two jobs:

- **CSRF** — **`csrf()`** puts a **valid `CsrfToken`** on the request (parameter). **`asHeader()`** / **`useInvalidToken()`** for header vs rejection tests. Required for **unsafe methods** when CSRF is on.
- **Who is calling** — **`user(username)`** (need **not** exist): **`UsernamePasswordAuthenticationToken`** + Security **`User`**. Fluent **`.password` / `.roles`**. Overload **`user(UserDetails)`**. **`anonymous()`**, **`authentication(Authentication)`**, **`securityContext(…)`**, **`jwt()`**, **`oauth2Login()`**, **`oidcLogin()`**, **`opaqueToken()`**.

**`httpBasic(username, password)`** Base64-encodes **`Authorization: Basic …`** and **attempts HTTP Basic** — the user **must** satisfy your `UserDetailsService` / `{noop}` password. That is **not** the same as **`user("user")`**.

`user(…)` attaches the principal to the **request**. For it to reach **`SecurityContextHolder`**, MockMvc must include the persistence filter: **`.apply(springSecurity())`**, **`FilterChainProxy`**, or a manual **`SecurityContextPersistenceFilter`** (`standaloneSetup`). Boot **`@WebMvcTest`** already does this. Class-level alternative: **`@WithMockUser`**. How-to: [[How do you test Spring Security in MockMvc tests]]. Annotations: [[What is the purpose of WithMockUser in Spring Security tests]]. Driver: [[What is MockMvc]]. Anonymous annotation: [[What is WithAnonymousUser]].

```java
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.*;

mvc.perform(post("/").with(csrf()).with(user("admin").roles("ADMIN")));
```

**Listing 1.** Conceptual Security **7.1**. POST needs **CSRF and** a user when both are enabled.

```java
mvc.perform(get("/").with(httpBasic("user", "password")));
```

**Listing 2.** Conceptual: header **`Authorization: Basic dXNlcjpwYXNzd29yZA==`**. Goes through the **Basic** filter, not a planted `User`.

```d2
direction: down
req: ".with(csrf()) / user() / httpBasic()" {
  width: 320
  height: 45
  style.fill: "#e3f2fd"
}
mvc: "MockMvc + springSecurity()" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}
chain: "SecurityFilterChain" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}

req -> mvc -> chain
```

**Fig. 1.** Post-processors ride **this** `perform`. `@WithMockUser` plants the holder for the **test method** (still needs the persistence filter).

> [!warning] Missing `csrf()` is 403, not 401
> A correct **`user(…)`** or **`@WithMockUser`** on **POST** still **403**s when CSRF is enabled and the token is absent.

> [!warning] `user()` without `springSecurity()`
> The fake user sits on the **request** and **never** reaches the holder. Manual **`standaloneSetup`** is the usual miss. Boot’s MockMvc auto-config already applies Security.

> [!warning] `httpBasic` is not `user()`
> **`httpBasic`** does **not** skip the `AuthenticationProvider`. Wrong password → **401**. **`user("ghost")`** does not need that account to exist.

> [!tip] Interview answer
> **`SecurityMockMvcRequestPostProcessors` — `.with(csrf())`, `.with(user(…))`, `.with(httpBasic(…))` on MockMvc.** `user()` fakes a principal on the request; `httpBasic` only sets the header. Apply `springSecurity()` so the persistence filter copies it into `SecurityContextHolder`.
