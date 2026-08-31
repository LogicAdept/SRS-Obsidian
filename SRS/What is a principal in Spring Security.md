<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is a principal in Spring Security?

> [!abstract] Short answer
> The **principal** is **who** is acting. On **`Authentication`**, that identity is **`getPrincipal()`** (`Object`): a **username `String`** on the login request, usually **`UserDetails`** after **`DaoAuthenticationProvider`**, a **`Jwt`** for resource-server JWT, or the string **`anonymousUser`** when **`AnonymousAuthenticationFilter`** filled an empty context. **`getCredentials()`** is the **proof** (password, token). **`Authentication` itself implements `java.security.Principal`**, so **`HttpServletRequest.getUserPrincipal()`** is the **token**, not `getPrincipal()`. Read the user with **`@AuthenticationPrincipal`** or **`authentication.getPrincipal()`** — and **cast only after you know the type**.

## Who vs proof vs the token

Javadoc: *The identity of the principal being authenticated.* For username/password **requests**, that is **the username**. After **`AuthenticationManager.authenticate`**, providers **often** put **`UserDetails`** there for the application ([[What is UserDetails and UserDetailsService in Spring Security]], [[What is UsernamePasswordAuthenticationToken]], [[What is AuthenticationManager and AuthenticationProvider in Spring Security]]).

**`Authentication` extends `Principal`.** `getName()` is the servlet/JAAS name (typically **`UserDetails.getUsername()`**). **`getPrincipal()`** is Spring’s richer identity object. **`getAuthorities()`** are granted **to** that principal. **`getDetails()`** is request metadata (IP, session id via **`WebAuthenticationDetails`**), not the user.

Unauthenticated **`UsernamePasswordAuthenticationToken.unauthenticated(username, password)`**: principal = username **`String`**, credentials = password. Successful **`DaoAuthenticationProvider`** (default **`forcePrincipalAsString` false**): principal = **`UserDetails`**. **`eraseCredentials()`** can clear the password on **credentials, principal, and details** if they implement **`CredentialsContainer`**. Custom fields belong on the principal (**`Authentication.toBuilder()`** javadoc, **since 7.0**).

**Anonymous:** **`AnonymousAuthenticationFilter(String key)`** installs principal **`"anonymousUser"`** and **`ROLE_ANONYMOUS`**. That **`Authentication` is still present** — `getPrincipal() instanceof UserDetails` is **false**. JWT resource server: principal is typically the **`Jwt`**, not `User`.

MVC: **`@AuthenticationPrincipal`** resolves **`Authentication.getPrincipal()`** (optional SpEL, **`errorOnInvalidType`** default **false** → **null** on a bad cast). Architecture also exposes **`@CurrentSecurityContext`** and **`HttpServletRequest.getRemoteUser()`** ([[What is AuthenticationPrincipal]], [[What is SecurityContextHolder]], [[How does form login work internally in Spring Security]]).

```java
Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
Object principal = authentication.getPrincipal();
if (principal instanceof UserDetails user) {
	String username = user.getUsername();
}
```

**Listing 1.** Do not assume **`UserDetails`**. Anonymous is a **`String`**; JWT is not `User`.

```java
@GetMapping("/me")
Map<String, String> me(@AuthenticationPrincipal UserDetails user) {
	return Map.of("username", user.getUsername());
}
```

**Listing 2.** Injects **`getPrincipal()`**. Wrong type with default **`errorOnInvalidType`**: **`user` is null**, not a hard failure.

```d2
direction: down
auth: "Authentication\nalso java.security.Principal" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
who: "getPrincipal()\nUserDetails / String / Jwt" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
proof: "getCredentials()\npassword / token" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
name: "getName()\nusername string" {
  width: 220
  height: 50
  style.fill: "#f3e5f5"
}

auth -> who
auth -> proof
auth -> name
```

**Fig. 1.** **Who**, **proof**, and **display name** are three getters. The servlet **`Principal`** is the **`Authentication`**.

> [!warning] Anonymous is still a principal
> A missing login is **not** a null `Authentication` once **`AnonymousAuthenticationFilter`** runs. Casting **`getPrincipal()`** to **`UserDetails`** NPE/CCE on **`anonymousUser`**. **`request.getUserPrincipal()`** returns the **`Authentication`**, so **`getUserPrincipal().getName()`** is **`getName()`**, not a shortcut to **`UserDetails`**.

> [!warning] `@AuthenticationPrincipal UserDetails` on a JWT API
> Resource-server **`Jwt`** principals make that parameter **null**. Use **`@AuthenticationPrincipal Jwt jwt`** (or **`JwtAuthenticationToken`**) there. **`errorOnInvalidType = true`** turns the mismatch into **`ClassCastException`**.

> [!tip] Interview answer
> The principal is the identity on Authentication.getPrincipal(): a username string going into AuthenticationManager, usually UserDetails coming out of DaoAuthenticationProvider. Credentials prove that identity. Authentication itself is a java.security.Principal, which is why getUserPrincipal() is the token. I never cast to UserDetails without handling anonymousUser and JWT.
