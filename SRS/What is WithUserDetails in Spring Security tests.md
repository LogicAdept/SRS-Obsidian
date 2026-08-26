<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Framework/Testing #Java/Annotations #SRS

# What is WithUserDetails in Spring Security tests?

> [!abstract] Short answer
> **`@WithUserDetails`** (`org.springframework.security.test.context.support`, module **`spring-security-test`**) plants an **`Authentication`** whose **principal is whatever your `UserDetailsService` returns** for a username. Default username is **`user`**. Token type is **`UsernamePasswordAuthenticationToken`**. Unlike **`@WithMockUser`**, the username **must exist** in that service — no synthesized Security **`User`**. Use it when production code **casts** the principal to a **custom `UserDetails` type**. Optional: **`userDetailsServiceBeanName`**, **`setupBefore`**.

## Lookup, not a fake `User`

`WithUserDetailsSecurityContextFactory` **`@Autowired`s `UserDetailsService`** and calls **`loadUserByUsername`**. Empty bean name → lookup **by type** (exactly **one** `UserDetailsService` bean). Named bean → that bean only. The factory then builds an authenticated token from the returned **`UserDetails`** (password and authorities come from **that object**).

Class-level placement applies to every method. Default setup is **`TestExecutionListener.beforeTestMethod`** (before JUnit `@Before`); **`setupBefore = TestExecutionEvent.TEST_EXECUTION`** runs after `@Before`. Meta-annotations work (`@WithUserDetails("admin")` wrapped as `@WithAdmin`). vs fake user: [[What is the difference between WithMockUser and WithUserDetails]]. Purpose of the fake: [[What is the purpose of WithMockUser in Spring Security tests]]. Method security: [[How do you test method security without replacing SecurityFilterChain]]. MockMvc: [[How do you test Spring Security in MockMvc tests]].

```java
@Test
@WithUserDetails
void getMessageWithUserDetails() {
    String message = messageService.getMessage();
    assertThat(message).contains("user");
}
```

**Listing 1.** Conceptual Security **7.1**. Looks up username **`user`**.

```java
@Test
@WithUserDetails(value = "customUsername", userDetailsServiceBeanName = "myUserDetailsService")
void getMessageWithUserDetailsServiceBeanName() {
    Object principal = SecurityContextHolder.getContext().getAuthentication().getPrincipal();
    assertThat(principal).isInstanceOf(CustomUserDetails.class);
}
```

**Listing 2.** Conceptual: principal type is **your** `UserDetails` implementation, not `org.springframework.security.core.userdetails.User`.

```d2
direction: down
ann: "@WithUserDetails(\"alice\")" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
uds: "UserDetailsService.loadUserByUsername" {
  width: 320
  height: 45
  style.fill: "#fff3e0"
}
holder: "SecurityContextHolder\n(test thread)" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}

ann -> uds -> holder
```

**Fig. 1.** Missing username → lookup fails. `@WithMockUser` never calls this bean.

> [!warning] The user must exist
> Unlike `@WithMockUser`, **`@WithUserDetails` requires the user to exist**. Seed an in-memory `UserDetailsService`, `@Sql`, or a test `@Bean`. A missing name is **not** a silent anonymous run.

> [!warning] Slice may have no `UserDetailsService`
> `@WebMvcTest` does **not** scan `@Service`. **`@Import`** the service (or a test in-memory implementation) or the factory has **nothing to `@Autowired`**. Several `UserDetailsService` beans without **`userDetailsServiceBeanName`** fail the type lookup.

> [!warning] Test thread only
> **`RANDOM_PORT`** HTTP is a **different** thread. `@WithUserDetails` **does not** ride along — authenticate the request (Basic / bearer) or stay on MockMvc / in-process method security.

> [!tip] Interview answer
> **`@WithUserDetails` loads the principal from a `UserDetailsService` so the test gets your custom `UserDetails` type.** The username must exist. `@WithMockUser` is enough when the code only needs a generic Security `User`.
