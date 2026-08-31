<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is the difference between Principal and UserDetails?

> [!abstract] Short answer
> **`java.security.Principal`** is the JDK identity contract: **`getName()`**. In a servlet, **`HttpServletRequest.getUserPrincipal()`** and a controller **`Principal`** parameter are that type — and Spring’s **`Authentication` implements `Principal`**, so you get the **token**, not **`getPrincipal()`**. **`UserDetails`** is Spring’s **user snapshot** for username/password: username, **password hash**, **`GrantedAuthority`**, and account flags. After **`DaoAuthenticationProvider`**, **`Authentication.getPrincipal()`** is **often** a **`UserDetails`**. **`UserDetails` does not implement `Principal`.** Cast **`getPrincipal()`** to **`UserDetails`** only when you know that is what the provider stored.

## JDK name versus Spring’s user object

**`Principal.getName()`** is a string. **`AbstractAuthenticationToken.getName()`** returns **`UserDetails.getUsername()`** when the inner principal is **`UserDetails`**, otherwise **`principal.toString()`**. **`getRemoteUser()`** is that same name ([[What is a principal in Spring Security]], [[What is UsernamePasswordAuthenticationToken]]).

**`UserDetails`** (loaded by **`UserDetailsService`**) is what **`DaoAuthenticationProvider`** authenticates against: **`getUsername`**, **`getPassword`**, **`getAuthorities`**, **`isEnabled` / `isAccountNonLocked` / `isAccountNonExpired` / `isCredentialsNonExpired`**. On success that object is stored as **`getPrincipal()`** unless **`forcePrincipalAsString`**. **`User`** is the stock implementation ([[What is UserDetails and UserDetailsService in Spring Security]], [[What account status flags does UserDetails expose]], [[What is DaoAuthenticationProvider]]).

| | `Principal` (servlet / JAAS) | `UserDetails` |
| --- | --- | --- |
| Package | **`java.security`** | **`org.springframework.security.core.userdetails`** |
| What you hold | Usually the **`Authentication`** | Often **`Authentication.getPrincipal()`** after DAO |
| API | **`getName()`** | Username, password, authorities, flags |
| Implements `Principal`? | **`Authentication` does** | **No** |
| MVC inject | Method arg **`Principal`** | **`@AuthenticationPrincipal UserDetails`** |

Unauthenticated login request: inner principal is a username **`String`**. Anonymous: **`"anonymousUser"`**. Resource-server JWT: typically **`Jwt`**. OAuth2 Login: **`OAuth2User` / `OidcUser`**. None of those are **`UserDetails`** ([[What is AuthenticationPrincipal]], [[What is the difference between a principal and credentials in Spring Security]]).

```java
@GetMapping("/who")
Map<String, String> who(Principal servletPrincipal,
		@AuthenticationPrincipal UserDetails user) {
	return Map.of(
			"servletName", servletPrincipal.getName(),
			"userDetails", user != null ? user.getUsername() : "none");
}
```

**Listing 1.** **`Principal`** is the **`Authentication`**. **`@AuthenticationPrincipal`** is **`getPrincipal()`**. On JWT, **`user` is null** (default **`errorOnInvalidType`**).

```java
Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
if (authentication.getPrincipal() instanceof UserDetails details) {
	String username = details.getUsername();
}
```

**Listing 2.** Pattern-match. Do not cast blindly.

```d2
direction: down
auth: "Authentication\nimplements Principal" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
name: "getName()\nusername string" {
  width: 240
  height: 50
  style.fill: "#f3e5f5"
}
inner: "getPrincipal()\nUserDetails / String / Jwt / OidcUser" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}

auth -> name
auth -> inner
```

**Fig. 1.** Servlet **`Principal`** is the **token**. **`UserDetails`** is **one possible** inner principal.

> [!warning] `UserDetails` is not a `Principal`
> Dumps that say “UserDetails is a Principal” mix **`getPrincipal()`’s runtime type** with the JDK interface. **`instanceof Principal`** on a **`User`** is **false**. **`request.getUserPrincipal()`** is **`Authentication`**; calling **`getName()`** is not a shortcut to **`UserDetails`**.

> [!warning] JWT / OAuth2 principals are not `User`
> **`@AuthenticationPrincipal UserDetails`** on a resource server is **null**. Use **`Jwt`**, **`OidcUser`**, or a custom type. Anonymous **`anonymousUser`** is a **`String`** — a raw cast **CCE**s. After **`eraseCredentials()`**, even a **`User`** principal may have a **cleared password**.

> [!tip] Interview answer
> Principal is java.security.Principal — getName() — and in Spring MVC that parameter is the Authentication token because Authentication implements Principal. UserDetails is Spring’s username/password user object: hash, authorities, account flags. DaoAuthenticationProvider often puts UserDetails in getPrincipal(), but UserDetails does not implement Principal, and JWT or OIDC login will not be UserDetails.
