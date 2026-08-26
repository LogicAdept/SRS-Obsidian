<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# How does Spring AOP work internally?

> [!abstract] Short answer
> A **`BeanPostProcessor`** (`AnnotationAwareAspectJAutoProxyCreator`) wraps eligible beans in a **runtime AOP proxy**. Matching **advisors** become an interceptor chain. Clients call the **proxy**; interceptors run; then the **target** method. The target class bytecode is **not** rewritten. `this` calls never re-enter the proxy.

## Auto-proxy, then interceptor chain

`@EnableAspectJAutoProxy` (or `<aop:aspectj-autoproxy/>`) registers **`AnnotationAwareAspectJAutoProxyCreator`**. It is an **`AbstractAutoProxyCreator`**: after the container instantiates a bean, the post-processor decides whether to wrap it. `AnnotationAwareAspectJAutoProxyCreator` collects `@Aspect` beans and Spring `Advisor`s, matches them to the bean, and — if anything applies — replaces the bean with a proxy that **delegates to interceptors before invoking the bean itself**.

Spring models advice as interceptors around the join point (always a **method execution**). Around advice can skip the target by not calling `proceed()`.

```java
ProxyFactory factory = new ProxyFactory(new SimplePojo());
factory.addInterface(Pojo.class);
factory.addAdvice(new RetryAdvice());
Pojo pojo = (Pojo) factory.getProxy();
pojo.foo(); // interceptor chain, then SimplePojo.foo()
```

**Listing 1.** Same runtime object as auto-proxy, built by hand (`Proxying Mechanisms`). The container injects the equivalent of `factory.getProxy()`, not `new SimplePojo()`.

Proxy kind (*Proxying Mechanisms*): **JDK dynamic proxy** if the target implements **at least one interface** (all those interfaces are proxied); **CGLIB subclass** if there is **no** interface. That is the **core Framework** default (`@EnableAspectJAutoProxy(proxyTargetClass=false)`). **Spring Boot** `AopAutoConfiguration` sets **`spring.aop.proxy-target-class=true`** (CGLIB) unless you override it. As of Framework 7.0, `@Proxyable` can override the type per bean.

```d2
direction: down
bpp: "AnnotationAwareAspectJAutoProxyCreator\n(BeanPostProcessor)" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
proxy: "JDK or CGLIB proxy\n+ interceptor chain" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
target: "Target instance\n(unmodified bytecode)" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

bpp -> proxy -> target
```

**Fig. 1.** Weaving is **runtime** (AOP Concepts). Compile-time / load-time weaving is AspectJ, not this path — [[What is weaving in AOP]]. Enablement: [[How do you enable AOP in a Spring application]].

> [!warning] Self-invocation never hits the chain
> After the proxy has entered the target, `this.bar()` is a direct call. Advice on `bar` does not run — [[Why does a self-invocation skip Spring AOP advice]]. AspectJ weaving does not have that hole because it edits bytecode.

> [!warning] “Interface → JDK proxy” is not Boot’s default
> Framework docs start from JDK proxies when an interface exists. Boot often creates **CGLIB** proxies for the same bean. Final/private methods still cannot be advised — [[What are Spring AOP proxy limitations]].

> [!tip] Interview answer
> **Spring AOP is a BeanPostProcessor that wraps beans in a JDK or CGLIB proxy and runs an interceptor chain on each matching method call.** The target class is unchanged. Calls that never enter the proxy — especially `this.foo()` — skip advice.
