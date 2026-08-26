<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Annotations #SRS

# What is the `EnableAspectJAutoProxy` annotation?

> [!abstract] Short answer
> **`@EnableAspectJAutoProxy`** (on `@Configuration`, since Spring 3.1) turns on processing of **`@Aspect` beans** and **auto-proxies** advised components — the Java equivalent of **`<aop:aspectj-autoproxy/>`**. It is **not** full AspectJ weaving: the runtime is still **Spring AOP proxies** that understand `@AspectJ` **annotations**. Needs **`aspectjweaver`** on the classpath.

## What it actually enables

Javadocs: it ensures `@Aspect` beans are processed and matching targets (for example `FooService`) are **proxied** so advice runs. How to switch it on in an app: [[How do you enable AOP in a Spring application]].

```java
@Configuration
@EnableAspectJAutoProxy
public class AppConfig {

    @Bean
    public FooService fooService() {
        return new FooService();
    }

    @Bean
    public MyAspect myAspect() {
        return new MyAspect();
    }
}
```

**Listing 1.** From `EnableAspectJAutoProxy` javadoc — service + `@Aspect` `@Bean` in the same config.

| Attribute | Default (Framework) | Meaning |
| --- | --- | --- |
| **`proxyTargetClass`** | `false` | `true` → **CGLIB subclass** proxies; `false` → **JDK interface** proxies |
| **`exposeProxy`** | `false` | Expose the proxy in a `ThreadLocal` for `AopContext.currentProxy()` |

Spring **Boot** auto-config defaults to **CGLIB** (`spring.aop.proxy-target-class=true`) and can skip this annotation when AspectJ is on the classpath.

```d2
direction: right
ann: "@EnableAspectJAutoProxy" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
aspect: "@Aspect beans" {
  width: 160
  height: 50
  style.fill: "#fff3e0"
}
proxy: "JDK or CGLIB proxy" {
  width: 180
  height: 50
  style.fill: "#e8f5e9"
}

ann -> aspect -> proxy
```

**Fig. 1.** Annotation-style aspects, proxy weaving — not `ajc` / LTW. Contrast [[What is the difference between EnableLoadTimeWeaving and EnableAspectJAutoProxy]].

> [!warning] The name does not mean AspectJ compiler
> “AspectJ” here is the **`@Aspect` annotation style**. Bytecode weaving is `@EnableLoadTimeWeaving` / `ajc`, a different stack.

> [!warning] Local context only
> Redeclare on each `ApplicationContext` that must proxy beans (root vs `DispatcherServlet`).

> [!warning] Framework default is JDK proxies
> `proxyTargetClass=false` by default in Spring Framework. Classes without an interface are not advised unless you set CGLIB (or use Boot’s default).

> [!tip] Interview answer
> **`@EnableAspectJAutoProxy` is `<aop:aspectj-autoproxy/>` in annotation form.** It auto-proxies beans advised by `@Aspect` components. Still Spring proxies, not AspectJ LTW. `proxyTargetClass=true` forces CGLIB; `aspectjweaver` is required.
