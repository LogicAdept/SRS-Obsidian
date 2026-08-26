<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# Can you use Spring AOP with beans not managed by Spring?

> [!abstract] Short answer
> **`@Aspect` auto-proxying only wraps Spring beans.** `new Foo()` is never advised that way. You **can** still apply Spring AOP to a plain object with **`ProxyFactory`** (programmatic proxy, no IoC required). For `new` domain instances everywhere, **AspectJ compile- or load-time weaving** is the usual alternative.

## Auto-proxy vs programmatic proxy

`@EnableAspectJAutoProxy` / `<aop:aspectj-autoproxy/>` inspect **beans in the application context**. Objects you construct yourself never enter that pipeline — same idea as missing `@Component` on an `@Aspect` class.

Spring *Creating AOP Proxies Programmatically with the ProxyFactory*: you can use Spring AOP **without depending on Spring IoC**. Wrap any target, add advice/advisors, call `getProxy()`. Callers must use **that** proxy reference.

```java
ProxyFactory factory = new ProxyFactory(myBusinessInterfaceImpl);
factory.addAdvice(myMethodInterceptor);
factory.addAdvisor(myAdvisor);
MyBusinessInterface tb = (MyBusinessInterface) factory.getProxy();
```

**Listing 1.** From Spring Framework reference. Best practice is still to let the container create proxies. See [[What is an AOP proxy in Spring]].

Domain objects created with `new` (entities, DTOs) typically need **AspectJ weaving** (`@Configurable`, LTW) rather than a hand-built `ProxyFactory` per instance — [[What is the difference between Spring AOP and AspectJ]], [[What is the Configurable annotation in Spring]].

```d2
direction: down
ioc: "IoC @Aspect auto-proxy\nSpring beans only" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
pf: "ProxyFactory\nany object you wrap" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
aj: "AspectJ weaving\nnew instances in bytecode" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

ioc -> pf
pf -> aj
```

**Fig. 1.** Three ways to get advice; only the first is “put `@Aspect` in the context.”

> [!warning] `new Service()` inside a bean skips auto-proxy
> Even a `@Service` class is unadvised if you instantiate it yourself instead of injecting the bean.

> [!warning] Programmatic proxy still has proxy semantics
> `this` calls on the wrapped target skip advice. You must call through the object `getProxy()` returned.

> [!tip] Interview answer
> **Declarative Spring AOP (`@Aspect`) is for container beans.** `new` objects are not auto-proxied. You can wrap a non-bean with `ProxyFactory`, or weave with AspectJ so even `new` instances are advised. Prefer IoC for application services.
