<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Framework/Testing #Java/Annotations #SRS

# What is WithAnonymousUser?

> [!abstract] Short answer
> **`@WithAnonymousUser`** (`org.springframework.security.test.context.support`, module **`spring-security-test`**, since **4.1**) plants an **`AnonymousAuthenticationToken`** in **`SecurityContextHolder`** for the test. Factory principal is **`"anonymous"`**, one authority **`ROLE_ANONYMOUS`**. Typical use: class-level **`@WithMockUser`**, then **override one method** to run anonymous. It is **not** an empty context — there **is** an `Authentication`.

## Override the class-level user

`WithAnonymousUserSecurityContextFactory` builds `new AnonymousAuthenticationToken("key", "anonymous", ROLE_ANONYMOUS)`. Same listener as `@WithMockUser`: **`WithSecurityContextTestExecutionListener`**. Default setup is **`beforeTestMethod`** (before JUnit `@Before`); **`setupBefore = TestExecutionEvent.TEST_EXECUTION`** is after `@Before`.

Docs treat this as the convenient way to keep most tests as a user and flip a few to anonymous. A method with **no** security annotation and **no** class-level user is different: **`SecurityContextHolder` empty** → method security’s **`AuthenticationCredentialsNotFoundException`**. Anonymous is **present**, and `AuthenticationTrustResolver` still classifies it as **anonymous** (`isAuthenticated()` expressions fail; `permitAll` / `ROLE_ANONYMOUS` can pass). Production web filter default principal is **`anonymousUser`** — the test factory uses **`anonymous`**. Fake user: [[What is the purpose of WithMockUser in Spring Security tests]]. Lookup: [[What is WithUserDetails in Spring Security tests]]. Method security: [[How do you test method security without replacing SecurityFilterChain]]. MockMvc: [[How do you test Spring Security in MockMvc tests]].

```java
@ExtendWith(SpringExtension.class)
@WithMockUser
class WithUserClassLevelAuthenticationTests {

    @Test
    void withMockUser1() { }

    @Test
    @WithAnonymousUser
    void anonymous() {
        // override default to run as anonymous user
    }
}
```

**Listing 1.** Conceptual Security **7.1**. Method `anonymous` is **not** `ROLE_USER`.

```java
Authentication auth = SecurityContextHolder.getContext().getAuthentication();
assertThat(auth).isInstanceOf(AnonymousAuthenticationToken.class);
assertThat(auth.getAuthorities()).extracting(GrantedAuthority::getAuthority)
        .containsExactly("ROLE_ANONYMOUS");
```

**Listing 2.** Conceptual: token type and authority from **`WithAnonymousUserSecurityContextFactory`**.

```d2
direction: down
cls: "@WithMockUser on class" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
m: "@WithAnonymousUser on method" {
  width: 280
  height: 40
  style.fill: "#fff3e0"
}
tok: "AnonymousAuthenticationToken\nROLE_ANONYMOUS" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}

cls -> m -> tok
```

**Fig. 1.** Method annotation wins for that test. Other methods keep the mock user.

> [!warning] Anonymous is still an `Authentication`
> `getAuthentication() != null` is **true**. That is the point of anonymous auth in production too: the holder is **never left null** by the filter. Check **token type**, **`isAnonymous`**, or an expression such as **`isAuthenticated()`**, not mere presence.

> [!warning] Not the same as “no user”
> `@PreAuthorize("isAuthenticated()")` **rejects** anonymous. A test with **no** `@With*` often throws **`AuthenticationCredentialsNotFoundException`** instead of **`AccessDeniedException`**. Pick the annotation that matches the production path you care about.

> [!warning] Test thread only
> **`RANDOM_PORT`** HTTP is another thread. `@WithAnonymousUser` **does not** ride along.

> [!tip] Interview answer
> **`@WithAnonymousUser` puts an `AnonymousAuthenticationToken` (`ROLE_ANONYMOUS`) in the test `SecurityContext`.** Use it to override class-level `@WithMockUser`. It is not “logged out / null Authentication.”
