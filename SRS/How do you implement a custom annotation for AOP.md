<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Annotations #SRS

# How do you implement a custom annotation for AOP?

> [!abstract] Short answer
> Declare a **method** annotation with **`@Retention(RUNTIME)`**, put it on **Spring bean** methods, and match with **`@annotation(...)`**. Bind the annotation instance in advice if you need attributes. Matching still goes through the **AOP proxy** — self-calls and non-intercepted signatures are skipped.

## Marker (or valued) annotation plus `@annotation`

Spring’s `@Auditable` example is the pattern: a runtime method annotation, then a pointcut that names it.

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Auditable {
    AuditCode value();
}

@Aspect
@Component
public class AuditAspect {

    @Before("execution(public * *(..)) && @annotation(auditable)")
    public void audit(Auditable auditable) {
        AuditCode code = auditable.value();
        // ...
    }
}
```

**Listing 1.** Spring *Declaring Advice* binding form: `@annotation(auditable)` matches the advice parameter name and passes the annotation instance. Type form (no bind) uses the FQN: `@annotation(com.xyz.Auditable)`.

JLS: if you omit `@Retention`, the compiler treats the annotation as **`CLASS`** — present in the class file, **not** retained for reflective reads. Spring AOP matching is runtime/proxy-based, so **`RUNTIME`** is required. `SOURCE` is discarded at compile time.

| PCD | What must carry the annotation |
| --- | --- |
| **`@annotation`** | The **method** being executed |
| **`@within`** | The **declaring type** |
| **`@target`** | The **class of the executing object** (target) |

Combine with a kinded/scoping cut (`execution`, `within`) rather than `@annotation` alone. Expressions: [[How do you define a pointcut expression in Spring AOP]]. Binding names: [[How do you pass parameters to advice methods]].

```d2
direction: right
ann: "@Auditable on\nbean method" {
  width: 180
  height: 70
  style.fill: "#e3f2fd"
}
pc: "@annotation(auditable)" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
adv: "advice reads\nauditable.value()" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}

ann -> pc -> adv
```

**Fig. 1.** The annotation is only a marker (plus attributes). The `@Aspect` bean still needs auto-proxy enablement, and the call must enter the proxy.

> [!warning] `CLASS` retention looks “compiled in” and still misses
> Default retention is **`CLASS`**, not `RUNTIME`. The pointcut string can be valid and still match **nothing** because `getAnnotation` cannot see it.

> [!warning] Annotation does not bypass the proxy
> `@annotation` does not advise `this.foo()` inside the target, private methods, or JDK-proxy methods that are not on the interface. The annotated method must be invoked **through the Spring proxy** — [[Why does a self-invocation skip Spring AOP advice]].

> [!tip] Interview answer
> **Write a `RUNTIME` method annotation, put it on bean methods, and cut with `@annotation` — bind the annotation parameter if you need attributes.** It still only runs when the call hits the Spring AOP proxy. Class-level annotations use `@within` / `@target`, not `@annotation`.
