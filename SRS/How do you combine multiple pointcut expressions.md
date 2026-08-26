<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# How do you combine multiple pointcut expressions?

> [!abstract] Short answer
> Combine AspectJ fragments with **`&&`**, **`||`**, and **`!`**, or **name** them on `@Pointcut` methods and refer to those names. Spring’s recommended style is **small named cuts** composed into a larger one. Java visibility applies to which names you can see; it does not change matching.

## Operators and named composition

Spring *Combining Pointcut Expressions*: you can mix designators in one string and **refer to other pointcuts by name**.

```java
package com.xyz;

public class Pointcuts {

    @Pointcut("execution(public * *(..))")
    public void publicMethod() {}

    @Pointcut("within(com.xyz.trading..*)")
    public void inTrading() {}

    @Pointcut("publicMethod() && inTrading()")
    public void tradingOperation() {}
}
```

**Listing 1.** From Spring Framework reference — `tradingOperation` is public methods in the trading package tree. Advice then uses `@Before("com.xyz.Pointcuts.tradingOperation()")` (or a local name in the same class).

Share cuts across aspects in a dedicated class (`CommonPointcuts`) and reference `fully.qualified.Class.method()`. How individual `execution` / `within` strings work: [[How do you define a pointcut expression in Spring AOP]]. Excluding one method is `&& !…` — [[How would you exclude a method from being advised]].

```d2
direction: right
a: "publicMethod()\nexecution(public * *(..))" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
b: "inTrading()\nwithin(com.xyz.trading..*)" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
c: "tradingOperation()\n&& composition" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

a -> c
b -> c
```

**Fig. 1.** Named pointcuts are predicates; `&&` is intersection of join-point sets.

> [!warning] Do not rely on mixed `&&` / `||` without grouping
> Spring shows **named** composition rather than a long inline mix. If you inline both `||` and `&&`, use **parentheses**. Named cuts avoid that ambiguity.

> [!warning] Name lookup is Java visibility, matching is not
> `private` `@Pointcut` methods are visible only in the same type. A `public` cut in another class needs the **FQN**. Visibility never turns matching on or off.

> [!tip] Interview answer
> **Combine with `&&`, `||`, and `!`, preferably via named `@Pointcut` methods.** Spring’s example is `publicMethod() && inTrading()`. Reuse a shared `CommonPointcuts` class by fully qualified method name. Use `!` to subtract join points rather than writing one giant expression.
