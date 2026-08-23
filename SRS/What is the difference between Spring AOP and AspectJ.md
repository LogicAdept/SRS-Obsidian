<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# What is the difference between Spring AOP and AspectJ?

> [!abstract] Short answer
> **Spring AOP** is a **proxy-based** framework that advises **method executions on Spring beans** at runtime. **AspectJ** is a **full AOP language/weaver** (compile-time or load-time bytecode) that can advise many join-point kinds — including field access, constructors, and objects **outside** the Spring container. Spring often uses **AspectJ’s annotation/pointcut language** (`@Aspect`, `@Before`, …) while still weaving through **Spring proxies**, unless you opt into real AspectJ weaving.

## Side-by-side

| | **Spring AOP** | **AspectJ** |
|---|---|---|
| **Mechanism** | JDK / CGLIB **proxies** | Bytecode **weaving** (CTW / LTW) |
| **Join points** | Method execution on Spring beans | Method, field get/set, constructors, … |
| **Targets** | Beans in the Spring context | Any class the weaver reaches |
| **Self-invocation** | `this.foo()` **skips** advice | Advice applies inside the class |
| **Setup** | No separate weave step | AspectJ compiler / agent / weaver |

Spring’s capabilities chapter: Spring AOP **only** supports method-execution join points; for field interception, use AspectJ. Choosing-style docs: prefer Spring AOP when you only need to advise Spring beans; use AspectJ for non-managed objects or richer join points — [[What is aspect oriented programming AOP]].

## “Uses AspectJ” ≠ “is AspectJ weaving”

`@Aspect` + AspectJ pointcut expressions are the **programming model**. Default Spring Boot/Framework still creates a **proxy** around the bean. Full AspectJ weaving is a different mode (e.g. load-time weaving with an agent) — [[Why do you need a Java agent for load-time weaving]].

```d2
direction: right
spring: "Spring AOP\n(proxy around bean)" {
  width: 180
  height: 60
  style.fill: "#e3f2fd"
}
aspectj: "AspectJ\n(bytecode weave)" {
  width: 180
  height: 60
  style.fill: "#fff3e0"
}
call: "External call\nvia proxy/ref" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}
self: "this.method()\ninside target" {
  width: 140
  height: 50
  style.fill: "#fce4ec"
}

call -> spring: "advised"
self -> spring: "not advised"
call -> aspectj: "advised"
self -> aspectj: "advised"
```

**Fig. 1.** Proxy AOP only sees calls that enter through the proxy; AspectJ weaving can advise internal calls too.

> [!warning] Proxy traps stay with Spring AOP
> **Private** / **final** methods and **self-invocation** skip Spring proxies — [[Why does a self-invocation skip Spring AOP advice]], [[Can Spring AOP advise private methods]]. AspectJ weaving can cover those call sites because advice lives in the bytecode, not on a wrapper.

> [!tip] Interview answer
> Spring AOP = runtime proxies, method executions on beans only, simple setup. AspectJ = full weaver, more join points, works on non-Spring objects. @Aspect syntax can look the same; check whether you are proxying or actually weaving.
