<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS

# How do you fix a circular dependency caused by self-injection in Spring?

> [!abstract] Short answer
> Constructor self-injection (`OrderService(OrderService self)`) is a **one-bean cycle**: the instance cannot finish constructing in order to be injected into itself → `BeanCurrentlyInCreationException`. Official AOP guidance for “I need the **proxy**, not `this`” is: **prefer refactoring** so the call is not a self-invocation; otherwise **inject a self-reference** and call that, not `this`. Make that injection **`@Lazy`** (or `ObjectProvider`) so the container injects a **lazy-resolution proxy** instead of the unfinished singleton ([[What is the Lazy annotation in Spring]]). Do **not** “fix” it by turning circular references back on. `AopContext.currentProxy()` is documented as a last resort.

## Why self-injection exists — and why it cycles

Spring AOP is **proxy-based**. After the call has reached the target, `this.process()` **bypasses** advice (`@Transactional`, `@Async`, …). Current Proxying Mechanisms: **avoid self-invocation** first; else **inject a self reference** and invoke on the proxy; `AopContext.currentProxy()` is **highly discouraged** (and needs `exposeProxy`). AspectJ weaving does not have this `this` problem.

That self-reference is still a **dependency on the bean currently in creation**. A **constructor** argument of the same type is the circular-constructor case the DI chapter forbids ([[Which dependency injection styles do you know]]). Setter/field wiring can expose an early singleton **if** circular references are allowed — **Boot 2.6+** (and AOT) treat that as something to **avoid**; AOT docs: use **`@Lazy` injection points or `ObjectProvider`**, not setter cycles.

```java
@Service
public class OrderService {

    private final OrderService self;

    public OrderService(@Lazy OrderService self) {
        this.self = self;
    }

    public void submit() {
        self.process();
    }

    @Transactional
    public void process() { /* advised */ }
}
```

**Listing 1.** Conceptual. `@Lazy` on the **injection point** inserts a proxy now; the real singleton is resolved on first `self.process()`. `this.process()` would skip the transaction interceptor.

Better still: move `process` to another bean (`OrderProcessor`) so there is **no** self-call. That is the AOP chapter’s least-invasive fix.

```d2
direction: down
client: "client → proxy" {
  width: 180
  height: 36
  style.fill: "#e8f5e9"
}
target: "target this.process()" {
  width: 200
  height: 40
  style.fill: "#ffebee"
}
self: "self.process() via @Lazy" {
  width: 220
  height: 40
  style.fill: "#fff3e0"
}

client -> target
client -> self
```

**Fig. 1.** Advice runs only through the proxy. `@Lazy` self is that proxy; `this` is not.

> [!warning] `@Lazy` self is not optional `null`
> The proxy is always injected. A missing bean fails on **first call**. `ObjectProvider<OrderService>` is for delayed `getObject()` / optionality. Do not `@Autowired` self on a `BeanPostProcessor`.

> [!warning] Enabling circular references is not the design fix
> `spring.main.allow-circular-references` (Boot **2.6+**, default **off**) only restores the old early-singleton trick. It does not make constructor self-injection valid, and AOT still rejects explicit cycles. Prefer extract-a-bean or `@Lazy` / `ObjectProvider`.

> [!tip] Interview answer
> Self-injection is usually to call your own proxied method because this skips @Transactional. Constructor-injecting this same bean is a circular dependency. Inject a @Lazy self-reference or ObjectProvider, or better split the advised method onto another bean. AopContext.currentProxy is the documented last resort.
