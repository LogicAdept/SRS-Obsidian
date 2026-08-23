<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Framework/AOP #SRS

# Why does method security skip self-invocation?

> [!abstract] Short answer
> **Method security is enforced by Spring AOP advisors on the bean proxy.** A call like **`this.securedMethod()`** from inside the same class is a **direct `this` reference** on the target object — it **never enters the proxy**, so **`@PreAuthorize`**, **`@PostAuthorize`**, **`@Secured`**, and related interceptors **do not run**.

## Proxy boundary, not URL boundary

With **`@EnableMethodSecurity`** (default **`mode = AdviceMode.PROXY`**), Spring Security registers **method interceptors** that match annotated methods. An external caller invokes the **proxy**; the interceptor runs **before** (or **after**, for **`@PostAuthorize`**) the target method.

The method-security guide describes this flow explicitly: **Spring AOP invokes the proxy method**, then **`AuthorizationManagerBeforeMethodInterceptor`** evaluates **`@PreAuthorize`** before the real method body runs.

Inside the target instance, **`this.otherMethod()`** is not a proxy call. Spring Framework's proxying documentation states that **self-invocation via `this` bypasses the advice** — the same rule applies to **`@Transactional`**, **`@Cacheable`**, and method security.

```java
@Service
public class OrderService {

    public void placeOrder(Order order) {
        this.validateOwner(order); // @PreAuthorize never runs
    }

    @PreAuthorize("hasAuthority('order:validate')")
    public void validateOwner(Order order) { /* ... */ }
}
```

**Listing 1.** Conceptual bug — only a cross-bean call (or a self-proxy) triggers authorization.

```d2
direction: right
client: "Other bean\ncalls proxy" {
  width: 160
  height: 60
  style.fill: "#e8f5e9"
}
proxy: "Spring proxy\n@PreAuthorize interceptor" {
  width: 180
  height: 60
  style.fill: "#e3f2fd"
}
target: "Target instance\nthis.secured()" {
  width: 180
  height: 60
  style.fill: "#fce4ec"
}
skip: "Advice skipped\n(no proxy hop)" {
  width: 160
  height: 50
  style.fill: "#ffcdd2"
}

client -> proxy -> target
target -> skip: "internal call"
```

**Fig. 1.** External calls hit advisors; in-class `this` calls do not.

## Fixes and alternatives

| Approach | Idea |
|---|---|
| **Refactor to another bean** | Move secured methods to a separate **`@Service`** and inject it — the recommended fix in Spring's AOP docs |
| **Self-injection** | Inject **`@Lazy`** self-reference and call **`self.securedMethod()`** through the proxy |
| **`AdviceMode.ASPECTJ`** | **`@EnableMethodSecurity(mode = AdviceMode.ASPECTJ)`** weaves advice into bytecode so self-calls are advised — requires AspectJ setup |
| **`AopContext.currentProxy()`** | Discouraged last resort; needs **`exposeProxy = true`** |

AspectJ compile-time or load-time weaving **does not suffer the self-invocation gap** because advice is applied in bytecode, not only on the proxy surface. See [[When should you use AspectJ mode for method security]] and [[What is the difference between Spring AOP and AspectJ]].

> [!warning] URL rules do not compensate
> A controller may pass **`authorizeHttpRequests`**, but **`this.secured()`** inside the same service still skips method security. Defense in depth requires **cross-bean** calls or AspectJ mode — not assuming the filter chain already checked the user. See [[Why does method security still matter if URL rules exist]] and [[What is EnableMethodSecurity]].

> [!tip] Interview answer
> Method security uses Spring AOP proxies. this.securedMethod() inside the same class bypasses the proxy, so @PreAuthorize never runs. Fix by moving the method to another bean, self-injecting the proxy, or switching to @EnableMethodSecurity(mode = AdviceMode.ASPECTJ) when bytecode weaving is acceptable.
