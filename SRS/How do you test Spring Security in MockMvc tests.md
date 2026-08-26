<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Java/Spring/Security #Java/Annotations #SRS

# How do you test Spring Security in MockMvc tests?

> [!abstract] Short answer
> Keep Security **on**. `@WebMvcTest` **auto-configures Spring Security and MockMvc** when Security is on the classpath (Boot **4.1**). Run as a user with **`@WithMockUser`** from **`spring-security-test`**, or attach **`SecurityMockMvcRequestPostProcessors`** (`user(…)`, `httpBasic()`, `csrf()`, …) on the request. Need a **real `UserDetails` type** from your `UserDetailsService`? **`@WithUserDetails`**. There is **no `secure = false`** on `@WebMvcTest`. Manual `MockMvcBuilders.webAppContextSetup` needs **`.apply(springSecurity())`**.

## Filter chain stays; you fake the principal

Unauthenticated MockMvc calls hit the **`SecurityFilterChain`**. Typical outcomes: **401** (HTTP Basic / JWT / `httpBasic`) or **302** to login (form). `@WithMockUser` (method or class) puts a **`UsernamePasswordAuthenticationToken`** whose principal is Security’s **`User`**. Defaults: username **`user`**, password **`password`**, one authority **`ROLE_USER`**. `roles = "ADMIN"` becomes **`ROLE_ADMIN`**. Use **`authorities`** when you **do not** want the `ROLE_` prefix.

`@WithUserDetails` loads the user from a **`UserDetailsService` bean** — the username **must exist**. Per-request alternative: static import **`SecurityMockMvcRequestPostProcessors.*`** and **`.with(user("admin").roles("ADMIN"))`**. CSRF is on by default for **unsafe methods**: **`.with(csrf())`** (or **`asHeader()`** / **`useInvalidToken()`**).

`@WebMvcTest` scans **`WebSecurityConfigurer` / `SecurityFilterChain`** types it can see. A `@Bean` `SecurityFilterChain` on a mixed `@Configuration` that the slice **does not scan** is **missing** until **`@Import(YourSecurityConfig.class)`**. Split security config from DataSource beans so the slice does not pull Hikari. Annotations: [[What is the purpose of WithMockUser in Spring Security tests]]. Post-processors: [[What is SecurityMockMvcRequestPostProcessors]]. Method security without a permit-all test chain: [[How do you test method security without replacing SecurityFilterChain]]. Slice: [[How do you test a Spring MVC controller in isolation]].

```java
@WebMvcTest(UserController.class)
class MySecurityTests {

    @Autowired MockMvcTester mvc;

    @Test
    @WithMockUser(roles = "ADMIN")
    void requestProtectedUrlWithUser() {
        assertThat(this.mvc.get().uri("/")).doesNotHaveFailed();
    }
}
```

**Listing 1.** Conceptual Boot **4.1** how-to. Hamcrest: `mockMvc.perform(get("/")).andExpect(status().isOk())`. Class-level `@WithMockUser` covers every method; **`@WithAnonymousUser`** overrides one of them.

```java
mvc.perform(post("/").with(csrf()).with(user("user").roles("USER")));
```

**Listing 2.** Conceptual Security **7.1** MockMvc: CSRF token **and** a request-scoped user. Missing **`csrf()`** on POST is **403**, not a role miss.

```d2
direction: down
mvc: "MockMvc / MockMvcTester" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
chain: "SecurityFilterChain\n(always on in the slice)" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
user: "@WithMockUser /\nuser() / @WithUserDetails" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}

mvc -> chain
user -> chain
```

**Fig. 1.** The test does not log in through `/login`. It **plants** `SecurityContext` (annotations need `springSecurity()` / Boot’s MockMvc auto-config so the **persistence filter** sees it).

> [!warning] `secure = false` does not compile
> Boot **4** `@WebMvcTest` has **`controllers`**, not **`secure`**. Do not disable the chain to “make the test green.”

> [!warning] CSRF is not authentication
> A correct `@WithMockUser` on **POST** still **403**s without **`csrf()`** when CSRF is enabled.

> [!warning] `@WithMockUser` skips your `AuthenticationProvider`
> No password check, no custom principal. If the controller casts to **`YourUser`**, use **`@WithUserDetails`** (user must exist) or a custom **`@WithSecurityContext`**. These annotations populate the **test thread**; **`RANDOM_PORT`** HTTP is a **different thread** — send Basic / a bearer token on that request.

> [!tip] Interview answer
> **`@WebMvcTest` plus `@WithMockUser` (or `.with(user(…))`) from `spring-security-test`.** Security stays enabled. Add **`csrf()`** on state-changing MockMvc calls. Do not ship a permit-all `SecurityFilterChain` in `@TestConfiguration` just to dodge 401.
