<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Framework/Testing #Java/Annotations #SRS

# What is the difference between WithMockUser and WithUserDetails?

> [!abstract] Short answer
> Both plant an **`Authentication` in `SecurityContextHolder`** for the test (module **`spring-security-test`**). **`@WithMockUser`** **synthesizes** Security’s **`User`**: username/roles/authorities you pass, **no `UserDetailsService`**, user **need not exist**. **`@WithUserDetails`** **loads** the principal from a **`UserDetailsService` bean** — the username **must exist**. Use **`@WithUserDetails`** when the app **casts** the principal to a **custom `UserDetails` type**. Default lookup username is **`user`**; override with **`@WithUserDetails("customUsername")`** or **`userDetailsServiceBeanName`**.

## Fake `User` vs lookup

`@WithMockUser` is the easy start (Security *Testing Method Security*). Token type is still **`UsernamePasswordAuthenticationToken`**. **`roles`** get **`ROLE_`**; **`authorities`** do not. No password check, no `AuthenticationProvider`.

`@WithUserDetails` exists because many apps **reduce coupling** by typing the principal as **`CustomUserDetails`**. The factory **`@Autowired`s `UserDetailsService`** and calls **`loadUserByUsername`**. Unlike `@WithMockUser`, **the user must exist** in that service (in-memory test users, `@Sql` seed, …). Class-level placement works for both.

Same thread-only rule: **`RANDOM_PORT`** HTTP **does not** see these annotations. MockMvc / in-process method security does. Purpose: [[What is the purpose of WithMockUser in Spring Security tests]]. Lookup cue: [[What is WithUserDetails in Spring Security tests]]. Anonymous: [[What is WithAnonymousUser]]. Method security: [[How do you test method security without replacing SecurityFilterChain]]. MockMvc: [[How do you test Spring Security in MockMvc tests]].

```java
@Test
@WithMockUser(username = "admin", roles = {"USER", "ADMIN"})
void withSynthesizedUser() { /* principal is org.springframework.security.core.userdetails.User */ }
```

**Listing 1.** Conceptual Security **7.1**. No `UserDetailsService` call.

```java
@Test
@WithUserDetails(value = "customUsername", userDetailsServiceBeanName = "myUserDetailsService")
void withLookedUpUser() {
    Object principal = SecurityContextHolder.getContext().getAuthentication().getPrincipal();
    assertThat(principal).isInstanceOf(CustomUserDetails.class);
}
```

**Listing 2.** Conceptual: principal is **whatever the service returned**. Missing username → lookup **fails**.

```d2
direction: down
mock: "@WithMockUser\nsynthesize User" {
  width: 260
  height: 45
  style.fill: "#e3f2fd"
}
uds: "@WithUserDetails\nUserDetailsService.loadUserByUsername" {
  width: 340
  height: 50
  style.fill: "#fff3e0"
}
ctx: "SecurityContextHolder" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}

mock -> ctx
uds -> ctx
```

**Fig. 1.** Same holder, different principal type and data (account flags, custom fields).

> [!warning] `@WithUserDetails` is not optional username sugar
> If **`customUsername` is absent**, the test **explodes at lookup**. `@WithMockUser("ghost")` **always** succeeds.

> [!warning] Casting `User` to your type
> `@WithMockUser` then **`ClassCastException`** in the controller/service. That is the reason `@WithUserDetails` exists.

> [!warning] Slice may not have a `UserDetailsService`
> `@WebMvcTest` does **not** scan `@Service`. **`@Import`** the service (or a test in-memory `UserDetailsService`) or `@WithUserDetails` has **nothing to call**. `@WithMockUser` does not need that bean.

> [!tip] Interview answer
> **`@WithMockUser` fakes a `User`. `@WithUserDetails` loads the real `UserDetails` from a `UserDetailsService` — the user must exist.** Pick WithUserDetails when the code needs your custom principal; otherwise WithMockUser is enough.
