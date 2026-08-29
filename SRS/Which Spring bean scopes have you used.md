<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #Career/Experience #SRS

# Which Spring bean scopes have you used?

> [!abstract] Short answer
> Answer with **named built-in scopes you actually configured**, not “I used Spring so I used scopes.” Official table: **six** — **`singleton`** (default; **most beans**), **`prototype`**, plus **web-only** **`request`**, **`session`**, **`application`**, **`websocket`**. **`globalSession` is gone** (5.0+). **`SimpleThreadScope` is not registered** until you call `registerScope`. If you only ever omitted `@Scope`, you have used **singleton** — including `@RestController` ([[What is the default Spring bean scope]], [[Which Spring bean scopes fit most application types]]). Do not claim `request` because HTTP happened.

## How to answer (not a fake résumé)

This cue is **experience**. The Framework cannot document *your* tickets. It **does** document which names are **honest**.

| Say you used | Only if you… |
|---|---|
| **`singleton`** | Shipped any Spring app. Default on `@Component` / `@Bean` / MVC controllers ([[What is the default scope of a Spring MVC controller]]) |
| **`prototype`** | Set `scope="prototype"` / `@Scope("prototype")` because of **conversational state**, and knew a singleton **field still captures one** ([[When would you use prototype scope in Spring]]) |
| **`request` / `session`** | Annotated `@RequestScope` / `@SessionScope` (or XML `scope`) **and** a **web-aware** context. Mention **scoped proxy** / `ObjectProvider` if a singleton depended on it ([[What is ObjectProvider and a scoped proxy in Spring]]) |
| **`application`** | Needed one instance per **`ServletContext`**, not per `ApplicationContext` |
| **`websocket`** | STOMP-over-WebSocket session beans, not “we had SockJS” |
| **Custom (`thread`, …)** | Implemented `Scope` and **`registerScope` / `CustomScopeConfigurer`** ([[How do you register a custom Spring bean scope]]) |

```java
@Service
class InvoiceService { }                 // singleton — say this if that is all you did

@Component
@Scope("prototype")
class ImportCommand { }                  // only if you really declared it

@Component
@RequestScope
class LoginAction { }                    // only with a web-aware context
```

**Listing 1.** Conceptual **labels** for the spoken answer. Replace types with **yours**. `@RequestScope` on a CLI `ClassPathXmlApplicationContext` is **`IllegalStateException`**, not experience ([[What are Spring bean scopes]]).

```d2
direction: down
q: "Which scopes have you used?" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}
always: "singleton (default)" {
  width: 200
  height: 36
  style.fill: "#e8f5e9"
}
maybe: "prototype / request / session\nif you set them" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
no: "globalSession / unregistered thread" {
  width: 280
  height: 40
  style.fill: "#ffebee"
}

q -> always
q -> maybe
q -> no
```

**Fig. 1.** Recite **what you configured**. Reciting the six-row table is not use. Do not list **`globalSession`** ([[What is global-session bean scope in Spring]]).

> [!warning] HTTP traffic is not `request` scope
> A singleton controller serving many requests is still **singleton**. Per-request **data** on method arguments is not a scoped bean. Claiming `request` without `@RequestScope` / XML `scope="request"` (or equivalent) is the usual fail.

> [!warning] Do not pad with `prototype` for thread-safety
> Prototype is **stateful independent instances**, not a lock. If you never wrote `@Scope("prototype")` and never used `ObjectProvider`/`@Lookup` for a new instance per call, say **singleton only**.

> [!tip] Interview answer
> I have used singleton on every Spring service and controller — that is the default, including in web apps. I use prototype only for stateful commands and then ObjectProvider or @Lookup so a singleton does not capture one instance. I name request or session only when I actually declared those scopes on a web-aware context. I do not claim globalSession or a thread scope I never registered.
