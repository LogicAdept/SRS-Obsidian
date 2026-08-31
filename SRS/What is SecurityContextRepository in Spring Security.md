<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/SecurityContext #SRS

# What is SecurityContextRepository in Spring Security?

> [!abstract] Short answer
> **`SecurityContextRepository`** is the strategy that **persists `SecurityContext` between HTTP requests**. The holder is **per-thread for one request** ([[What is SecurityContextHolder]]); the repository is how the **next** request gets the same user. Default (Spring Security **6+**) is **`DelegatingSecurityContextRepository`**: **`RequestAttributeSecurityContextRepository`** plus **`HttpSessionSecurityContextRepository`**. **`NullSecurityContextRepository`** persists **nothing** (JWT / **`SessionCreationPolicy.STATELESS`**). A custom implementation is how you store the context **somewhere other than the servlet session**.

## Load at the start of the request, save if it should survive

Interface (`org.springframework.security.web.context`): **`containsContext(request)`**, **`saveContext(context, request, response)`**, and **`loadDeferredContext(request)`** (replaces deprecated **`loadContext`**). Implementations must **never return null** from load — unauthenticated means an **empty** context.

**`SecurityContextHolderFilter`** (default in **6+**) **loads** the repository into **`SecurityContextHolder`** and does **not** save. Built-in authentication still saves when needed; code that only **`setContext(...)`** must also **`saveContext(...)`** if the user should survive this request (`requireExplicitSave`). Older **`SecurityContextPersistenceFilter`** loaded **and** saved whenever the context changed. Difference: [[What is the difference between SecurityContextHolderFilter and SecurityContextPersistenceFilter]].

## Built-in repositories

| Type | What it associates the context with |
|------|-------------------------------------|
| **`HttpSessionSecurityContextRepository`** | **`HttpSession`**, default key **`SPRING_SECURITY_CONTEXT`**. No session on load if none exists; **save** creates a session only if the context is **not** empty. |
| **`RequestAttributeSecurityContextRepository`** | A **request attribute**, so an **error dispatch** on the **same** request still sees `Authentication`. |
| **`NullSecurityContextRepository`** | **No-op** — does not write the session (OAuth/JWT-style; **`STATELESS`** wires this). |
| **`DelegatingSecurityContextRepository`** | **Saves to all** delegates; **loads from the first** that has it. |

Replace the session repo when you want Redis, a header, or **no** cross-request persistence.

```java
http.securityContext(sc -> sc.securityContextRepository(
		new DelegatingSecurityContextRepository(
				new RequestAttributeSecurityContextRepository(),
				new HttpSessionSecurityContextRepository())));
```

**Listing 1.** Default **6+** arrangement — request attribute **and** session. Use **`NullSecurityContextRepository`** (or **`sessionCreationPolicy(STATELESS)`**) when each request rebuilds `Authentication` from a token.

```d2
direction: right
req1: "Request 1\nauthenticate" {
  width: 160
  height: 60
  style.fill: "#e3f2fd"
}
save: "saveContext\n(session / attribute / no-op)" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
req2: "Request 2\nHolderFilter loads repo" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
holder: "SecurityContextHolder\nthis thread only" {
  width: 200
  height: 70
  style.fill: "#fce4ec"
}

req1 -> save -> req2 -> holder
```

**Fig. 1.** Repository bridges **requests**; the holder does not.

> [!warning] STATELESS vs a session repository
> Leaving **`HttpSessionSecurityContextRepository`** in place still creates a **`JSESSIONID`** when a non-empty context is saved — even on a JSON API. **`STATELESS`** / **`NullSecurityContextRepository`** means Spring Security **will not** obtain `SecurityContext` from the session; the token filter must populate the holder **every** request. Custom **`setContext`** without **`saveContext`** is lost at the end of the request under **`SecurityContextHolderFilter`**.

> [!tip] Interview answer
> SecurityContextRepository persists SecurityContext across HTTP requests. Default is DelegatingSecurityContextRepository (request attribute + HttpSession). NullSecurityContextRepository / STATELESS stores nothing so JWT rebuilds Authentication each time. SecurityContextHolderFilter only loads; you must save explicitly if you set the holder yourself. A custom repository is how you keep the context somewhere other than the servlet session.
