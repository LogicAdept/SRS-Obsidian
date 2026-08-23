<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #Java/Annotations #SRS

# Why is Autowired often omitted on a single constructor in modern Spring?

> [!abstract] Short answer
> When a Spring bean has **only one constructor**, the container **autowires it automatically** — an **`@Autowired` annotation is optional**. Modern style omits it because constructor injection is the default path and the annotation adds noise without changing behavior.

## Single-constructor autowiring rule

The Spring Framework reference states:

> An `@Autowired` annotation on such a constructor is **not necessary** if the target bean defines **only one constructor**.

The constructor-resolution rules go further: if a class declares **only a single constructor**, Spring **always uses it for injection**, **even when it is not annotated**.

That is why Boot’s dependency-injection examples show a **`@Service`** with a lone constructor and **no `@Autowired`**:

```java
@Service
public class MyAccountService implements AccountService {

    private final RiskAssessor riskAssessor;

    public MyAccountService(RiskAssessor riskAssessor) {
        this.riskAssessor = riskAssessor;
    }
}
```

**Listing 1.** Official Boot sample — one constructor, dependencies injected without `@Autowired`.

## When you still need `@Autowired`

The annotation becomes **required for disambiguation** when a class has **multiple constructors**:

- Mark **one** constructor with **`@Autowired`** (default **`required = true`**) so the container knows which to use
- Or mark multiple constructors with **`@Autowired(required = false)`** and let Spring pick the one whose dependencies can be satisfied

```java
@Service
public class MyAccountService implements AccountService {

    private final RiskAssessor riskAssessor;

    @Autowired
    public MyAccountService(RiskAssessor riskAssessor) {
        this.riskAssessor = riskAssessor;
    }

    public MyAccountService(RiskAssessor riskAssessor, PrintStream out) {
        this.riskAssessor = riskAssessor;
    }
}
```

**Listing 2.** Conceptual multi-constructor case — `@Autowired` selects the injection constructor (from Spring Boot reference).

```d2
direction: right
one: "One constructor\n@Autowired optional" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
many: "Multiple constructors\n@Autowired required" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}

one -> many: "add ctor →\nmark choice"
```

**Fig. 1.** Omission is safe only while the bean exposes a unique constructor.

> [!warning] Do not drop `@Autowired` after adding a second constructor
> Introducing another constructor without annotating either one leaves Spring to apply **multi-constructor resolution rules** — which may pick an unexpected ctor or fail startup. Keep exactly **one** obvious injection constructor, or annotate explicitly. See [[Why is constructor injection preferred in Spring]] and [[What does Autowired required false do]].

> [!tip] Interview answer
> Spring autowires the only constructor by default, so @Autowired is redundant on a single-ctor bean — that is why modern code omits it. Add @Autowired when you have multiple constructors and need to tell the container which one to use.
