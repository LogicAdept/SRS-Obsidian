<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is the difference between Authentication and AuthenticationManager?

> [!abstract] Short answer
> **`Authentication`** is the **token**: principal, credentials, authorities, and **`isAuthenticated()`**. The same type is the **request** (usually **unauthenticated**) and the **result** (fully populated, **`isAuthenticated() == true`**). **`AuthenticationManager`** is the **process**: **`authenticate(Authentication)`** returns that populated token or throws **`AuthenticationException`**. Stock implementation is **`ProviderManager`**, which delegates to **`AuthenticationProvider`**. You put **`Authentication`** on **`SecurityContext`**, never the manager.

## Token versus the component that validates it

**`Authentication`** (also **`java.security.Principal`**) is **who + proof + grants**. Filters build an **unauthenticated** **`UsernamePasswordAuthenticationToken`** and pass it in. A successful manager returns a **new** trusted token — typically **`UserDetails`** as principal plus authorities — not the request object flipped in place ([[What is a principal in Spring Security]], [[What is the difference between a principal and credentials in Spring Security]], [[What is UsernamePasswordAuthenticationToken]]).

**`AuthenticationManager`** (**`@FunctionalInterface`**) javadoc: *Processes an Authentication request.* **`authenticate`** must return a **fully populated** **`Authentication`** (authorities included) or throw. Exception contract, in order when the manager can test the state: **`DisabledException`**, **`LockedException`**, then **always** credential checking (**`BadCredentialsException`**). That order exists so passwords are **not** tested against a disabled or locked account. **`ProviderManager`** is the usual implementation; it does **not** check the password itself — **`DaoAuthenticationProvider`** (and others) do ([[What is ProviderManager in Spring Security]], [[What is AuthenticationManager and AuthenticationProvider in Spring Security]], [[What is DaoAuthenticationProvider]]).

| | **`Authentication`** | **`AuthenticationManager`** |
| --- | --- | --- |
| Kind | Value object / token | Strategy (**one method**) |
| Lifetime | Per request / session in **`SecurityContext`** | Application bean / filter field |
| Input | Built by a filter or your code | Receives that token |
| Output | **`isAuthenticated()`**, getters | **`authenticate` → Authentication** or throw |
| Stored in context? | **Yes** | **No** |

Form login: **`UsernamePasswordAuthenticationFilter`** holds an **`AuthenticationManager`** and calls it on **`POST /login`**. **`AnonymousAuthenticationFilter`** can install an **`Authentication`** **without** going through the manager. A missing manager bean fails **login wiring**; a **null** **`getAuthentication()`** is an **empty `SecurityContext`** (or you looked before the anonymous filter). Those are different bugs ([[How does form login work internally in Spring Security]], [[What is an authenticated versus unauthenticated UsernamePasswordAuthenticationToken]]).

```java
Authentication request = UsernamePasswordAuthenticationToken
	.unauthenticated("user", "password");
Authentication result = authenticationManager.authenticate(request);
SecurityContextHolder.getContext().setAuthentication(result);
```

**Listing 1.** Request token in; trusted token out; **only the result** goes on the context. **`request != result`**.

```java
http
	.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
	.formLogin(Customizer.withDefaults());
```

**Listing 2.** The filter chain **owns** an **`AuthenticationManager`**. Controllers read **`Authentication`**, not the manager.

```d2
direction: down
req: "Authentication\n(unauthenticated request)" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
mgr: "AuthenticationManager.authenticate\n(ProviderManager)" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
ok: "Authentication\n(authenticated result)" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
ctx: "SecurityContext" {
  width: 220
  height: 50
  style.fill: "#f3e5f5"
}

req -> mgr -> ok -> ctx
```

**Fig. 1.** The manager is the **arrow**. The token is what sits in **`SecurityContext`**.

> [!warning] Do not put the manager in the context
> **`SecurityContextHolder.getContext().setAuthentication(manager)`** is a type error and a design error. Downstream code reads **`getAuthentication()`**. After **`ProviderManager`**, **`eraseCredentials()`** (default **on**) often leaves **`getCredentials() == null`** even though the manager javadoc says the return includes credentials.

> [!warning] Null context is not a missing manager
> **`getAuthentication() == null`** means no token in this thread’s context. **`AnonymousAuthenticationToken`** is **not** null and **`isAuthenticated()` is true**. **`ProviderNotFoundException`** means a manager **ran** but no provider supported the token type. A missing **`AuthenticationManager`** fails when a filter **calls** **`authenticate`**, not when you read the context.

> [!tip] Interview answer
> Authentication is the object on SecurityContext: principal, credentials, authorities, before and after login. AuthenticationManager is authenticate() — usually ProviderManager calling AuthenticationProviders — and it returns a new populated Authentication or throws. I never store the manager in the context, and I do not treat a null getAuthentication() as the same problem as a missing manager bean.
