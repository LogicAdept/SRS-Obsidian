<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is ProviderManager in Spring Security?

> [!abstract] Short answer
> **`ProviderManager`** is the stock **`AuthenticationManager`**. It does **not** check passwords itself. It walks a **`List<AuthenticationProvider>`** in order: **`supports(Class)`** is the type gate; **`authenticate`** returns a **trusted `Authentication`**, **`null`** (try the next), or throws. A **later success discards an earlier `AuthenticationException`**. **`AccountStatusException`** and **`InternalAuthenticationServiceException`** **stop** the list (**SEC-546**). If nothing authenticates, an optional **parent `AuthenticationManager`** runs; if still nothing, **`ProviderNotFoundException`**. After success it **`eraseCredentials()`** by default.

## Iterate providers, then maybe a parent

Class javadoc: providers are tried until one returns **non-null**. That provider **decided**; later ones are skipped. Parent exists mainly for **namespace** fallback and is **not** something you usually need ([[What is AuthenticationManager and AuthenticationProvider in Spring Security]], [[How do you configure multiple AuthenticationProviders in Spring Security]]).

| Provider outcome | Manager |
| --- | --- |
| **`supports` false** | Skip |
| **`authenticate` → `Authentication`** | Copy **`details`** if missing; **done** |
| **`null`** | Next provider |
| **`AccountStatusException` / `InternalAuthenticationServiceException`** | **Rethrow now** |
| Other **`AuthenticationException`** (e.g. **`BadCredentialsException`**) | Remember it; **keep going** |
| List exhausted, **`result == null`** | **`parent.authenticate`** if set |
| Still nothing | **`ProviderNotFoundException`** — no provider **supported** the token type (or all returned **`null`**) |

Events go to **`AuthenticationEventPublisher`** (default **no-op** if you construct the bean yourself; **`DefaultAuthenticationEventPublisher`** under **`<http>` / Boot**). Parent success/failure events are **not** republished, to avoid duplicates.

**`eraseCredentialsAfterAuthentication`** defaults **`true`**: a result that implements **`CredentialsContainer`** is wiped before return. Caching **`UserDetails`** that share that instance needs **`false`** or a **copy** ([[What is an authenticated versus unauthenticated UsernamePasswordAuthenticationToken]], [[What is DaoAuthenticationProvider]]). **`hideUserNotFoundExceptions`** is on **DAO**, not here ([[What is UsernameNotFoundException]]).

Construct **`new ProviderManager(first, second)`** or **`HttpSecurity.authenticationProvider(...)`**. A **single** **`AuthenticationProvider` `@Bean`** can be auto-wired; **two are ignored** ([[How do you configure a custom AuthenticationProvider in Spring Security]]).

```java
AuthenticationManager manager = new ProviderManager(List.of(daoProvider, ldapProvider));
Authentication result = manager.authenticate(
	UsernamePasswordAuthenticationToken.unauthenticated(username, password));
```

**Listing 1.** Explicit manager. **`DaoAuthenticationProvider` then LDAP**: a **`BadCredentialsException`** from DAO does **not** by itself skip LDAP; a **locked** account **does**.

```java
manager.setEraseCredentialsAfterAuthentication(true); // default
```

**Listing 2.** After success, **`result.getCredentials()`** is typically **null**.

```d2
direction: down
req: "Authentication request" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
loop: "AuthenticationProvider list\nsupports → authenticate" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
parent: "optional parent AuthenticationManager" {
  width: 280
  height: 50
  style.fill: "#fce4ec"
}
ok: "eraseCredentials + return" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}

req -> loop
loop -> parent
loop -> ok
parent -> ok
```

**Fig. 1.** First **non-null** result wins. Parent is only if the list produced **nothing**.

> [!warning] `ProviderNotFoundException` is a type miss
> Usually **`supports` never returned true** (custom token, JWT provider not on this manager). It is **not** “wrong password.” Wrong password is **`BadCredentialsException`** from a provider that **did** run. **`UsernameNotFoundException` hidden as `BadCredentialsException`** still **continues** the list unless you throw **`InternalAuthenticationServiceException`**.

> [!warning] Status exceptions are fatal
> **Locked / disabled / expired** must not fall through to another user store. **`InternalAuthenticationServiceException`** (DAO **`null` user**) is the same. Do not catch those in a provider and return **`null`** to “try LDAP.”

> [!tip] Interview answer
> ProviderManager is the default AuthenticationManager: a list of AuthenticationProviders, first non-null success wins. Returning null means try the next; throwing BadCredentialsException also tries the next, but AccountStatusException stops immediately. If nobody handles the token type, you get ProviderNotFoundException. After success it erases credentials unless I turn that off.
