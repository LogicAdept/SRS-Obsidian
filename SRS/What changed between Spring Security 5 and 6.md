<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS

# What changed between Spring Security 5 and 6?

> [!abstract] Short answer
> **Boot 3 / Jakarta** (`javax.*` → `jakarta.*`). Config is **composition**: a **`SecurityFilterChain` `@Bean`**, not **`WebSecurityConfigurerAdapter`** (deprecated **5.7**, **removed in 6**). HTTP and method authorization use **`AuthorizationManager`** (`authorizeHttpRequests`, `@EnableMethodSecurity`), not voters / **`AccessDecisionManager`**. The session is **read** by **`SecurityContextHolderFilter`**; you **save explicitly**. CSRF tokens are **deferred** and **XOR**’d. Official path: latest **5.8**, then **6.0**.

## 5.8 first, then 6.0

The team shipped **5.8 as a bridge**. Apply its prepare-for-6 opt-ins, then jump to Security **6** with Boot **3**. Remaining cleanup is the “Migrating to 6.0” chapter.

| Area | Spring Security 5 (typical) | Spring Security 6 |
| --- | --- | --- |
| Packages | `javax.servlet` | **`jakarta.servlet`** (Boot 3) |
| HTTP config | Extend **`WebSecurityConfigurerAdapter`** | **`@Bean SecurityFilterChain`** + `http.build()` |
| HTTP authorization | `authorizeRequests` + **`FilterSecurityInterceptor`** / voters | **`authorizeHttpRequests`** + **`AuthorizationFilter`** / **`AuthorizationManager`** |
| Matchers | `antMatchers` / `mvcMatchers` | **`requestMatchers`** |
| Method security | `@EnableGlobalMethodSecurity` (pre/post **off** by default) | **`@EnableMethodSecurity`** (pre/post **on**) |
| Context persistence | **`SecurityContextPersistenceFilter`** auto-saves, often into **`HttpSession`** | **`SecurityContextHolderFilter`** **reads** only; **`requireExplicitSave` is the default** |
| CSRF | Load token every request | **Deferred** load; **`XorCsrfTokenRequestAttributeHandler`** (BREACH) |
| `oauth2Login()` authority | `ROLE_USER` | **`OAUTH2_USER`** / **`OIDC_USER`** |

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {

	@Bean
	SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
		http.authorizeHttpRequests((authorize) -> authorize
				.requestMatchers("/public/**").permitAll()
				.anyRequest().authenticated());
		return http.build();
	}
}
```

**Listing 1.** The 6 shape: bean + lambda DSL + `requestMatchers`. No adapter, no `authorizeRequests` ([[Why was WebSecurityConfigurerAdapter removed]], [[How do you configure a SecurityFilterChain bean in Spring Security 6]], [[How do you configure authorizeHttpRequests in Spring Security 6]], [[What is the difference between EnableMethodSecurity and EnableGlobalMethodSecurity]]).

A custom filter that used to do only this:

```java
SecurityContextHolder.setContext(securityContext);
```

must also persist if the login should survive the next request:

```java
SecurityContextHolder.setContext(securityContext);
securityContextRepository.saveContext(securityContext, request, response);
```

**Listing 2.** 6 default: **`SecurityContextHolderFilter` does not write the session for you.** Built-in login filters already save. Hand-rolled auth that only touches the holder looks “logged in” for this request and anonymous on the next ([[How do you implement a custom AccessDecisionManager]], [[What is AuthorizationManager in method security]]).

```d2
direction: right
s5: "Security 5\nAdapter + voters\nauto-save session" {
  width: 210
  height: 64
  style.fill: "#fff3e0"
}
s6: "Security 6\nFilterChain bean +\nAuthorizationManager\nexplicit save" {
  width: 230
  height: 64
  style.fill: "#c8e6c9"
}
s5 -> s6: "5.8 prepare → Boot 3" {
  style.stroke: "#1565c0"
}
```

**Fig. 1.** Interview three: **composition**, **`AuthorizationManager`**, **explicit `SecurityContext` save**. Jakarta and `@EnableMethodSecurity` ride the same Boot 3 cut.

`@PreAuthorize("#id …")` needs **`-parameters`** (Framework 6.1 dropped `LocalVariableTableParameterNameDiscoverer`). `@EnableMethodSecurity` is not a rename: old **`prePostEnabled` defaulted to false**.

> [!warning] `authorizeRequests` / `antMatchers` mean you are still on 5
> Those methods are the 5.x DSL (`FilterSecurityInterceptor`). Security 6 uses **`authorizeHttpRequests` + `requestMatchers`**. If a snippet still compiles with `antMatchers`, you have not left 5.x. Pasting them into 6 is a compile error, not a silent fallback.

> [!warning] `setContext` without `saveContext` drops the login
> Auto-save on response commit was the 5 surprise (stateless APIs getting sessions). 6 writes the repository only when authentication code does. Logout must save the cleared context too. Do not set `requireExplicitSave(false)` to “make it like 5” on a JWT API.

> [!tip] Interview answer
> 6 is Boot 3 / Jakarta. Drop WebSecurityConfigurerAdapter for a SecurityFilterChain bean. Replace authorizeRequests and AccessDecisionManager with authorizeHttpRequests and AuthorizationManager. SecurityContextHolderFilter reads the context; you save it. Switch to @EnableMethodSecurity. Use 5.8 as the stepping stone.
