<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/Authentication #SRS

# What is the difference between `SecurityContextHolderFilter` and `SecurityContextPersistenceFilter`?

> [!abstract] Short answer
> Both sit **early** in the servlet chain and **load** `SecurityContext` from a **`SecurityContextRepository`** into **`SecurityContextHolder`**. **`SecurityContextPersistenceFilter`** (legacy, **deprecated**) also **auto-saved** the context just before the response committed and **cleared** the holder. **`SecurityContextHolderFilter`** (since **5.7**, Spring Security **6 default**) **only reads**. Authentication filters must **`saveContext` explicitly** (`requireExplicitSave` **true**). Use **one**, never both. TRACE **`(3/15)`** is the new filter (`FilterOrderRegistration` **700** vs Persistence **800**).

## Load vs load-and-save

```d2
direction: down
repo: "SecurityContextRepository" {
  width: 240
  height: 40
}
old: "SecurityContextPersistenceFilter\nload + auto-save + clear" {
  width: 320
  height: 50
  style.fill: "#fff3e0"
}
new: "SecurityContextHolderFilter\nload + clear; save is explicit" {
  width: 340
  height: 50
  style.fill: "#e8f5e9"
}

repo -> old: "SS5 default"
repo -> new: "SS6 default"
```

**Fig. 1.** Auto-save was surprising (writes just before commit, extra `HttpSession` hits). The new filter removes that. `http.securityContext((c) -> c.requireExplicitSave(false))` puts the old filter back for migration. See [[What is SecurityContextHolderFilter]], [[What is SecurityContextPersistenceFilter]], and [[What is FilterOrderRegistration]].

Both **clear `SecurityContextHolder` in `finally`**. Skip that and a pooled worker can keep the previous user’s `Authentication`. That leak is **not** unique to one class.

```java
http.securityContext((securityContext) -> securityContext
        .requireExplicitSave(true));
```

**Listing 1.** SS6 default. `true` → `SecurityContextHolderFilter`. Form login / HTTP Basic already call `saveContext`. A **custom** auth filter must do it too. See [[What is UsernamePasswordAuthenticationFilter]] and [[What is SessionManagementFilter]] (also **not** in the SS6 default chain).

> [!warning] Never register both
> Official session-management: an app should have **either** `SecurityContextHolderFilter` **or** `SecurityContextPersistenceFilter`, **never both**. Dump line “HolderFilter saves at the end” is the **old** filter. If login works for this request but the next GET is anonymous, you loaded with the new filter and **never saved**.

> [!tip] Interview answer
> SecurityContextPersistenceFilter was the old filter that loaded the SecurityContext, auto-saved it, and cleared the ThreadLocal. SecurityContextHolderFilter is the Spring Security 6 replacement: it only loads and still clears at the end, so authentication filters must save explicitly. You should never run both. The TRACE slot is the new filter, around order 700.
