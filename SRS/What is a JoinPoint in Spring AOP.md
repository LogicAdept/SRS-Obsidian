<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# What is a JoinPoint in Spring AOP?

> [!abstract] Short answer
> A **join point** is a **point during program execution** where advice *could* run. In **Spring AOP it is always a method execution** (on a Spring bean, via a proxy). A **pointcut** is the predicate that **selects** some of those executions. Full AspectJ can also use constructors, field get/set, and other kinds.

## Place in execution vs the match rule

Spring *AOP Concepts*: a join point is “a point during the execution of a program, such as the execution of a method or the handling of an exception.” Then: **“In Spring AOP, a join point always represents a method execution.”**

That is narrower than AspectJ. Spring’s proxy AOP does not intercept field access or constructor execution unless you switch to AspectJ weaving.

| Term | Role |
| --- | --- |
| **Join point** | A candidate site (in Spring: one method execution) |
| **Pointcut** | Predicate matching a set of join points — [[What is a Pointcut in Spring AOP]] |
| **Advice** | Action at matched join points — [[What is Advice in Spring AOP]] |

The `org.aspectj.lang.JoinPoint` **API** (signature, args, target) is the reflective view of the current site — [[What is the purpose of the JoinPoint interface in Spring AOP]]. Around advice uses the subtype **`ProceedingJoinPoint`**.

```d2
direction: right
all: "All method executions\non Spring beans" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
pc: "Pointcut\n(matches some)" {
  width: 180
  height: 70
  style.fill: "#fff3e0"
}
jp: "Selected join points" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}

all -> pc -> jp
```

**Fig. 1.** Join points exist whether or not you advise them; the pointcut filters which ones get advice.

> [!warning] Do not call the pointcut a join point
> Interview mix-up: the **site** is the join point; the **expression** (`execution(* …)`) is the pointcut.

> [!warning] “Exception handling” join points are not Spring AOP
> The generic definition mentions exception handling; **Spring still only weaves method execution**. `@AfterThrowing` runs when that **method** exits by throwing, not as a separate handler join point.

> [!tip] Interview answer
> **A join point is where advice can attach.** In Spring AOP that is **always method execution** on a proxied bean. The pointcut chooses which executions; AspectJ can advise more kinds of join points if you weave with AspectJ.
