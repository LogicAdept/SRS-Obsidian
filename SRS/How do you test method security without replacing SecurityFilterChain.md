<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Security/FilterChain #Java/Spring/Framework/Testing #Java/Annotations #SRS

# How do you test method security without replacing SecurityFilterChain?

> [!abstract] Short answer
> Keep the production **`SecurityFilterChain`**. Plant a user with **`@WithMockUser`** (or **`@WithUserDetails`**) from **`spring-security-test`** and invoke the **`@PreAuthorize` / `@Secured` bean through the Spring proxy**. Official samples call the service directly — **no MockMvc, no permit-all test chain**. HTTP tests can still use **`@WebMvcTest` / `@SpringBootTest` + `@AutoConfigureMockMvc`** with the **same** annotations so the filter chain **and** method security both see that `SecurityContext`. Do **not** register a second **`anyRequest().permitAll()`** `SecurityFilterChain` in `@TestConfiguration`.

## Fake the principal; leave URL rules alone

Method security is **AOP** (`@EnableMethodSecurity`). `WithSecurityContextTestExecutionListener` fills **`SecurityContextHolder`** before the test method (clears it after). Unauthenticated direct call: **`AuthenticationCredentialsNotFoundException`**. Authenticated but expression false: **`AccessDeniedException`**. Wrong role in the official `BankService` sample is the second case.

A nested **`@TestConfiguration` `@Bean SecurityFilterChain`** is **another** chain. `FilterChainProxy` runs **the first matching chain**; a permit-all matcher with **`@Order(1)`** (or any match-all that wins) **never runs production rules** — tests **200**, prod **401**. `@ActiveProfiles("test")` that loads a weaker chain is the **same** hole. Use a test profile only if it still **authorizes** the same way.

OAuth2: `@WithMockUser` does **not** call the IdP. For MockMvc JWT resource-server tests, use **`jwt()`** (and friends) on the request — still not a live token endpoint. HTTP MockMvc: [[How do you test Spring Security in MockMvc tests]]. Switch: [[What is EnableMethodSecurity]]. Why both layers: [[Why does method security still matter if URL rules exist]]. Annotation: [[What is the purpose of WithMockUser in Spring Security tests]].

```java
@Autowired BankService bankService;

@WithMockUser(roles = "ADMIN")
@Test
void readAccountWithAdminRoleThenInvokes() {
    Account account = this.bankService.readAccount("12345678");
}

@WithMockUser(roles = "WRONG")
@Test
void readAccountWithWrongRoleThenAccessDenied() {
    assertThatExceptionOfType(AccessDeniedException.class)
            .isThrownBy(() -> this.bankService.readAccount("12345678"));
}
```

**Listing 1.** Conceptual Security **7.1** method-security sample. Context must include **`@EnableMethodSecurity`**. `roles = "ADMIN"` is **`ROLE_ADMIN`**.

```java
@WebMvcTest(AccountController.class)
@Import(MethodSecurityConfig.class)
class AccountControllerSecurityTests {

    @Autowired MockMvc mockMvc;

    @Test
    @WithMockUser(roles = "ADMIN")
    void getAccountWhenAdminThenOk() throws Exception {
        mockMvc.perform(get("/accounts/12345678")).andExpect(status().isOk());
    }
}
```

**Listing 2.** Conceptual: HTTP still uses the **slice’s** (or app’s) **`SecurityFilterChain`**. `@Import` only if the slice **does not scan** the method-security `@Configuration`. No permit-all override.

```d2
direction: down
user: "@WithMockUser\nSecurityContextHolder" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
aop: "@PreAuthorize proxy\nAccessDeniedException" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
http: "SecurityFilterChain\nunchanged" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}

user -> aop
user -> http
```

**Fig. 1.** One fake user, two layers. Replacing the chain tests **neither**.

> [!warning] Permit-all `@TestConfiguration` is not a shortcut
> A second **`SecurityFilterChain`** is first-match, not a merge. Green tests with **`permitAll`** say nothing about production **401 / 403**.

> [!warning] Annotations stay on the test thread
> **`RANDOM_PORT`** handles HTTP on **another** thread. `@WithMockUser` **does not** ride along — send Basic / a bearer token (or stay on MockMvc).

> [!warning] No `@EnableMethodSecurity` means a green lie
> `@PreAuthorize` is then a **no-op**. Calling `this.secured()` **inside** the same class also skips the proxy.

> [!tip] Interview answer
> **Do not swap in a permit-all `SecurityFilterChain`.** Put **`@WithMockUser` on the test and call the secured bean** (or MockMvc with the real chain). You are testing **AOP authorization**, not a fake HTTP config. OAuth2 in CI: mock the user, do not hit the IdP.
