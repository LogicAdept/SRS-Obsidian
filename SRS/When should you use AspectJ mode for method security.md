<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Framework/AOP #SRS

# When should you use AspectJ mode for method security?

> [!abstract] Short answer
> Use **`@EnableMethodSecurity(mode = AdviceMode.ASPECTJ)`** when **self-invocation must be authorized**, or when you want Spring Security advice **woven into bytecode** (the docs also mention a possible performance win). Default **`AdviceMode.PROXY`** only intercepts calls **through the Spring proxy**. Prefer extracting a **second bean** (or self-injection) over switching the whole app to AspectJ.

## Proxy mode is the default — and it skips `this`

`@EnableMethodSecurity` defaults to **`mode = AdviceMode.PROXY`**. Advisors sit on the bean proxy. `this.secured()` is a direct call on the target, so `@PreAuthorize` / `@Secured` never run — [[Why does method security skip self-invocation]].

Spring Framework’s proxying guide lists the usual fixes in this order: **avoid self-invocation** (another bean), **inject a self-reference**, last-resort `AopContext.currentProxy()`. Compile-time and load-time weaving **do not** have that hole because advice is in the class bytecode.

## When ASPECTJ mode is the right trade-off

Switch when:

- many **same-class** calls must honor method security;
- splitting beans or self-injection is impractical;
- the team already runs **AspectJ compile-time or load-time weaving**.

The method-security guide: **after setting up AspectJ**, set the mode so Spring Security **publishes its advisors as AspectJ advice** to be woven. XML: `<sec:method-security mode="aspectj"/>`. Namespace docs for AspectJ mode: secured methods must be woven with **`AnnotationSecurityAspect`** from **`spring-security-aspects`**. AspectJ also follows Java: **annotations on interfaces are not inherited** — put security annotations on the **class**.

```java
@Configuration
@EnableMethodSecurity(mode = AdviceMode.ASPECTJ)
public class MethodSecurityConfig {
    // requires AspectJ CTW or LTW; not a proxy-only switch
}
```

**Listing 1.** Conceptual — this does not replace weaving infrastructure. See [[How do you perform load-time weaving with AspectJ in a Spring application]] and [[What is the difference between Spring AOP and AspectJ]].

```d2
direction: right
proxy: "PROXY (default)\nexternal calls only" {
  width: 220
  height: 70
  style.fill: "#ffcdd2"
}
aspectj: "ASPECTJ\nbytecode weaving\nthis-calls advised" {
  width: 240
  height: 80
  style.fill: "#c8e6c9"
}
cost: "CTW/LTW +\nspring-security-aspects" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}

proxy -> aspectj -> cost
```

**Fig. 1.** AspectJ mode buys self-invocation checks at weaving cost. Same idea as [[When should you use AspectJ mode for Transactional self-invocation]].

Do **not** flip the mode to paper over one accidental `this` call. Extract `OrderAuthorizationService` (or inject `@Lazy` self) and keep **proxy** mode.

> [!warning] Mode without a weaver does not intercept
> `mode = ASPECTJ` tells Spring to publish **AspectJ advice**, not Spring AOP interceptors. Without compile-time or load-time weaving actually applying that advice, method security does **not** run on those invocations — including ordinary cross-bean calls. Setting the annotation alone is not a silent upgrade of proxy mode.

> [!tip] Interview answer
> Default method security is Spring AOP proxies, so `this.secured()` skips `@PreAuthorize`. Use `AdviceMode.ASPECTJ` only when you must weave those checks into bytecode and you already have AspectJ set up. For one self-call, extract another bean instead.
