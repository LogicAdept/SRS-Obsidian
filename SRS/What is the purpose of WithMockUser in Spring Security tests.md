<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Java/Spring/Security #Java/Annotations #SRS

# What is the purpose of WithMockUser in Spring Security tests?

> [!abstract] Short answer
> **`@WithMockUser`** (`org.springframework.security.test.context.support`, module **`spring-security-test`**) plants a **fake authenticated user** in **`SecurityContextHolder`** for the test so you **do not log in** and **do not call your `AuthenticationProvider`**. Defaults: username **`user`**, password **`password`**, one authority **`ROLE_USER`**. The `Authentication` is a **`UsernamePasswordAuthenticationToken`**; the principal is Security’s **`User`**. Use it on MockMvc tests **and** on `@PreAuthorize` service tests. Need a **custom principal** from **`UserDetailsService`**? **`@WithUserDetails`**.

## Fake `User`, real filter chain / AOP

`WithSecurityContextTestExecutionListener` fills the context **before** the test method (clears after). **`roles = "USER"`** → **`ROLE_USER`**. **`authorities = "USER"`** is the string **`USER`** with **no** prefix. Class-level annotation applies to every method; **`@WithAnonymousUser`** overrides one of them. Meta-annotations (e.g. `@WithMockAdmin`) work.

MockMvc: Boot’s `@WebMvcTest` already wires Security test support. Manual **`MockMvcBuilders`** needs **`.apply(springSecurity())`** so the **persistence filter** sees the annotation. Per-request alternative: **`.with(user("admin").roles("ADMIN"))`**. How-to: [[How do you test Spring Security in MockMvc tests]]. vs lookup: [[What is the difference between WithMockUser and WithUserDetails]]. Method security: [[How do you test method security without replacing SecurityFilterChain]]. Anonymous: [[What is WithAnonymousUser]]. Post-processors: [[What is SecurityMockMvcRequestPostProcessors]].

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

**Listing 1.** Conceptual Boot **4.1** how-to. `roles = "ADMIN"` is **`ROLE_ADMIN`**.

```java
@Test
@WithMockUser
void getMessageWithMockUser() {
    String message = messageService.getMessage();
    assertThat(message).contains("user");
}
```

**Listing 2.** Conceptual Security **7.1** method-security sample. No MockMvc; AOP reads the same `SecurityContext`.

```d2
direction: down
ann: "@WithMockUser\nUsernamePasswordAuthenticationToken" {
  width: 320
  height: 50
  style.fill: "#e3f2fd"
}
holder: "SecurityContextHolder\n(test thread)" {
  width: 260
  height: 45
  style.fill: "#fff3e0"
}
use: "Filter chain / @PreAuthorize" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}

ann -> holder -> use
```

**Fig. 1.** Production login is skipped. The **chain stays on** — there is no `secure = false`.

> [!warning] Not your domain user type
> The principal is **`User`**, not **`YourUser`**. Controllers that **cast** fail. Use **`@WithUserDetails`** (user **must exist**) or **`@WithSecurityContext`**.

> [!warning] Test thread only
> **`RANDOM_PORT`** HTTP runs on **another** thread. `@WithMockUser` **does not** ride along — send Basic / a bearer token (or stay on MockMvc).

> [!warning] CSRF is separate
> A mocked user on **POST** still needs **`.with(csrf())`** when CSRF is enabled (**403**, not 401).

> [!tip] Interview answer
> **`@WithMockUser` fakes `SecurityContext` so tests do not hit `/login` or the IdP.** `roles` get a `ROLE_` prefix; `authorities` do not. It does not run your `AuthenticationProvider`. For a custom `UserDetails` type, `@WithUserDetails`.
