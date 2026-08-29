<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #SRS

# What is global-session bean scope in Spring?

> [!abstract] Short answer
> `globalSession` (XML `scope="globalSession"`, formerly `WebApplicationContext.SCOPE_GLOBAL_SESSION`) bound a bean to the **Portlet global `PortletSession`** (`APPLICATION_SCOPE` — shared by every portlet in the app), not the per-portlet session. It existed only on a **web-aware** `ApplicationContext`. **Spring Framework 5.0 dropped it** from the built-in scope table (six scopes remain). Current `WebApplicationContext` has `SCOPE_REQUEST` / `SCOPE_SESSION` / `SCOPE_APPLICATION` only — no `SCOPE_GLOBAL_SESSION`. Servlet apps that still listed `globalSession` on **4.x** silently used ordinary HTTP `session`; they did **not** get a second session type.

## Portlet “application session,” not a seventh Servlet scope

Through Spring Framework **4.3**, the reference listed **seven** built-in scopes. The extra web one was `globalSession`:

```xml
<bean id="userPreferences" class="example.UserPreferences" scope="globalSession"/>
```

**Listing 1.** Conceptual. 4.x Portlet metadata. There was no `@GlobalSessionScope` counterpart to `@SessionScope`.

The Portlet spec has two session maps on one `PortletSession`:

- **`session`** — portlet (component) scope (`PORTLET_SCOPE`). Default `SessionScope`.
- **`globalSession`** — application scope (`APPLICATION_SCOPE`), one map for the whole portlet web app.

`SessionScope(boolean globalSession)` selected that distinction. **In a Servlet environment the flag was ignored**; `ServletRequestAttributes` has **no** session vs global-session split. The 4.x reference stated the same: a Servlet app with `scope="globalSession"` used **standard HTTP `Session` scope and raised no error**.

Like other web scopes, `globalSession` required a web-aware context (`XmlWebApplicationContext` and friends). A `ClassPathXmlApplicationContext` threw `IllegalStateException` for an unknown scope ([[What are Spring bean scopes]]). Injecting a short-lived web scope into a singleton still needed a scoped proxy ([[What is ObjectProvider and a scoped proxy in Spring]]).

```d2
direction: down
sf4: "Spring Framework 4.x" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
portlet: "Portlet\nglobalSession = APPLICATION_SCOPE" {
  width: 280
  height: 60
  style.fill: "#fff3e0"
}
servlet: "Servlet\nsilently = HTTP session" {
  width: 260
  height: 60
  style.fill: "#fff8e1"
}
sf5: "Spring Framework 5.0+\nnot in the six built-in scopes" {
  width: 280
  height: 60
  style.fill: "#fce4ec"
}

sf4 -> portlet
sf4 -> servlet
portlet -> sf5: removed
servlet -> sf5: removed
```

**Fig. 1.** `globalSession` was a Portlet lifetime; Servlet 4.x aliased it; 5+ does not register the name.

## Removed with Portlet support

Spring Framework **5.0** reference: **six** scopes — `singleton`, `prototype`, `request`, `session`, `application`, `websocket`. Current Framework (7.0) is the same table. `SessionScope` is a **no-arg** constructor only. `spring-webmvc-portlet` / `DispatcherPortlet` are 4.x-era types.

A Spring Boot servlet or WebFlux app ([[What ApplicationContext type does Spring Boot create for a web app]]) should use `session` (HTTP `HttpSession`) or `application` (`ServletContext`) — never `globalSession`. Today an unregistered `scope="globalSession"` is an **unknown scope**, not a quiet alias.

> [!warning] Interview lists that still recite seven web-ish scopes
> `global-session` is a **4.x Portlet** answer. Naming it for a Boot REST service is a stale-list trap. Current docs do not describe it.

> [!warning] Servlet 4.x hid the mistake
> On Spring 4 Servlet stacks, `globalSession` did **not** fail; it was HTTP `session`. That is why old XML can look “fine” until you move to Framework 5+, where the name is gone.

> [!tip] Interview answer
> globalSession scoped a bean to the Portlet application-wide session, as opposed to the per-portlet session. Servlet apps on Spring 4 treated it as normal HTTP session with no error. Spring Framework 5 removed the scope with Portlet support; use session or application instead.
