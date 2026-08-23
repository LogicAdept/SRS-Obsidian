<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# Can Spring AOP advise private methods?

> [!abstract] Short answer
> **No.** Spring AOP is **proxy-based**. **`private` methods cannot be advised** — they are not overridable on a CGLIB subclass, and they never appear on a JDK interface proxy. Calls to private helpers always go through **`this`** inside the target class, so they never hit the proxy.

## Why private is out of reach

Spring’s proxying docs state it explicitly: **`private` methods cannot be advised, because they cannot be overridden.** Same for **`final`** methods/classes.

| Proxy type | What can be advised (when called **through the proxy**) |
|---|---|
| **JDK dynamic proxy** | Methods on the bean’s **interfaces** (typically **public**) |
| **CGLIB subclass** | Overridable methods — **public** / **protected** (and sometimes package-visible); **not private**, **not final** |

A private method is only callable from inside the same class, so the invocation path is always **direct on the target**, not through the proxy — the same reason **self-invocation** skips advice — [[Why does a self-invocation skip Spring AOP advice]].

```java
@Service
public class OrderService {

    public void place() {
        audit(); // this.audit() — never through the proxy
    }

    @Transactional // useless here under Spring AOP
    private void audit() { /* ... */ }
}
```

**Listing 1.** Even with an annotation on a private method, Spring AOP will not intercept it.

## If you truly need private join points

Use **AspectJ compile-time or load-time weaving**, which injects advice into bytecode instead of wrapping a proxy — [[What is the difference between Spring AOP and AspectJ]], [[Why do you need a Java agent for load-time weaving]].

Usually the better fix is to **extract a public method on another Spring bean** (or make the method package/public and call it through an injected collaborator) so proxy AOP can see the call.

```d2
direction: right
caller: "Other bean" {
  width: 110
  height: 45
  style.fill: "#e3f2fd"
}
proxy: "Spring AOP proxy" {
  width: 140
  height: 50
  style.fill: "#fff3e0"
}
pub: "public method" {
  width: 120
  height: 45
  style.fill: "#e8f5e9"
}
priv: "private helper" {
  width: 120
  height: 45
  style.fill: "#fce4ec"
}

caller -> proxy -> pub -> priv: "this.\n(no advice)"
```

**Fig. 1.** Advice runs only on the proxy → public entry; the private call stays inside the target.

> [!warning] CGLIB is not “all methods”
> Boot’s default **CGLIB** proxies still **cannot** advise `private` or `final` methods. Protected/package-visible methods may be interceptable **only if** the call enters through the proxy — internal `this.` calls still skip advice.

> [!tip] Interview answer
> No — Spring AOP cannot advise private methods. Proxies only intercept external calls to overridable API methods. For private join points you need AspectJ weaving, or refactor so the advised logic is a public method on a Spring bean.
