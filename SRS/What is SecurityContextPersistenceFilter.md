<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/Authentication #SRS

# What is `SecurityContextPersistenceFilter`?

> [!abstract] Short answer
> The **legacy** (since **3.0**, **`@Deprecated`**) filter that **loads** `SecurityContext` from a **`SecurityContextRepository`** (default **`HttpSessionSecurityContextRepository`**) at the start of the request, **saves** it when the request finishes, and **clears** `SecurityContextHolder` so pooled threads do not leak users. Spring Security **6 default** is [[What is SecurityContextHolderFilter]] (**load only**, explicit `saveContext`). **Never both.** `FilterOrderRegistration`: this slot is **800**, immediately after HolderFilter.

## Load, run the chain, save, clear

```d2
direction: down
load: "repository → SecurityContextHolder" {
  width: 300
  height: 40
  style.fill: "#e3f2fd"
}
app: "authentication + rest of chain" {
  width: 280
  height: 40
  style.fill: "#fff3e0"
}
save: "saveContext if changed\nthen clear holder" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}

load -> app
app -> save
```

**Fig. 1.** Javadoc: **must run before** BASIC/form/CAS — they expect a valid `SecurityContext` already. Executes **once per request** (old container quirks). `forceEagerSessionCreation` default **`false`**. See [[What is FilterOrderRegistration]] and [[How do you implement a custom security filter in Spring Security]].

SS6: `requireExplicitSave` **true** → HolderFilter, **not** this class. PersistenceFilter’s auto-save (just before the response commits) caused extra session writes and surprises. Migration: `securityContext((c) -> c.requireExplicitSave(false))`. XML `security-context-explicit-save`. `SessionCreationPolicy.STATELESS` uses **`NullSecurityContextRepository`** (no session write). See [[What is FilterChainProxy and DelegatingFilterProxy]] and [[What is ConcurrentSessionFilter]].

```java
http.securityContext((securityContext) -> securityContext
        .requireExplicitSave(false)); // migration: PersistenceFilter auto-save
```

**Listing 1.** Session-management: SS6 apps should **not** need this. Built-in login filters already call `saveContext` under HolderFilter.

> [!warning] ThreadLocal dies at the end of the request
> After this filter’s `finally`, `SecurityContextHolder` is **empty** on that thread. Async / worker threads need **explicit** propagation (`WebAsyncManagerIntegrationFilter` for servlet async). Do not install PersistenceFilter **and** HolderFilter.

> [!tip] Interview answer
> SecurityContextPersistenceFilter is the old filter that loaded SecurityContext from the session, saved it at the end, and cleared the ThreadLocal. Spring Security 6 replaced it with SecurityContextHolderFilter, which only loads; authentication filters save explicitly. STATELESS uses a null repository so nothing is written to the session.
