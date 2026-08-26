<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# What are Spring AOP proxy limitations?

> [!abstract] Short answer
> Spring AOP only advises **method executions** that enter a **runtime proxy**. **Self-invocation** (`this.foo()`) skips advice. **JDK proxies** cover **interface** methods; **CGLIB** cannot advise **`final` classes/methods** or **`private`** methods. Non-Spring objects are not proxied.

## What the proxy can and cannot see

*Proxying Mechanisms* + *AOP Concepts*:

| Limitation | Effect |
| --- | --- |
| **Proxy-only calls** | `this.method()` on the target never re-enters interceptors — [[Why does a self-invocation skip Spring AOP advice]] |
| **Join-point kind** | Method **execution** only — not field get/set, constructors, `call` PCDs |
| **JDK dynamic proxy** | Target must implement an interface; only those interface methods are proxied |
| **CGLIB subclass** | Used when there is no interface (or when forced). **`final` class** cannot be proxied; **`final` / `private`** methods cannot be overridden so they are **not advised** |
| **Visibility** | Package-private methods in a **parent class in another package** are effectively private — not advised |
| **Not a Spring bean** | No auto-proxy — [[Can you use Spring AOP with beans not managed by Spring]] |

```d2
direction: down
ok: "External call\nthrough proxy" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}
skip: "this.foo() / private /\nfinal method" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}

ok -> skip: "not advised"
```

**Fig. 1.** Advice runs only on the green path. Private methods: [[Can Spring AOP advise private methods]]. Proxy kinds: [[What is an AOP proxy in Spring]].

Force CGLIB with `proxyTargetClass=true` if you need class methods that are not on an interface — still subject to `final`/`private`. AspectJ weaving does not have the self-invocation hole because it edits bytecode.

> [!warning] Failed CGLIB advise is often silent
> A `final` method on a CGLIB proxy still **exists**; it just **cannot be overridden**, so annotations on it never run. Tests that only hit `public` entry points miss this.

> [!warning] Interface proxy hides concrete-only methods
> Extra `public` methods on the class that are **not** on the interface are invisible to a JDK proxy.

> [!tip] Interview answer
> **Spring AOP is proxy-based: only external method calls, only overridable methods.** `this` calls skip it. JDK proxies need interfaces; CGLIB cannot wrap `final` or `private`. For constructors, fields, or internal calls, use AspectJ weaving or split beans.
