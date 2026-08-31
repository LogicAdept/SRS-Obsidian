<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/Authentication #SRS

# How does Spring Security authenticate an HTTP request end to end?

> [!abstract] Short answer
> The request enters **`FilterChainProxy`**, which runs **one** `SecurityFilterChain`. **`SecurityContextHolderFilter`** loads any existing `Authentication`. If the user must log in, **`AuthorizationFilter`** denies, **`ExceptionTranslationFilter`** calls an **`AuthenticationEntryPoint`** (redirect to `/login` or `WWW-Authenticate`). A credential filter (**`UsernamePasswordAuthenticationFilter`**, or Bearer for JWT) builds an **unauthenticated** `Authentication`, **`ProviderManager`** picks an **`AuthenticationProvider`** (`DaoAuthenticationProvider` for passwords), then the filter **puts the result on `SecurityContextHolder`**. Later requests reuse that context; they do not re-run `ProviderManager` unless the mechanism is stateless (JWT/Basic).

## Form login (the dump pipeline)

```d2
direction: down
fcp: "FilterChainProxy\nfirst matching chain" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
ctx: "SecurityContextHolderFilter\nload SecurityContext" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
authz: "AuthorizationFilter\ndecline if anonymous" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
etf: "ExceptionTranslationFilter\nAuthenticationEntryPoint" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
upaf: "UsernamePasswordAuthenticationFilter\nUsernamePasswordAuthenticationToken" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
pm: "ProviderManager → DaoAuthenticationProvider\nUserDetailsService + PasswordEncoder" {
  width: 320
  height: 55
  style.fill: "#fce4ec"
}
save: "SecurityContextHolder + repository\nSuccessHandler" {
  width: 280
  height: 50
  style.fill: "#fce4ec"
}

fcp -> ctx
ctx -> authz
authz -> etf: "unauthenticated"
etf -> upaf: "POST credentials"
upaf -> pm
pm -> save
```

**Fig. 1.** Servlet authentication architecture: filters collect credentials; `AuthenticationManager` decides; the filter stores `Authentication`. See [[What is FilterChainProxy and DelegatingFilterProxy]] and [[What is ExceptionTranslationFilter in Spring Security]].

`DefaultLoginPageGeneratingFilter` **renders** the default `/login` page. The **redirect** to that page is `LoginUrlAuthenticationEntryPoint`, not the generating filter. `AuthorizationFilter` does not redirect; it throws, and `ExceptionTranslationFilter` translates.

```java
// Credential filter (UsernamePasswordAuthenticationFilter):
Authentication request = new UsernamePasswordAuthenticationToken(username, password); // not authenticated
Authentication result = authenticationManager.authenticate(request);
// ProviderManager → DaoAuthenticationProvider:
//   UserDetails user = userDetailsService.loadUserByUsername(username);
//   passwordEncoder matches user.getPassword() against the raw password
SecurityContext context = SecurityContextHolder.createEmptyContext();
context.setAuthentication(result);
SecurityContextHolder.setContext(context);
// Filter also SecurityContextRepository.saveContext for the next request
```

**Listing 1.** Conceptual form-login core (not a copy of framework source). `DaoAuthenticationProvider` **looks up** `UserDetails` and **validates** the password with `PasswordEncoder`. Success type is `UsernamePasswordAuthenticationToken` with `UserDetails` as principal. Create a **new** `SecurityContext` — do not `getContext().setAuthentication` (race across threads).

`ProviderManager` walks `AuthenticationProvider`s until one authenticates, fails, or all skip (`ProviderNotFoundException`). A JWT chain uses **`JwtAuthenticationProvider`** instead of `DaoAuthenticationProvider`. See [[How do you configure JWT and form login as two SecurityFilterChain beans]].

On **later** session requests, `SecurityContextHolderFilter` restores `Authentication`; `AuthorizationFilter` only checks `GrantedAuthority` (often `ROLE_*` from `UserDetailsService`). Bearer/JWT repeats authentication **each** request from the token, not from the session.

> [!warning] JWT does not use this form-login filter
> Resource-server JWT goes through **`BearerTokenAuthenticationFilter`** + **`JwtAuthenticationProvider`**. There is no `UsernamePasswordAuthenticationFilter` and usually no saved session (`STATELESS`). Mixing both is **two chains**, not one pipeline.

> [!tip] Interview answer
> End to end: FilterChainProxy runs the matching chain, AuthorizationFilter plus ExceptionTranslationFilter start login if needed, UsernamePasswordAuthenticationFilter builds a token and ProviderManager authenticates via DaoAuthenticationProvider (UserDetailsService and PasswordEncoder), then the Authentication is stored in SecurityContextHolder. JWT swaps in a bearer filter and JwtAuthenticationProvider instead of form login.
