<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Annotations #SRS

# How do you control the order of multiple aspects?

> [!abstract] Short answer
> Put **`@Order`** on the **aspect class** (or implement **`Ordered`**). **Lower** `getOrder()` / annotation value → **higher** precedence. Highest-precedence advice runs **first on the way in** and **last on the way out**. Without an order, relative order of two aspects is **undefined**.

## Aspect-level precedence, not advice-method `@Order`

When two pieces of advice from **different** `@Aspect` beans hit the same join point, Spring follows AspectJ: highest precedence first inbound, last outbound. You set that precedence the usual Spring way: implement `org.springframework.core.Ordered` on the aspect, or annotate the aspect **class** with `@Order`. The lower integer wins.

```java
@Aspect
@Component
@Order(1)
public class AuditAspect { /* @Before / @Around … */ }

@Aspect
@Component
@Order(2)
public class TxAspect { /* … */ }
```

**Listing 1.** `@Order` belongs on the aspect bean type. Default `@Order` value is `Ordered.LOWEST_PRECEDENCE` (`Integer.MAX_VALUE`). Same numeric order → arbitrary relative position.

XML: `order` on `<aop:aspect>` / advisor, or `@Order` / `Ordered` on the backing bean. A worked `Ordered` aspect is Spring’s `ConcurrentOperationExecutor` retry example (order higher than transaction advice so each retry is a fresh transaction). Advice kinds themselves: [[What advice types does Spring AOP support]].

```d2
direction: down
outer: "@Order(1) aspect\nenter first / exit last" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
inner: "@Order(2) aspect\nenter second / exit first" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
target: "join point\n(target method)" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}

outer -> inner -> target
```

**Fig. 1.** Highest-precedence aspect is the **outer** wrapper: first `@Before` / first to enter `@Around.proceed()`, last `@After` after the inner aspect unwinds.

> [!warning] Same `@Aspect`, same advice type — unorderable
> Inside one class, type precedence is `@Around` > `@Before` > `@After` > `@AfterReturning` > `@AfterThrowing`, but `@After` still runs as **finally** (after returning/throwing in that aspect). Two `@Before` methods in the **same** class have **undefined** order (javac drops declaration order). Split them into separate `@Aspect` beans and `@Order` those beans. Do not put `@Order` on the advice method.

> [!warning] Unspecified order is undefined
> Two aspects with no `Ordered` / `@Order` are not promised any sequence. `OrderComparator` treats missing order as `LOWEST_PRECEDENCE`; two such aspects still sort arbitrarily relative to each other. `PriorityOrdered` sorts ahead of plain `Ordered`.

Aspect beans still need auto-proxy enablement: [[How do you enable AOP in a Spring application]]. Module shape: [[What is an Aspect in Spring AOP]].

> [!tip] Interview answer
> **Order aspects with `@Order` or `Ordered` on the aspect class — lower number is higher precedence.** That aspect runs first into the join point and last on the way out. Same-type advice in one `@Aspect` cannot be ordered; split classes.
