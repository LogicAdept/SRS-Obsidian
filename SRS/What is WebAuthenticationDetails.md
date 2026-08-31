<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is WebAuthenticationDetails?

> [!abstract] Short answer
> **`WebAuthenticationDetails`** is the usual **`Authentication.getDetails()`** value for servlet logins: a **serializable snapshot** of the **remote IP** and, if a session **already exists**, the **`HttpSession` id**. **`WebAuthenticationDetailsSource`** builds it from the **`HttpServletRequest`**. Form/Basic filters attach it to the **request** token; **`ProviderManager`** copies **`details`** onto the **success** token if missing. It is **request metadata**, not identity and **not** **`GrantedAuthority`**. **`hasRole` does not read it.**

## IP and session id on `getDetails()`, not on the principal

**`Authentication.getDetails()`** javadoc: extra data about the **request** (IP, certificate serial, …). The web implementation records **`getRemoteAddress()`** (TCP/IP address the authentication request came from) and **`getSessionId()`**. The request constructor **sets the session id only if a session already exists — it will not create one**. A first login often has **`sessionId == null`** on this object even after a session is created later. The two-arg constructor (**since 5.7**) exists for Jackson serialization ([[What is a principal in Spring Security]], [[What is the difference between a principal and credentials in Spring Security]]).

**`AbstractAuthenticationProcessingFilter`** (form **`POST /login`**) calls **`AuthenticationDetailsSource.buildDetails(request)`** before **`AuthenticationManager`**. Default source: **`WebAuthenticationDetailsSource`**. **`equals` / `hashCode`** use address + session id ([[How does form login work internally in Spring Security]], [[What is UsernamePasswordAuthenticationToken]], [[What is ProviderManager in Spring Security]]).

This is **not** session-fixation protection. Fixation strategies **change the `HttpSession` id** after success; this holder is a **snapshot at authenticate time** and can be **stale**. **`eraseCredentials()`** can clear **details** if they implement **`CredentialsContainer`** — this class does **not**.

Subclass **`PreAuthenticatedGrantedAuthoritiesWebAuthenticationDetails`** is pre-auth specific. Custom extra fields belong in **your** details type (or on the **principal**), not stuffed into **`GrantedAuthority`** ([[What is GrantedAuthority in Spring Security]]).

```java
Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
if (authentication.getDetails() instanceof WebAuthenticationDetails details) {
	String ip = details.getRemoteAddress();
	String sessionId = details.getSessionId(); // often null on first form login
}
```

**Listing 1.** Audit IP / session id. Do **not** authorize on these strings.

```java
http
	.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
	.formLogin(Customizer.withDefaults());
```

**Listing 2.** Stock form login already sets **`WebAuthenticationDetails`** via **`WebAuthenticationDetailsSource`**. Override **`authenticationDetailsSource`** only for a custom details type.

```d2
direction: down
req: "HttpServletRequest" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
src: "WebAuthenticationDetailsSource" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
det: "WebAuthenticationDetails\nremoteAddress + sessionId?" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
auth: "Authentication.getDetails()" {
  width: 240
  height: 50
  style.fill: "#f3e5f5"
}

req -> src -> det -> auth
```

**Fig. 1.** Details are **built from the request**, then **carried on the token**.

> [!warning] Details are not roles
> **`hasRole` / `hasAuthority`** read **`getAuthorities()`**. Putting **`ROLE_ADMIN`** in **`getDetails()`** does nothing. **`getPrincipal()`** is the user; **`getDetails()`** is **where the request came from**.

> [!warning] `getSessionId()` is not “the current session”
> The constructor **refuses to start a session**. After login, **`request.getSession().getId()`** can differ from **`details.getSessionId()`**. Reverse-proxy setups need **`request.getRemoteAddr()`** to be the real client (forwarded headers), or the stored IP is the proxy.

> [!tip] Interview answer
> WebAuthenticationDetails is what Spring Security usually puts in Authentication.getDetails() for a servlet login: remote IP and the session id if one already existed. The filter’s WebAuthenticationDetailsSource builds it; it is not GrantedAuthority and hasRole ignores it. I use it for audit logs, not authorization, and I do not assume sessionId is set on the first login.
