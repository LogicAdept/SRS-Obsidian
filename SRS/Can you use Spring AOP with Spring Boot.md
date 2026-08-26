<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# Can you use Spring AOP with Spring Boot?

> [!abstract] Short answer
> **Yes.** Spring Boot **auto-configures** Spring AOP. If **AspectJ is on the classpath** (usual path: **`spring-boot-starter-aop`**), Boot enables `@Aspect` auto-proxy and you typically **do not** add `@EnableAspectJAutoProxy`. You still write **`@Aspect` beans** and advised services as usual.

## Boot auto-config vs Framework enablement

Spring Boot *Aspect-Oriented Programming*: Boot provides AOP auto-configuration. **If AspectJ is on the classpath, AspectJ auto-proxy is enabled so `@EnableAspectJAutoProxy` is not required.**

Default in Boot: **CGLIB** class proxies. Set `spring.aop.proxy-target-class=false` for JDK interface proxies. `AopAutoConfiguration` is the equivalent of enabling `@EnableAspectJAutoProxy`; it stays off if `spring.aop.auto=false`.

Plain Framework setup (annotation/XML + weaver) is still valid inside Boot — [[How do you enable AOP in a Spring application]] — but redundant when the starter (or another dependency that brings AspectJ) is present.

```java
@SpringBootApplication
public class App { /* starter-aop on the classpath */ }

@Aspect
@Component
public class TimingAspect {

    @Around("execution(* com.example.service.*.*(..))")
    public Object time(ProceedingJoinPoint pjp) throws Throwable {
        return pjp.proceed();
    }
}
```

**Listing 1.** Conceptual Boot app: no `@EnableAspectJAutoProxy` on the application class; aspect is a scanned `@Component`.

```d2
direction: down
starter: "spring-boot-starter-aop\n(aspectjweaver on classpath)" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
auto: "AopAutoConfiguration" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
proxy: "CGLIB proxies by default" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}

starter -> auto -> proxy
```

**Fig. 1.** Boot wires Framework auto-proxy; advice is still Spring AOP, not `ajc`. See [[What is the EnableAspectJAutoProxy annotation]].

> [!warning] No AspectJ on the classpath → no `@Aspect` processing
> Without `starter-aop` (or another module that pulls AspectJ), `@Aspect` classes can sit unused. Transactions/cache may still use lower-level Spring AOP via their own auto-config.

> [!warning] Proxy rules are unchanged
> Self-invocation, private methods, and non-beans still skip advice. Boot does not switch you to AspectJ weaving.

> [!tip] Interview answer
> **Yes — Boot auto-configures Spring AOP.** Add `spring-boot-starter-aop`, keep `@Aspect` `@Component` beans, skip manual `@EnableAspectJAutoProxy`. Default proxies are CGLIB. It is still proxy-based Spring AOP.
