<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is the difference between a principal and credentials in Spring Security?

> [!abstract] Short answer
> On **`Authentication`**, **`getPrincipal()`** is **who** (*the identity of the principal being authenticated*). **`getCredentials()`** is **proof** (*the credentials that prove the principal is correct* — usually a password, otherwise whatever the **`AuthenticationManager`** needs). A login **request** typically has a username **`String`** plus a password. After **`DaoAuthenticationProvider`**, the principal is usually **`UserDetails`**. **`ProviderManager`** then **`eraseCredentials()`** by default, so **`getCredentials()`** on the stored token is **`null`**. The servlet **`Principal`** is the **`Authentication` itself**, not `getPrincipal()`.

## Who versus proof on the same token

Both getters are **`Object`**. Javadoc for **`getPrincipal()`**: callers populate identity on the **request**; the manager **often returns a richer principal** (many providers put **`UserDetails`** there). Javadoc for **`getCredentials()`**: populate proof on the request. **`getDetails()`** is request metadata (IP, session id), **not** the secured resource and **not** the user ([[What is a principal in Spring Security]], [[What is UsernamePasswordAuthenticationToken]], [[What is UserDetails and UserDetailsService in Spring Security]]).

| | Principal | Credentials |
| --- | --- | --- |
| Getter | **`getPrincipal()`** | **`getCredentials()`** |
| Role | Identity (**who**) | Proof (**how**) |
| Form-login **request** | Username **`String`** | Password |
| After **DAO** (default) | **`UserDetails`** | Password, then often **`null`** |
| JWT resource server | Typically **`Jwt`** | Bearer string (then often erased) |
| Anonymous | **`"anonymousUser"`** | Empty string |

**`UsernamePasswordAuthenticationToken.unauthenticated(username, password)`** (**since 5.7**): principal = name, credentials = password, **`isAuthenticated() == false`**. Success returns a **new** **`authenticated(...)`** token. **`forcePrincipalAsString`** on **DAO** (default **false**) keeps a **`String`** principal instead of **`UserDetails`** ([[What is an authenticated versus unauthenticated UsernamePasswordAuthenticationToken]], [[What is DaoAuthenticationProvider]]).

**`ProviderManager`** **`eraseCredentialsAfterAuthentication`** defaults **`true`**. **`AbstractAuthenticationToken.eraseCredentials()`** walks **credentials, principal, and details** and calls **`eraseCredentials()`** on any **`CredentialsContainer`** (**since 3.0.3**). **`User`** implements that interface, so the **hash on the principal** can be wiped too. Framework javadoc: write a provider that **returns an `Authentication` already without secrets**; do not treat **`CredentialsContainer`** as an application API ([[What is ProviderManager in Spring Security]]).

**`Authentication` implements `java.security.Principal`.** **`request.getUserPrincipal()`** is the **token**. **`getName()`** is the display username. Custom fields belong on the principal (**`Authentication.toBuilder()`**, **since 7.0**).

```java
Authentication request = UsernamePasswordAuthenticationToken
	.unauthenticated("user", "password");
Object who = request.getPrincipal();       // "user"
Object proof = request.getCredentials();   // "password"

Authentication result = authenticationManager.authenticate(request);
Object loaded = result.getPrincipal();     // typically UserDetails
Object leftover = result.getCredentials(); // typically null after erase
```

**Listing 1.** Same **`Authentication` type**, two getters. After **`ProviderManager`**, **proof is gone**; **who remains**.

```java
http
	.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
	.formLogin(Customizer.withDefaults());
```

**Listing 2.** Form login: filter puts **username / password** on an **unauthenticated** token; **DAO** replaces **who** with **`UserDetails`**.

```d2
direction: down
req: "unauthenticated token" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
who: "getPrincipal()\nusername String" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
proof: "getCredentials()\npassword" {
  width: 240
  height: 70
  style.fill: "#ffe0b2"
}
ok: "authenticated token" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
user: "getPrincipal()\nUserDetails" {
  width: 240
  height: 70
  style.fill: "#c8e6c9"
}
gone: "getCredentials()\nnull after erase" {
  width: 240
  height: 70
  style.fill: "#ffcdd2"
}

req -> who
req -> proof
ok -> user
ok -> gone
```

**Fig. 1.** Login **changes who** (String → **`UserDetails`**) and **drops proof** (**`eraseCredentials`**).

> [!warning] Erase hits the principal too
> **`getCredentials() == null`** after login is expected. If the principal is a shared **`User`**, **`User.eraseCredentials()`** also clears **`User.getPassword()`**. Cache a **copy**, set **`eraseCredentialsAfterAuthentication` false**, or return a fresh **`UserDetails`** each load.

> [!warning] Anonymous still has a principal
> **`AnonymousAuthenticationFilter`** installs **`"anonymousUser"`**. **`isAuthenticated()`** is **true** on that token — that is **not** a logged-in user. Casting **`getPrincipal()`** to **`UserDetails`** fails. The protected **resource** is the URL or method being authorized, **not** a third getter on **`Authentication`**.

> [!tip] Interview answer
> Principal is getPrincipal() — who is acting. Credentials are getCredentials() — the password or token that proves it. On the login request those are a username string and a password; after DaoAuthenticationProvider the principal is usually UserDetails and ProviderManager clears credentials. I do not confuse Authentication itself with getPrincipal(), and I do not read a password off the SecurityContext after a successful form login.
