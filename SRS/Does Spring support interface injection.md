<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/DI #SRS

# Does Spring support interface injection?

> [!abstract] Short answer
> **Not as a dependency-injection mode.** Classic IoC named three styles: constructor injection, setter injection, and **interface injection** (the container calls a method on an interface the component implements). Spring’s reference documents **two major variants**: constructor-based and setter-based DI. Ordinary beans stay POJOs — no injection interface to implement.

## What “interface injection” means

The third classic style is **not** “the dependency type is an interface.” It is: you implement a dedicated injection API (`injectFinder(...)`, Avalon’s `Serviceable.service(ServiceManager)`), and the **container** invokes that method to push collaborators (or a locator) in.

```java
public interface InjectFinder {
    void injectFinder(MovieFinder finder);
}

public class MovieLister implements InjectFinder {
    private MovieFinder finder;

    @Override
    public void injectFinder(MovieFinder finder) {
        this.finder = finder;
    }
}
```

**Listing 1.** Conceptual interface injection: the component must implement a container-facing injection interface. Spring does not wire collaborators this way.

Spring’s constructor and setter examples are the opposite: a POJO with “no dependencies on container specific interfaces, base classes, or annotations.”

```java
public class SimpleMovieLister {

    private final MovieFinder movieFinder;

    public SimpleMovieLister(MovieFinder movieFinder) {
        this.movieFinder = movieFinder;
    }
}
```

**Listing 2.** Conceptual Spring constructor injection. `MovieFinder` may be an **interface type**; that is ordinary typed DI, not interface injection.

```d2
direction: down
classic: "Classic three DI styles" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
ctor: "Constructor\n(Pico, Spring)" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}
setter: "Setter / JavaBean\n(Spring)" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}
iface: "Interface injection\n(Avalon Serviceable)" {
  width: 220
  height: 70
  style.fill: "#ffebee"
}
spring: "Spring ApplicationContext\nctor + setter (major variants)\n+ field / config methods" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}

classic -> ctor
classic -> setter
classic -> iface
ctor -> spring
setter -> spring
```

**Fig. 1.** Spring implements constructor and setter DI. Interface injection is the Avalon-style callback, not “inject an interface.”

The `ApplicationContext` supports constructor-based and setter-based DI and can mix them (constructors for mandatory collaborators, setters or configuration methods for optional ones). Factory-method arguments are treated like constructor arguments. See [[Which dependency injection styles do you know]] and [[Why is constructor injection preferred in Spring]].

## What Spring added beyond the two variants

`@Autowired` / `@Inject` can target **fields** and **arbitrary config methods**, not only constructors and JavaBean setters. Those are still “container pushes a matching bean into a constructor argument, setter, field, or method parameter” — they do not require the bean to implement an injection interface.

> [!warning] “No interface injection” ≠ “cannot inject an interface”
> Wiring `PaymentService` into a constructor whose parameter type is the **interface** is normal Spring DI and is what the docs recommend for testability. Interface injection would be `class OrderService implements InjectPayment { void injectPayment(...) }`.

> [!warning] `*Aware` is not the missing third DI mode
> If a bean implements `ApplicationContextAware`, the container calls `setApplicationContext`. That *looks* like interface injection, but Spring documents it as an **infrastructure callback**: it couples the class to Spring and “does not follow the Inversion of Control style, where collaborators are provided to beans as properties.” Prefer constructor/setter/`@Autowired` of the collaborator (or of `ApplicationContext` itself). Same idea for `BeanFactoryAware`, `BeanNameAware`, and the other `Aware` types — [[What Aware interfaces does Spring invoke during bean initialization]].

> [!warning] The old “only constructor and setter” line is incomplete
> That sentence is right **as Spring’s listed major DI variants**. It is wrong if it pretends field `@Autowired` and multi-arg `@Autowired` methods do not exist. It is also wrong if it confuses interface injection with injecting an interface-typed dependency.

> [!tip] Interview answer
> Spring does not support Avalon-style interface injection, where you implement an inject-Xxx interface and the container calls it. It supports constructor and setter DI as the two major variants, plus field and method injection via `@Autowired`. Injecting a dependency whose type is an interface is ordinary Spring wiring, not interface injection.
