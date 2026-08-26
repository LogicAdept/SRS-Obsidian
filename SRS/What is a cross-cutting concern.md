<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# What is a cross-cutting concern?

> [!abstract] Short answer
> A **cross-cutting concern** is behavior that **spans many types and objects** and is **not** owned by one domain class — Spring’s textbook example is **transaction management**. **AOP** is one way to **modularize** it as an **aspect**. The concern is the *problem*; AOP is an *approach*. Filters, interceptors, and copy-paste are other approaches.

## Cuts across the type tree

Spring AOP overview: OOP’s unit of modularity is the **class**; AOP’s is the **aspect**. Aspects modularize concerns (such as transactions) that **cut across multiple types and objects**. Those concerns are called **crosscutting** in AOP literature.

Pointcuts matter because they target join points **independently of the OO hierarchy** — e.g. around advice for transactions on **all service-layer business methods**, not one superclass. Spring uses that for **declarative enterprise services** (especially `@Transactional`) and for **custom aspects** you write.

Typical examples in a Spring app (same shape, different modules):

| Concern | Often implemented as |
| --- | --- |
| Transactions | `@Transactional` (Spring AOP proxy) |
| Security | Servlet **filter chain** + optional method-security AOP |
| Logging / timing / audit | Custom `@Aspect` |
| Caching | `@Cacheable` (AOP interceptor) |

```d2
direction: down
concern: "Cross-cutting concern\n(tx, security, logging)" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
oop: "Would scatter into\nmany domain classes" {
  width: 260
  height: 60
  style.fill: "#ffebee"
}
aop: "Aspect + pointcut\n(or filter / interceptor)" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

concern -> oop
concern -> aop
```

**Fig. 1.** The concern exists whether or not you use AOP. What to extract: [[Which parts of a system would you move into aspects]]. Security specifically: [[Is security a cross-cutting concern]]. AOP vocabulary: [[What is aspect oriented programming AOP]].

Spring AOP still only advises **method executions on Spring beans** (proxies). A concern that must run on `this.foo()`, constructors, or non-beans needs AspectJ weaving or a different layer (servlet filter).

> [!warning] Not a synonym for “aspect”
> “Logging is a cross-cutting concern” does not mean “logging is an `@Aspect`.” You can still log inside methods. AOP is justified when the same technical behavior would otherwise be **copied** across types.

> [!warning] Not everything cross-cutting belongs in Spring AOP
> HTTP auth, CORS, and gzip sit in the **servlet filter** chain, not in a service `@Around`. Putting web concerns in method aspects misses requests that never hit that bean.

> [!tip] Interview answer
> **A cross-cutting concern is shared technical behavior that cuts across many classes — transactions are the Spring example.** AOP extracts it into an aspect with pointcuts so domain types stay focused. AOP is how you modularize it, not the concern itself.
