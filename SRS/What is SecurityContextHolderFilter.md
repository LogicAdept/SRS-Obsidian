<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/Authentication #SRS

# What is `SecurityContextHolderFilter`?

> [!abstract] Short answer
> A **`GenericFilterBean`** (since **5.7**) that **loads** `SecurityContext` from a **`SecurityContextRepository`** into **`SecurityContextHolder`** at the start of the request. Spring Security **6 default** (replaces deprecated **`SecurityContextPersistenceFilter`**). It does **not** auto-save: authentication filters must **`saveContext` explicitly** (`requireExplicitSave` **true**). Architecture TRACE **`(3/15)`**. Dump “~100” is **wrong** (`FilterOrderRegistration` **700**). Dump “saves at the end” describes the **old** persistence filter.

## Load only; save is someone else’s job

```d2
direction: down
repo: "SecurityContextRepository\n(session / request attr)" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
schf: "SecurityContextHolderFilter\nset on SecurityContextHolder" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
auth: "form / Basic / Bearer\nexplicit saveContext" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}

repo -> schf: "read"
schf -> auth
auth -> repo: "write if login succeeded"
```

**Fig. 1.** Session-management chapter: never install **both** HolderFilter and PersistenceFilter. Built-in [[What is UsernamePasswordAuthenticationFilter]] / Bearer already save. A **custom** JWT filter that only `SecurityContextHolder.setContext` **will not** survive the next request. See [[How do you implement a custom security filter in Spring Security]] and [[What is FilterChainProxy and DelegatingFilterProxy]] (clears the holder to avoid leaks).

Exploit-protection filters go **after** this (architecture rule of thumb). A filter **before** it cannot see the **restored session** `Authentication`. Not [[What is SecurityContextHolderAwareRequestFilter]] (servlet `isUserInRole` wrapper). See [[What is FilterOrderRegistration]].

```java
http.securityContext((securityContext) -> securityContext
        .securityContextRepository(repository)); // default: session repo + HolderFilter
```

**Listing 1.** `HttpSecurity.securityContext`. XML `security-context-explicit-save` selects HolderFilter. Custom persist: `repository.saveContext(context, request, response)` after `setContext`.

> [!warning] It does not write the session for you
> SS6 **does not** save on every response. `requireExplicitSave(false)` brings back PersistenceFilter (migration only). `STATELESS` APIs still **load** (often empty) then Bearer **saves** into a request-attribute repo if configured — not a remember-me cookie.

> [!tip] Interview answer
> SecurityContextHolderFilter is the Spring Security 6 filter that reads SecurityContext from the repository into the ThreadLocal at the start of the request. It replaced SecurityContextPersistenceFilter and does not auto-save. Form login and Bearer filters call saveContext themselves. Put custom authentication after it, or you will not see the session user.
