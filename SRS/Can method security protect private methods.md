<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Framework/AOP #SRS

# Can method security protect private methods?

> [!abstract] Short answer
> **No, not in default proxy mode.** Method security is Spring AOP. **`private` methods cannot be advised** (they cannot be overridden on a CGLIB subclass and never appear on a JDK interface proxy). A private helper is only reachable via **`this`**, so `@PreAuthorize` / `@Secured` never run. **`final`** methods/classes have the same override problem.

## Why the interceptor never sees it

`@EnableMethodSecurity` defaults to **`AdviceMode.PROXY`**. Advisors wrap the **bean proxy**. Spring’s *Proxying Mechanisms*: **private methods cannot be advised, because they cannot be overridden.** Package-private methods on a **parent in another package** are treated the same way.

A private method is only callable from inside the same class, so the path is always **direct on the target** — the same hole as self-invocation of a public method — [[Why does method security skip self-invocation]], [[Can Spring AOP advise private methods]].

```java
@Service
public class OrderService {

    public void place(Order order) {
        this.checkOwner(order); // never enters the proxy
    }

    @PreAuthorize("hasAuthority('order:check')")
    private void checkOwner(Order order) { /* ... */ }
}
```

**Listing 1.** Conceptual double miss — private (not overridable) **and** `this.` (no proxy hop). Annotating the public `place` method is what the interceptor can see.

```d2
direction: right
client: "Other bean" {
  width: 120
  height: 50
  style.fill: "#e8f5e9"
}
proxy: "Method-security proxy" {
  width: 180
  height: 55
  style.fill: "#e3f2fd"
}
pub: "public place()" {
  width: 140
  height: 50
  style.fill: "#fff3e0"
}
priv: "private @PreAuthorize" {
  width: 180
  height: 55
  style.fill: "#ffcdd2"
}

client -> proxy -> pub -> priv: "this.\n(skipped)"
```

**Fig. 1.** Only the public entry through the proxy is a join point for default method security.

## What actually works

Put the annotation on a **public** (or otherwise overridable) method that callers invoke **through the injected bean**. Extract a second `@Service` if the check must stay a separate method. **`AdviceMode.ASPECTJ`** weaves bytecode so **self-invocation** of public methods is advised — that is a different switch, with a weaver — [[When should you use AspectJ mode for method security]]. Do not treat “AspectJ mode” as a reason to keep security on `private` helpers in proxy-mode apps.

> [!warning] CGLIB does not save private
> Boot often uses class-based proxies. They still **cannot** override `private` or `final`. A compiling `@PreAuthorize` on a private method is a silent no-op under `AdviceMode.PROXY`.

> [!tip] Interview answer
> Default method security cannot protect private methods. Proxies only intercept external calls to overridable methods. A private `@PreAuthorize` helper called from `this` is skipped twice. Put the annotation on the public API, or split a bean.
