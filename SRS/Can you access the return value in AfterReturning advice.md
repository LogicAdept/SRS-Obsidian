<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Annotations #SRS

# Can you access the return value in AfterReturning advice?

> [!abstract] Short answer
> **Yes.** Use **`@AfterReturning`’s `returning` attribute** with the **same name** as an advice parameter. Spring passes the method’s return value into that parameter. You can **read** it, not **replace** it — swapping the caller’s result requires **`@Around`**.

## Bind with `returning`

Spring *After Returning Advice*: the `returning` name **must correspond** to an advice-method parameter. When the join point returns normally, that value is passed in. The clause also **restricts matching** to executions whose return type is compatible with that parameter type (`Object` matches any return).

```java
@AfterReturning(
    pointcut = "execution(* com.xyz.dao.*.*(..))",
    returning = "retVal")
public void doAccessCheck(Object retVal) {
    // inspect retVal — do not try to replace the caller's reference
}
```

**Listing 1.** From Spring Framework reference. Contrast with `@After`, which does not bind a return value — [[What is the difference between After AfterReturning and AfterThrowing advice]].

`@AfterReturning` **does not run** if the method throws. To change what the caller receives, use `@Around` and return from `proceed()` (or a substitute) — [[Why can Around advice lose the join point return value]].

```d2
direction: right
target: "Target method\nreturns value" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
bind: "returning = \"retVal\"" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
adv: "advice(Object retVal)" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}

target -> bind -> adv
```

**Fig. 1.** Binding is name-based: attribute and parameter must match.

> [!warning] Names must match
> `returning = "result"` with a parameter named `retVal` does not bind. Align the strings **exactly**.

> [!warning] You cannot swap the return reference
> Spring: after-returning advice **cannot** return a totally different object to the caller. Cache-or-replace belongs in `@Around`.

> [!warning] Type on the parameter filters join points
> A `String retVal` parameter matches only methods that return `String` (or a subtype), not every `execution(* *(..))` hit.

> [!tip] Interview answer
> **Yes — `@AfterReturning(returning = "retVal")` plus a parameter `Object retVal`.** The names must match. You can log or inspect the value; you cannot change what the caller gets. That takes `@Around`.
