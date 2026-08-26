<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# What is an Advisor in Spring AOP?

> [!abstract] Short answer
> An **Advisor** is Spring’s low-level **aspect unit**: **one advice object + a filter** (usually a **pointcut**). **`DefaultPointcutAdvisor`** is the common implementation. `@Aspect` classes are split into advisors internally; you rarely declare `Advisor` beans yourself.

## One advice, one pointcut

Spring *Advisor API*: an Advisor is **an aspect that contains only a single advice** associated with a **pointcut expression**. The `Advisor` interface holds **advice** (action at a join point) and a **filter** for where it applies. Spring AOP is built around **around** advice as AOP Alliance **`MethodInterceptor`s**; the Advisor type also covers before / throws / after-returning advice that is not written as interception.

```java
Advised advised = (Advised) myObject;
advised.addAdvice(new DebugInterceptor()); // wrapped: Pointcut.TRUE
advised.addAdvisor(new DefaultPointcutAdvisor(mySpecialPointcut, myAdvice));
```

**Listing 1.** From *Manipulating Advised Objects*. Bare `addAdvice` becomes a `DefaultPointcutAdvisor` that matches **all** methods. Introductions need a different advisor type — `DefaultPointcutAdvisor` **cannot** hold them.

`@Aspect` style hides this: each advice method becomes an advisor on the auto-proxy chain (`AnnotationAwareAspectJAutoProxyCreator` / `AbstractAdvisorAutoProxyCreator`). XML schema `<aop:advisor>` is the same pair (`pointcut-ref` + `advice-ref`). Advice vs pointcut: [[What is Advice in Spring AOP]], [[What is a Pointcut in Spring AOP]]. Internals: [[How does Spring AOP work internally]].

```d2
direction: right
pc: "Pointcut\n(where)" {
  width: 160
  height: 60
  style.fill: "#e3f2fd"
}
adv: "Advice\n(what)" {
  width: 160
  height: 60
  style.fill: "#fff3e0"
}
ad: "Advisor" {
  width: 140
  height: 60
  style.fill: "#e8f5e9"
}
proxy: "Interceptor chain\non the AOP proxy" {
  width: 200
  height: 70
  style.fill: "#fce4ec"
}

pc -> ad
adv -> ad
ad -> proxy
```

**Fig. 1.** An `@Aspect` with three advice methods is three advisors, not one. Mix interceptor, before, and throws advice on the **same** proxy; Spring builds the chain.

> [!warning] Advisor ≠ `@Aspect` class
> An `@Aspect` bean is a **module** that can hold many pointcuts and advice methods. Each advice is compiled down to **one Advisor**. Interviews that treat them as synonyms lose ordering and “which interceptor ran.”

> [!warning] `Pointcut.TRUE` is easy to add by accident
> `addAdvice(...)` without a pointcut advises **every** method on that proxy. Use `DefaultPointcutAdvisor(pointcut, advice)` when you meant “only these join points.” Frozen proxies (`Advised.isFrozen()`) reject later add/remove (`AopConfigException`). You cannot add/remove **introduction** advisors on an existing proxy.

> [!tip] Interview answer
> **An Advisor is Spring AOP’s pair of one advice plus a pointcut.** `DefaultPointcutAdvisor` is the usual type. `@Aspect` is sugar: auto-proxy turns each advice method into an advisor on the interceptor chain.
