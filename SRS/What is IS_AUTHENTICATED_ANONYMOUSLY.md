<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is IS_AUTHENTICATED_ANONYMOUSLY?

> [!abstract] Short answer
> **`IS_AUTHENTICATED_ANONYMOUSLY`** is a **legacy `ConfigAttribute`** processed by **`AuthenticatedVoter`** (deprecated). It is the **least strict** of three levels: **`IS_AUTHENTICATED_FULLY`**, **`IS_AUTHENTICATED_REMEMBERED`**, **`IS_AUTHENTICATED_ANONYMOUSLY`**. Javadoc: access is granted if the caller is **anonymous, remember-me, or fully authenticated** — not “anonymous only.” XML dumps put it on login/index **`intercept-url`**s. Current **`authorizeHttpRequests`** uses **`permitAll()`** for public pages, **`anonymous()`** only when the user **must** be anonymous, and **`authenticated()` / `fullyAuthenticated()` / `rememberMe()`** for the stricter levels.

## Three trust levels, not a role name

Authorization architecture: this string is **not** a **`ROLE_`** prefix for **`RoleVoter`**. **`AuthenticatedVoter`** inspects **`AuthenticationTrustResolver`**: **FULLY** = not anonymous and not remember-me; **REMEMBERED** = remember-me **or** fully authenticated; **ANONYMOUSLY** = remember-me **or** anonymous **or** full ([[How do you configure remember-me in Spring Security]], [[What is hasRole versus hasAuthority in Spring Security]]).

Anonymous support still installs an **`AnonymousAuthenticationToken`** (`anonymousUser`, **`ROLE_ANONYMOUS`**) when the context is empty ([[What is AnonymousAuthenticationFilter]], [[What is AnonymousAuthenticationToken]], [[What is the difference between ROLE_USER and ROLE_ANONYMOUS]], [[What is a principal in Spring Security]]). Servlet **`getUserPrincipal()`** stays **null**. **`ExceptionTranslationFilter`** treats anonymous **`AccessDeniedException`** as **commence login** (**401** path), not **403** ([[What is AuthenticationEntryPoint]], [[What is AccessDeniedHandler]]).

Official anonymous chapter: **`ROLE_ANONYMOUS`** on an interceptor is often **replaced with** **`IS_AUTHENTICATED_ANONYMOUSLY`**. **`RoleVoter` + `ROLE_ANONYMOUS`** matches that **authority only** (logged-in users typically **lack** it). **`AuthenticatedVoter`** is the API that can tell anonymous / remember-me / full apart. **`AuthenticatedVoter` is deprecated** in **7.1**; **`AuthenticatedAuthorizationManager`** (**since 5.5**, factories **`anonymous` / `authenticated` / `fullyAuthenticated` / `rememberMe` since 5.8**) is the replacement — and **`anonymous()` means is-anonymous only**, which is **stricter** than **`IS_AUTHENTICATED_ANONYMOUSLY`**.

```xml
<intercept-url pattern="/login.jsp" access="IS_AUTHENTICATED_ANONYMOUSLY"/>
<intercept-url pattern="/**" access="ROLE_USER"/>
```

**Listing 1.** Legacy non-expression XML. With **expression** `access=`, write **`permitAll`** or **`isAnonymous()`**, not this constant.

```java
http.authorizeHttpRequests((authorize) -> authorize
	.requestMatchers("/login", "/css/**").permitAll()
	.requestMatchers("/account/**").fullyAuthenticated()
	.anyRequest().authenticated());
```

**Listing 2.** Current DSL. **`permitAll()`** is the usual public-page stand-in (session is **not** consulted). **`anonymous()`** **denies** a logged-in user. **`authenticated()`** **denies** anonymous.

```d2
direction: down
full: "IS_AUTHENTICATED_FULLY\ninteractive login only" {
  width: 280
  height: 70
  style.fill: "#fce4ec"
}
rem: "IS_AUTHENTICATED_REMEMBERED\nremember-me OR full" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
anon: "IS_AUTHENTICATED_ANONYMOUSLY\nanon OR remember-me OR full" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}

full -> rem -> anon
```

**Fig. 1.** Each step **adds** callers. **ANONYMOUSLY** is the **widest** of the three, not the narrowest.

> [!warning] Not “anonymous only”
> **`IS_AUTHENTICATED_ANONYMOUSLY` allows a fully authenticated user.** **`anonymous()`** and **`hasRole("ANONYMOUS")` / `ROLE_ANONYMOUS`** do **not** — they **403** someone already logged in (login page trap). **`anyRequest().authenticated()`** **excludes** anonymous even though the token’s **`isAuthenticated()`** is **true**; use **`AuthenticationTrustResolver.isAnonymous`**, not “is there an `Authentication`?”

> [!warning] Deprecated voter, expression XML
> **`AuthenticatedVoter` / `AccessDecisionVoter`** are **deprecated**. Do not paste **`IS_AUTHENTICATED_ANONYMOUSLY`** into **`use-expressions="true"`** `access` SpEL. Prefer **`permitAll`**, **`isAnonymous()`**, **`isAuthenticated()`**, **`isFullyAuthenticated()`**, **`isRememberMe()`**.

> [!tip] Interview answer
> IS_AUTHENTICATED_ANONYMOUSLY is an old ConfigAttribute for AuthenticatedVoter meaning “at least anonymous”: anonymous, remember-me, or fully logged in. It is not ROLE_ANONYMOUS and it is not anonymous()-only. I map public pages to permitAll today, use fullyAuthenticated when remember-me is not enough, and I never treat an AnonymousAuthenticationToken as a missing Authentication.
