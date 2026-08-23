<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# Why does a self-invocation skip Spring AOP advice?

> [!abstract] Short answer
> **Spring AOP advises the proxy, not the raw target object.** External callers invoke the **proxy**, which runs interceptors then delegates to the target. **`this.otherMethod()`** inside the same class is a **direct call on `this`** (the target) — it **never re-enters the proxy**, so **`@Transactional`**, **`@Async`**, **`@Cacheable`**, **`@PreAuthorize`**, and custom **`@Around`** advice on the inner method **do not run**.

## Proxy vs target

Spring Framework's proxying documentation explains the sequence:

1. Client holds a reference to the **proxy**.
2. **`proxy.foo()`** runs advice, then invokes **`SimplePojo.foo()`** on the target.
3. Inside **`foo()`**, **`this.bar()`** calls **`bar()` on the target directly** — **not** on the proxy.
4. Advice registered for **`bar()`** is **bypassed**.

That limitation applies to **Spring's default proxy-based AOP** (JDK dynamic proxies or CGLIB subclasses). It is the same boundary that breaks nested **`@Transactional`** propagation when both methods sit on one bean.

```java
@Service
public class ReportService {

    public Report generate() {
        return this.buildCachedSection(); // @Cacheable ignored
    }

    @Cacheable("sections")
    public Report buildCachedSection() { /* ... */ }
}
```

**Listing 1.** Self-call skips cache/transaction/security interceptors on the inner method.

```d2
direction: right
client: "External caller" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}
proxy: "Spring proxy\n(advice chain)" {
  width: 160
  height: 60
  style.fill: "#e3f2fd"
}
target: "Target bean\nthis.inner()" {
  width: 160
  height: 60
  style.fill: "#fff3e0"
}
skip: "Advice on inner\nmethod skipped" {
  width: 160
  height: 50
  style.fill: "#ffcdd2"
}

client -> proxy -> target
target -> skip: "direct this call"
```

**Fig. 1.** Only the first hop crosses the proxy; in-class `this` calls stay inside the target.

## Fixes (Spring's recommended order)

| Approach | Notes |
|---|---|
| **Refactor to another bean** | Preferred — inject a collaborator; the call is naturally cross-bean and proxied |
| **Self-injection** | Inject **`@Lazy`** self (or **`ObjectProvider`**) and call **`self.innerMethod()`** through the proxy |
| **AspectJ weaving** | **`@EnableAspectJAutoProxy`** is still proxy mode; use **compile-time / load-time AspectJ** (or **`AdviceMode.ASPECTJ`** on feature annotations) so advice is woven into bytecode — **no self-invocation gap** |
| **`AopContext.currentProxy()`** | Last resort; requires **`exposeProxy = true`** on the auto-proxy creator — couples code to Spring AOP |

AspectJ compile-time and load-time weaving **does not have this self-invocation problem** because advice is applied in **bytecode**, not only on the proxy wrapper. See [[What is the difference between Spring AOP and AspectJ]] and [[When should you use AspectJ mode for Transactional self-invocation]].

> [!warning] `AopContext.currentProxy()` is off by default
> **`AopContext.currentProxy()`** throws unless the active invocation **exposed the proxy**. It ties business code to Spring AOP APIs and breaks tests that call the plain target. Prefer refactoring or self-injection. Transaction-specific nuance: [[What is the difference between a self-invocation and a cross-bean Transactional call]]. Method-security variant: [[Why does method security skip self-invocation]].

> [!tip] Interview answer
> Spring AOP wraps the bean in a proxy. Calls through the proxy run advice; this.innerMethod() inside the same class hits the target directly and skips @Transactional, @Cacheable, @Async, and other interceptors. Fix by moving the method to another bean, self-injecting the proxy, or using AspectJ weaving instead of proxy-only AOP.
