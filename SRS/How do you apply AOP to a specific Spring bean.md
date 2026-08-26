<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# How do you apply AOP to a specific Spring bean?

> [!abstract] Short answer
> Use Spring’s **`bean(idOrName)`** pointcut designator — **not** standard AspectJ. Combine it with `execution` / `within` as needed. Wildcards work (`bean(*Service)`). It matches **bean names** at the **instance** level. **`bean()` is unavailable in native AspectJ weaving.**

## Spring-only `bean` PCD

Spring *Supported Pointcut Designators*: extra PCD **`bean(idOrNameOfBean)`**. Limited `*` wildcards. Combine with `&&`, `||`, `!` like other designators.

It is a **Spring AOP extension**. It **does not** work in native AspectJ weaving and is **not** available for aspects in the `@Aspect` model **when those aspects are woven by AspectJ** (instance-based matching vs type-based weaving). In **proxy** `@EnableAspectJAutoProxy` mode, `bean(...)` is the way to target one container instance.

```java
@Before("bean(tradeService) && execution(* *(..))")
public void logTradeService(JoinPoint jp) { /* ... */ }

@Before("bean(*Service)")
public void logNamedServices(JoinPoint jp) { /* ... */ }
```

**Listing 1.** Names from Spring’s examples (`bean(tradeService)`, `bean(*Service)`). Also valid: `execution(* com.xyz.service.AccountService.*(..))` if the **type** is unique — that is type-based, not bean-id-based.

Alternatives: `@annotation` on methods of that bean; `this`/`target` with the implementation type. How expressions compose: [[How do you define a pointcut expression in Spring AOP]].

```d2
direction: right
name: "Spring bean id\ntradeService" {
  width: 180
  height: 60
  style.fill: "#e3f2fd"
}
pc: "bean(tradeService)" {
  width: 180
  height: 60
  style.fill: "#fff3e0"
}
adv: "advice on that instance" {
  width: 200
  height: 60
  style.fill: "#e8f5e9"
}

name -> pc -> adv
```

**Fig. 1.** Matching is by factory bean name, not by Java type alone.

> [!warning] Not portable to `ajc` / LTW
> If you compile the same `@Aspect` with the AspectJ weaver, `bean(...)` is not a legal AspectJ PCD. Keep type/`@annotation` cuts for dual-use aspects.

> [!warning] Name is the Spring bean name
> Default for `@Component` `TradeService` is `tradeService`, not the FQN. A `@Bean` method name wins. Wrong id → no match, no error.

> [!tip] Interview answer
> **Spring AOP adds `bean(myService)` to limit advice to that bean name** (`*` wildcards allowed). It is instance-based and proxy-only — not core AspectJ. For type-wide matching use `execution` / `within` instead.
