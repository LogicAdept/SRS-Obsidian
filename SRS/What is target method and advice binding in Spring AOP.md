<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# What is target method and advice binding in Spring AOP?

> [!abstract] Short answer
> **Binding** is how Spring copies values from the **advised method execution** into **typed advice parameters**: join-point args (`args(name)`), the **proxy** (`this`), the **target object** (`target`), annotations (`@annotation`, …), and **`returning` / `throwing`**. Names in the pointcut must match names on the advice (or `@Pointcut`) method. The target method itself is not rewritten; the proxy interceptor reads the `MethodInvocation` and passes bound values.

## Two jobs of a binding PCD

Spring *Advice Parameters*: prefer typed parameters over `Object[]`. If you put a **parameter name** (not a type) in `args(...)`, that clause both **restricts matching** and **passes the runtime argument** into the advice.

```java
@Before("execution(* com.xyz.dao.*.*(..)) && args(account,..)")
public void validateAccount(Account account) {
    // first target-method argument, typed
}

@Pointcut("execution(* com.xyz.dao.*.*(..)) && args(account,..)")
private void accountDataAccessOperation(Account account) {}

@Before("accountDataAccessOperation(account)")
public void validateAccountNamed(Account account) { /* ... */ }
```

**Listing 1.** Spring’s DAO example — `args(account,..)` means at least one argument, first is `Account`, and `account` is bound. Same idea: `this(proxyType)`, `target(appType)`, `@annotation(auditable)`.

After advice binds results the same way: `returning="retVal"` / `throwing="ex"` must match an advice parameter name and also **narrow** the join points (return type / exception type).

Any advice may take a first **`JoinPoint`** (`getArgs()`, `getThis()`, `getTarget()`, `getSignature()`). Around **must** take **`ProceedingJoinPoint`** first.

```d2
direction: down
target: "Target method\ntransfer(Account a, int n)" {
  width: 260
  height: 55
  style.fill: "#fff3e0"
}
pc: "args(account,..)\nname match" {
  width: 200
  height: 55
  style.fill: "#e3f2fd"
}
adv: "advice(Account account)" {
  width: 220
  height: 55
  style.fill: "#e8f5e9"
}

target -> pc -> adv
```

**Fig. 1.** Binding is name-based plumbing from the join point into the advice signature. How-to: [[How do you pass parameters to advice methods]]. `getTarget()` vs proxy: [[What is a Target object in Spring AOP]].

## How names are discovered

Binding matches **pointcut tokens** to **Java parameter names**. Discoverers run in order; **first success wins**. If none work, Spring **throws**.

1. `argNames` on the advice / `@Pointcut` annotation (`AspectJAnnotationParameterNameDiscoverer`)
2. Kotlin reflection, if present
3. Standard reflection — compile with **`javac -parameters`** (recommended)
4. Deduce from the pointcut / `returning` / `throwing` (`AspectJAdviceParameterNameDiscoverer`)

`ajc`-compiled aspects keep names without `argNames`. `JoinPoint` / `ProceedingJoinPoint` as the **first** parameter can be omitted from `argNames`.

> [!warning] Names, not just types
> `args(account)` with a parameter named `acc` does not bind. `args(Account)` (type) **matches only**; `args(account)` (name) **matches and binds**. Generic `Collection<MyType>` cannot be used as that type filter — use `Collection<?>` and check elements yourself.

> [!tip] Interview answer
> Binding wires the target method’s arguments (or `this` / `target` / annotations / return / exception) into typed advice parameters by **name**. `args(param)` both filters and injects. Compile with `-parameters` or set `argNames`, or take `JoinPoint` and call `getArgs()`.
