<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/SelfInvocation #Java/Spring/Framework/AOP #SRS

# How would you explain self-invocation?

> [!abstract] Short answer
> **Self-invocation** is `this.otherMethod()` (or an implicit `this`) **inside the same Spring bean**. Default **proxy** AOP intercepts only **external** calls. The inner call hits the **target**, not the proxy, so `@Transactional`, `@Async`, `@Cacheable`, and other proxy advice on that inner method **do not run**. Spring’s preferred fix is to **stop calling yourself** — move the advised method to **another bean**. Alternatives: **self-injection** of the proxy, or **AspectJ** compile/load-time weaving. `AopContext.currentProxy()` is discouraged.

## Proxy vs `this`

Client code holds the **proxy**. `proxy.foo()` runs interceptors, then the **target** `foo()`. Inside `foo()`, `this.bar()` is a plain Java call on the target — advice for `bar()` never sees it ([[Why does a self-invocation skip Spring AOP advice]], [[What is the difference between a self-invocation and a cross-bean Transactional call]]).

`@Transactional` in **proxy** mode (the default) states the same: self-invocation does **not** start a transaction at runtime even if the callee is annotated. Do not rely on this in `@PostConstruct` — the proxy may not be ready ([[When should you use AspectJ mode for Transactional self-invocation]]).

```java
@Service
public class OrderService {

	@Transactional
	public void place(Order order) {
		this.persist(order); // @Transactional on persist is ignored
	}

	@Transactional(propagation = Propagation.REQUIRES_NEW)
	public void persist(Order order) { /* ... */ }
}
```

**Listing 1.** Conceptual. `REQUIRES_NEW` never starts; both methods run in whatever transaction (if any) already exists on the outer call — or none.

```d2
direction: right
client: "Other bean" {
  width: 120
  height: 50
  style.fill: "#e8f5e9"
}
proxy: "Spring proxy" {
  width: 140
  height: 50
  style.fill: "#e3f2fd"
}
target: "this.persist()\nno interceptor" {
  width: 180
  height: 55
  style.fill: "#ffebee"
}
client -> proxy: "place()"
proxy -> target: "after advice"
```

**Fig. 1.** Only the inbound `place()` call is advised.

## What Spring documents as fixes

1. **Avoid self-invocation** — extract the inner method to a **separate bean** (AOP proxying: best / least invasive; `@Autowired` chapter: factor out a delegate; self-injection is a **last resort**).
2. **Inject a self-reference** and call the **proxy**, not `this` (`@Autowired` considers self references as fallback; `@Resource` by unique name can return the proxy).
3. **AspectJ `mode`** — no proxy; bytecode weaving, so inner calls are advised. Needs `spring-aspects` and compile-time or load-time weaving.
4. **`AopContext.currentProxy()`** — highly discouraged; couples the class to Spring AOP and needs `exposeProxy`.

> [!warning] Self-injection is not the first design
> Official `@Autowired` text: use a self-reference **only as a last resort** to go through the transactional proxy. Prefer another bean. `@Lazy` on the self field is a circular-creation trick, not the documented primary fix.

> [!tip] Interview answer
> this.inner() skips the Spring proxy, so the inner @Transactional never runs. Same for @Async and @Cacheable. Split the method onto another bean, or weave with AspectJ. Injecting self to call the proxy works but is a last resort; AopContext.currentProxy is worse.
