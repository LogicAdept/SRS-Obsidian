<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/SelfInvocation #Java/Spring/Framework/AOP #SRS

# When should you use AspectJ mode for `Transactional` self-invocation?

> [!abstract] Short answer
> Switch to **`@EnableTransactionManagement(mode = AdviceMode.ASPECTJ)`** when **`this`-calls must honor `@Transactional`** and refactoring to a second bean or self-injection is impractical. Default **proxy** mode never advises self-invocation. AspectJ **weaves** transaction advice into bytecode — but it requires **`spring-aspects`** and **compile-time or load-time weaving**; prefer extracting another bean for ordinary services.

## Default proxy mode cannot advise `this`

Spring’s `@Transactional` docs: in **proxy** mode (the default), only calls **through the proxy** are intercepted. Self-invocation does not create a transaction at runtime even when the callee is annotated.

That is why interview answers still recommend a **cross-bean** call or injected self-proxy first — [[How do you make an inner Transactional method honor its annotation]] and [[What is the difference between a self-invocation and a cross-bean Transactional call]].

## When AspectJ mode is the right trade-off

Use AspectJ transaction mode when:

* many **same-class** calls must respect `@Transactional` (including propagation like `REQUIRES_NEW`);
* you **cannot** reasonably split beans or inject self-references;
* the team accepts **AspectJ weaving** in the build or at load time.

```java
@Configuration
@EnableTransactionManagement(mode = AdviceMode.ASPECTJ)
public class TransactionConfig {
    // requires spring-aspects + compile-time or load-time weaving
}
```

**Listing 1.** Conceptual: AspectJ mode weaves the transaction aspect into affected classes so **any** method call — including `this.inner()` — can start or join a transaction. Spring’s AOP proxy docs note that compile-time and load-time weaving **do not** have the self-invocation limitation.

```d2
direction: right
proxy: "Proxy mode\nexternal calls only" {
  width: 220
  height: 80
  style.fill: "#ffebee"
}
aspectj: "AspectJ mode\nbytecode weaving\nthis-calls advised" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
cost: "spring-aspects +\nLTW/CTW setup" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}

proxy -> aspectj -> cost
```

**Fig. 1.** AspectJ buys self-invocation advice at weaving infrastructure cost.

## When not to reach for AspectJ

Prefer a **second `@Service` bean** for the inner transactional method in normal application code — clearer boundaries and standard proxy semantics without a weaver.

Do **not** enable AspectJ mode **only** to fix one accidental `this` call — the operational cost (build agents, LTW agents, test setup) usually outweighs a small refactor.

Setting `mode = ASPECTJ` **without** a working weaver and `spring-aspects` on the classpath does **not** magically intercept self-calls.

> [!warning] Weaving is mandatory infrastructure
> AspectJ mode requires **`spring-aspects.jar`** and **compile-time or load-time weaving** configured in the application. Proxy mode works with standard Spring AOP auto-proxying alone.

> [!warning] Whole-class weaving is heavier than one extracted bean
> AspectJ affects build/runtime weaving for affected classes. Fixing a single self-invocation by extracting `AuditService` is usually cheaper than switching the project’s transaction mode.

> [!warning] Other AOP limits may still apply in proxy mode
> Even before AspectJ, **`final`** methods and non-public methods on CGLIB targets have proxy advising constraints. AspectJ mode changes the self-invocation story, not every visibility/final edge case in all setups.

> [!tip] Interview answer
> **Use AspectJ transaction mode when self-invoked methods must honor `@Transactional` and you accept AspectJ weaving with `spring-aspects`.** Default proxy mode skips `this`-calls. In normal code, extract another bean first; AspectJ is the bulk fix when many internal calls must be advised and refactoring is impractical.
