<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# What is a Pointcut in Spring AOP?

> [!abstract] Short answer
> A **pointcut** is the **predicate** that selects **join points** — in Spring AOP, **method executions** on Spring beans. Advice runs only where that predicate matches. You write it as an **AspectJ expression** on **`@Pointcut`** or inline on an advice annotation.

## Predicate, not the extra behavior

Spring’s AOP chapter: a pointcut **determines join points of interest** and thus **when advice runs**. The extra work itself is **advice** — [[What is Advice in Spring AOP]], [[What is the difference between AOP advice and pointcuts]].

In `@AspectJ` style the declaration has two parts:

1. **Signature** — a `void` method that names the pointcut
2. **Expression** — the `@Pointcut` string (AspectJ language)

```java
@Pointcut("execution(* transfer(..))")
private void anyOldTransfer() {}
```

**Listing 1.** Spring’s example: `anyOldTransfer` is the signature; `execution(* transfer(..))` is the expression.

Spring AOP supports designators including **`execution`** (primary), **`within`**, **`this`**, **`target`**, **`args`**, **`@annotation`**, **`@within`**, **`@target`**, **`@args`**, and Spring-only **`bean(...)`**. How to write those strings: [[How do you define a pointcut expression in Spring AOP]].

```d2
direction: right
pc: "Pointcut\n(predicate)" {
  width: 180
  height: 70
  style.fill: "#e3f2fd"
}
jp: "Join points\n(method executions)" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
adv: "Advice\n(runs if match)" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}

pc -> jp -> adv
```

**Fig. 1.** Pointcut filters join points; advice is the action at matches.

`execution(* com.xyz.service.*.*(..))` matches methods **in** that package, not subpackages (`..*` for nested packages). Combining named cuts: [[How do you combine multiple pointcut expressions]].

> [!warning] Spring does not match every AspectJ join point
> Only **method execution** on **proxied beans**. `call`, `get`, `cflow`, and similar designators throw **`IllegalArgumentException`**. Self-invocation never matches.

> [!warning] `execution` is common, not exclusive
> Interviews that only quote `execution(* …)` miss `within`, `@annotation`, and `bean` — all official Spring PCDs.

> [!tip] Interview answer
> **A pointcut is the match rule for join points — in Spring, method executions on beans.** You express it in AspectJ (`execution`, `within`, `@annotation`, …) on `@Pointcut` or on the advice. Advice runs only at matches; the pointcut itself does no work.
