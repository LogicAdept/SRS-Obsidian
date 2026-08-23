<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/SelfInvocation #SRS

# How do you make an inner `Transactional` method honor its annotation?

> [!abstract] Short answer
> In default **proxy** mode, `this.inner()` never hits the transaction interceptor. Make the call go through the **Spring proxy** (extract a second bean, inject a self-reference and call that, or — last resort — `AopContext.currentProxy()`), switch to **AspectJ** transaction mode so bytecode weaving applies advice on self-calls, or open the boundary with `TransactionTemplate` instead of a second `@Transactional`.

## Why `this.inner()` ignores `@Transactional`

Spring’s default `@EnableTransactionManagement` mode is `proxy`. Only calls that enter through the proxy are advised. Once execution is inside the target instance, `this.audit()` is a plain Java call on the target, so the inner method’s `@Transactional` attributes (propagation, rollback rules, timeout, …) never run. Same proxy boundary as [[What is the difference between a self-invocation and a cross-bean Transactional call]] and [[Why does a self-invocation skip Spring AOP advice]].

```d2
direction: down
client: "Other bean\ncalls proxy" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
proxy: "Spring proxy\nTransactionInterceptor" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
outer: "target.outer()\n@Transactional" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
bypass: "this.inner()\nbypasses proxy" {
  width: 260
  height: 80
  style.fill: "#ffebee"
}
honor: "proxy.inner() or woven call\nhonors @Transactional" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}

client -> proxy
proxy -> outer
outer -> bypass
proxy -> honor
```

**Fig. 1.** Self-invocation skips the proxy; a proxied or AspectJ-woven call does not.

## Preferred fixes (proxy mode)

Spring’s AOP proxy docs rank the options: **refactor away self-invocation**, then **self-injection**, and treat `AopContext.currentProxy()` as a discouraged last resort. AspectJ mode is the alternative when you want self-calls advised without changing call sites.

```java
@Service
public class OrderService {

    private final AuditService auditService; // separate bean → always proxy

    public OrderService(AuditService auditService) {
        this.auditService = auditService;
    }

    @Transactional
    public void placeOrder(Order order) {
        // ...
        auditService.writeAudit(order); // crosses the proxy
    }
}

@Service
public class AuditService {

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void writeAudit(Order order) {
        // ...
    }
}
```

**Listing 1.** Conceptual: move the inner `@Transactional` method to another Spring bean so the call is external.

```java
@Service
public class OrderService {

    private final OrderService self;

    public OrderService(@Lazy OrderService self) {
        this.self = self; // injected reference is the proxy
    }

    @Transactional
    public void placeOrder(Order order) {
        self.writeAudit(order);
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void writeAudit(Order order) {
        // ...
    }
}
```

**Listing 2.** Conceptual: self-injection. Constructor self-injection often needs `@Lazy` to break the circular dependency; the field must be the proxy, not `this`.

```java
((OrderService) AopContext.currentProxy()).writeAudit(order);
```

**Listing 3.** Conceptual last resort. Requires the proxy to be exposed (`factory.setExposeProxy(true)`, or equivalent on the auto-proxy infrastructure). Couples the class to Spring AOP; Spring’s docs discourage this.

## AspectJ mode and programmatic boundaries

```java
@EnableTransactionManagement(mode = AdviceMode.ASPECTJ)
```

**Listing 4.** Conceptual: AspectJ mode weaves the transaction aspect into the class bytecode so self-invocations are advised. Needs `spring-aspects` and compile-time or load-time weaving. See [[When should you use AspectJ mode for Transactional self-invocation]].

When you only need a nested or separate boundary and do not want a second declarative method, drive the resource transaction with `TransactionTemplate` / `PlatformTransactionManager` from the outer method. That does not “fix” `@Transactional` on `this.inner()`; it replaces that annotation with an explicit programmatic scope.

> [!warning] Exposing the proxy is mandatory for `AopContext`
> `AopContext.currentProxy()` throws if the current invocation did not expose the proxy. Turning on exposure only for a quick demo still leaves the class tied to Spring AOP and easy to break in tests that call the target directly.

> [!warning] Visibility and proxy type still apply
> Even after you route through a proxy, non-public methods are not reliably advised under Spring’s proxy-based model, and `final` methods cannot be overridden by a CGLIB subclass. Extracting a bean or using AspectJ does not remove those constraints for proxy mode.

> [!tip] Interview answer
> Default Spring transactions are **proxy-based**, so `this.inner()` never sees `@Transactional`. Fix it by calling through another bean or an injected self-proxy, enable **AspectJ** transaction mode if you need true self-invocation advice, or use `TransactionTemplate`. Avoid `AopContext.currentProxy()` unless you accept the AOP coupling and `exposeProxy` requirement.
