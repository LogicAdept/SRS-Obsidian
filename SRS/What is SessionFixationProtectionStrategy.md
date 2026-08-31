<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/SessionManagement #SRS

# What is SessionFixationProtectionStrategy?

> [!abstract] Short answer
> **`SessionFixationProtectionStrategy`** is a `SessionAuthenticationStrategy` that fights session fixation by **`HttpSession.invalidate()`**, then **`getSession()`** for a **new** session, after a successful login. By default it **copies all attributes** to that new session (`migrateSession()`). `newSession()` is the same class with **`migrateSessionAttributes = false`** (application attributes dropped; Spring Security attributes still copied). It is **not** the Servlet 3.1+ default — that is **`ChangeSessionIdAuthenticationStrategy`**.

## Invalidate-and-recreate, not `changeSessionId`

The attack is: the attacker plants a session id, the victim authenticates **with that id**, the attacker reuses the cookie. See [[How do you handle session fixation in Spring Security]].

This class (since 3.0) is the **old-container** defence: if the user **already has a session**, invalidate it and create another, so the planted id is dead. It is a no-op when there is **no session** (unless `alwaysCreateSession`) or when the client’s requested id is **already invalid**. That is why a **`STATELESS`** chain has nothing to rotate — see [[What is SessionCreationPolicy in Spring Security]] and [[What is SessionAuthenticationStrategy]].

It only works if the servlet container **assigns a new session id** after `invalidate()` + `getSession()`. If the container reused the same id, the planted cookie would still win.

On Servlet 3.1+ the configurer default is **`ChangeSessionIdAuthenticationStrategy`** (`HttpServletRequest.changeSessionId()`): **same session object**, new id, attributes never leave. `SessionFixationProtectionStrategy` is what you get from **`migrateSession()`** / **`newSession()`**.

```d2
direction: right
old: "Planted HttpSession" {
  width: 150
  height: 50
  style.fill: "#fce4ec"
}
inv: "invalidate()" {
  width: 130
  height: 50
  style.fill: "#fff3e0"
}
neu: "getSession()\nnew id" {
  width: 150
  height: 50
  style.fill: "#e8f5e9"
}
copy: "copy attributes\n(migrateSession default)" {
  width: 180
  height: 60
  style.fill: "#e3f2fd"
}

old -> inv
inv -> neu
neu -> copy
```

**Fig. 1.** This strategy **destroys** the old session. `changeSessionId` does not — it only renames the id.

```java
http.sessionManagement((session) -> session
    .sessionFixation((fixation) -> fixation.migrateSession()));
```

**Listing 1.** DSL for this class with **all** attributes copied. That is the Servlet **3.0** default, **not** today’s `changeSessionId`.

```java
http.sessionManagement((session) -> session
    .sessionFixation((fixation) -> fixation.newSession()));
```

**Listing 2.** Same class, `setMigrateSessionAttributes(false)`: application attributes discarded; cached-request and other Spring Security attributes **still** migrate (`extractAttributes`).

A successful change publishes **`SessionFixationProtectionEvent`**. In a `CompositeSessionAuthenticationStrategy`, this strategy (or `changeSessionId`) runs **after** concurrent-session control and **before** `RegisterSessionAuthenticationStrategy`, so a rejected extra login does not create a session and the registry records the **new** id. Wiring: [[How do you configure session management in Spring Security]].

> [!warning] Migrating attributes unbinds session-scoped beans
> Copying attributes **removes** them from the old session and **binds** them on the new one. `HttpSessionBindingListener` implementations — including Spring **session-scoped beans** via `DisposableBean` — can run **destroy** on unbind and then break when put back. Prefer `changeSessionId` if you store such objects, or customize `extractAttributes`. `migrateSession()` is **not** “the HttpSecurity spelling of the default strategy” on a current container.

> [!tip] Interview answer
> SessionFixationProtectionStrategy invalidates the existing HttpSession after login and creates a new one so a planted id is useless. migrateSession copies every attribute; newSession keeps only Spring Security attributes. The Servlet 3.1+ default is ChangeSessionIdAuthenticationStrategy instead, which keeps the same session and only changes the id.
