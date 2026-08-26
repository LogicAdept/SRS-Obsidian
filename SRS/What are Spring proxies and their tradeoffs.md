<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# What are Spring proxies and their tradeoffs?

> [!abstract] Short answer
> Spring AOP **JDK proxies** are lighter and interface-typed; they **miss class-only methods**. **CGLIB** subclasses the target so **class methods** can be advised, but **`final` / `private`** still cannot, constructors/modules have extra constraints, and the runtime type is a generated subclass. **Self-invocation** is a tradeoff of **both**. Pick via `proxyTargetClass` / Boot `spring.aop.proxy-target-class`.

## JDK vs CGLIB in practice

Spring *Proxying Mechanisms* — choose by target shape and what you need to intercept.

| | **JDK dynamic proxy** | **CGLIB subclass** |
| --- | --- | --- |
| Mechanism | `java.lang.reflect.Proxy` | Runtime subclass (Objenesis, often no double constructor) |
| Needs | ≥1 interface | Concrete class that can be extended |
| Advises | Interface methods only | Overridable class methods |
| Fails on | No interface; extra impl-only methods | `final` class; `final`/`private` methods |
| `instanceof` concrete class | **No** | **Yes** (subclass) |

Force CGLIB: `@EnableAspectJAutoProxy(proxyTargetClass = true)` or XML `proxy-target-class="true"`. Several enable annotations **collapse** to the **strongest** setting. Boot often **defaults to CGLIB**. Spring 7: `@Proxyable` per bean.

Shared costs (both kinds): only **method execution**; **`this` calls skip advice**; not a substitute for AspectJ weaving. Details: [[What kinds of proxies exist in Java or Spring]], [[What are Spring AOP proxy limitations]].

```d2
direction: right
jdk: "JDK proxy\ninterface-only" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
cglib: "CGLIB\nsubclass" {
  width: 180
  height: 70
  style.fill: "#fff3e0"
}
self: "this.foo()\nskips both" {
  width: 180
  height: 70
  style.fill: "#ffebee"
}

jdk -> self
cglib -> self
```

**Fig. 1.** Switching proxy type does not fix self-invocation.

> [!warning] CGLIB is not “advise everything”
> `final` methods stay unadvised **silently**. Module-path types in `java.lang` need `--add-opens` — Spring documents this as a CGLIB/Jigsaw limit.

> [!warning] Unified auto-proxy takes the strongest flag
> One `@EnableTransactionManagement(proxyTargetClass = true)` can force **CGLIB for all** auto-proxied beans in that context, including `@Aspect` and `@Async`.

> [!tip] Interview answer
> **JDK proxies: interfaces, no class-only methods. CGLIB: subclass, more methods, but not final/private.** Boot often uses CGLIB by default. Neither sees `this` calls. Use AspectJ weaving when you need those join points.
