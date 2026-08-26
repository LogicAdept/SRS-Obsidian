<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# How do you pass parameters to advice methods?

> [!abstract] Short answer
> Use **typed advice parameters** plus **binding** in the pointcut: **`args(name)`**, **`this`**, **`target`**, **`@annotation`**, and the same idea for **`returning` / `throwing`**. The **token in the expression must match the Java parameter name**. You can also take a first **`JoinPoint`** (or **`ProceedingJoinPoint`** for `@Around`) for reflective access.

## Binding form of `args` (and friends)

Spring *Advice Parameters*: prefer typed parameters over `Object[]`. If you put a **parameter name** in `args(...)` instead of a type, Spring both **restricts matching** and **passes that argument** into the advice.

```java
@Before("execution(* com.xyz.dao.*.*(..)) && args(account,..)")
public void validateAccount(Account account) {
    // account is the first runtime argument, typed as Account
}

@Pointcut("execution(* com.xyz.dao.*.*(..)) && args(account,..)")
private void accountDataAccessOperation(Account account) {}

@Before("accountDataAccessOperation(account)")
public void validateAccountNamed(Account account) { /* ... */ }
```

**Listing 1.** Spring’s DAO example — `args(account,..)` means “at least one arg, first is `Account`,” and binds it. Bind annotations the same way: `@annotation(auditable)` with an `Auditable auditable` parameter.

Also bind:

* **`this(proxyType)` / `target(appType)`** — proxy vs advised object
* **`returning` / `throwing`** on after advice — [[Can you access the return value in AfterReturning advice]]
* **`JoinPoint` first** — `getArgs()`, `getThis()`, `getTarget()` — [[What is the purpose of the JoinPoint interface in Spring AOP]]

```d2
direction: right
pc: "args(account,..)" {
  width: 200
  height: 60
  style.fill: "#e3f2fd"
}
match: "restricts join points" {
  width: 200
  height: 60
  style.fill: "#fff3e0"
}
bind: "advice(Account account)" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}

pc -> match
pc -> bind
```

**Fig. 1.** One `args` clause both filters and injects. Name matching: [[What is target method and advice binding in Spring AOP]].

> [!warning] Names must match, not just types
> Binding uses **parameter names** discovered from bytecode / `-parameters` / explicit `argNames`. `args(account)` with a parameter called `acc` fails (exception if names cannot be determined).

> [!warning] `args(Account)` vs `args(account)`
> A **type** in `args` only matches; a **name** matches **and** binds. Mixing them up is a common interview slip.

> [!warning] Generic collections do not bind element type
> `args(param)` with `Collection<MyType>` is not supported as a type filter; use `Collection<?>` and check elements yourself.

> [!tip] Interview answer
> **Bind with `args(paramName)` (or `this` / `target` / `@annotation`) so the names line up with the advice method.** That both narrows the pointcut and passes a typed value. `JoinPoint` is the untyped fallback; Around still needs `ProceedingJoinPoint` first.
