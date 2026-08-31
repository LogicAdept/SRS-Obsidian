<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/SessionManagement #SRS

# How do you handle session fixation in Spring Security?

> [!abstract] Short answer
> Spring Security already runs session-fixation protection **on login** by changing the session id (or creating a new session) so an attacker who planted an id cannot keep the authenticated session. On Servlet 3.1+ the default is **`changeSessionId`** (`HttpServletRequest.changeSessionId()`). Override it with `http.sessionManagement(sm -> sm.sessionFixation(...))` — `migrateSession`, `newSession`, or `none` (not recommended unless something else already changes the id).

## The attack and the default defence

The attacker obtains a session id (visits the site, or stuffs an id into a link), tricks the victim into authenticating **with that same id**, then reuses the cookie. Protection is a `SessionAuthenticationStrategy` invoked when authentication succeeds — from Spring Security 6, by the authenticating filter itself, not by a default `SessionManagementFilter`. See [[What is SessionAuthenticationStrategy]] and [[How do you configure session management in Spring Security]].

The default implementation is `ChangeSessionIdAuthenticationStrategy`: **same `HttpSession` object**, new id, **all attributes kept**. It needs Servlet 3.1+; asking for `changeSessionId` on an older container throws. Servlet 3.0 and older defaulted to **`migrateSession`**.

```d2
direction: right
plant: "Attacker plants\nsession id" {
  width: 160
  height: 60
  style.fill: "#fce4ec"
}
login: "Victim logs in" {
  width: 150
  height: 50
  style.fill: "#fff3e0"
}
sas: "SessionAuthenticationStrategy\nchangeSessionId (default)" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
safe: "New id; planted\ncookie is useless" {
  width: 170
  height: 60
  style.fill: "#e3f2fd"
}

plant -> login
login -> sas
sas -> safe
```

**Fig. 1.** Fixation is “reuse the pre-login id after authenticate.” The strategy breaks that by changing the id (or replacing the session) before the response goes back.

```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http
        .sessionManagement((session) -> session
            .sessionFixation((fixation) -> fixation.changeSessionId())
        );
    return http.build();
}
```

**Listing 1.** Explicit `changeSessionId` — the Servlet 3.1+ default. Omit the block and you get the same strategy (`ChangeSessionIdAuthenticationStrategy`).

## The four `sessionFixation` options

| DSL | What happens on login |
|---|---|
| **`changeSessionId()`** | `HttpServletRequest.changeSessionId()`; keep the session and **all** attributes. Default on Servlet 3.1+. |
| **`migrateSession()`** | Invalidate, `getSession()` for a new session, **copy every attribute**. Default on Servlet 3.0 or older. Implemented by `SessionFixationProtectionStrategy` with attribute migration on. |
| **`newSession()`** | Same invalidate-and-create, but **application** attributes are **not** copied. Spring Security attributes (for example a cached request) **still move**. |
| **`none()`** | No fixation protection. Useful only if the **container** already changes the id; otherwise it leaves cookie sessions open to the attack. |

```java
http.sessionManagement((session) -> session
    .sessionFixation((fixation) -> fixation.newSession()));
```

**Listing 2.** `newSession` — new session id **and** drop application attributes. Do not confuse this with `migrateSession()`, which copies everything.

`SessionFixationProtectionStrategy` (the invalidate-and-recreate path) only works if the container **assigns a new id** after `invalidate()` + `getSession()`. It also publishes `SessionFixationProtectionEvent`. `changeSessionId` publishes that event **and** notifies `HttpSessionIdListener`s — listeners that handle both will see two callbacks. Supplying a custom `sessionAuthenticationStrategy(...)` **replaces** the default fixation strategy (and on Security 6’s default chain that DSL method **throws**; set the strategy on the authenticating filter). Details: [[What is SessionFixationProtectionStrategy]].

## When the strategy does nothing

`AbstractSessionFixationProtectionStrategy` **skips** the change if there is **no session**, unless `alwaysCreateSession` is set. If the client’s requested id is **already invalid**, it also does nothing — there is nothing to steal. A **`STATELESS`** chain (`NullSecurityContextRepository`) typically never has a servlet session, so there is no id to migrate; pair that policy with token auth instead of cookie sessions. See [[What is SessionCreationPolicy in Spring Security]].

> [!warning] `migrateSession()` is not today’s default
> Interview dumps that “add” `sessionFixation().migrateSession()` are restating the **Servlet 3.0** default. On a current container the default is **`changeSessionId`**. `newSession()` does **not** drop Spring Security attributes — only application attributes. `none()` is **not** “fine for APIs”; it is for an **already protected** container, and the docs mark it as not recommended otherwise.

> [!warning] Migrating attributes can destroy session-scoped beans
> `migrateSession` unbinds attributes from the old session and binds them on the new one. Objects that implement `HttpSessionBindingListener` (including Spring **session-scoped beans** via `DisposableBean`) can run **destroy** logic on the unbind and then fail when put back. Do not store such objects if you migrate; use `changeSessionId` (attributes never leave the session) or a custom strategy.

> [!tip] Interview answer
> Session fixation is planting a session id, letting the victim log in, then reusing that cookie. Spring Security’s default SessionAuthenticationStrategy calls changeSessionId on Servlet 3.1+ so the planted id is dead after login. migrateSession copies all attributes into a new session and is the old default; newSession keeps only Spring Security attributes; none() turns protection off and is not recommended for cookie sessions.
