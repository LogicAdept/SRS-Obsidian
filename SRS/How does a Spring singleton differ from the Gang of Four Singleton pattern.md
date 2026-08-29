<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #Patterns/GoF/Creational #SRS

# How does a Spring singleton differ from the Gang of Four Singleton pattern?

> [!abstract] Short answer
> GoF Singleton **hard-codes** “one instance of this **class**” (typically per **ClassLoader**) and a **global** access point on the type. Spring `singleton` is a **bean-definition scope**: **one instance per bean definition per IoC container**, kept in the container’s singleton cache and returned for that **name**. Same class, two definitions or two containers → two objects. Default scope is still `singleton`.

## Class-level uniqueness versus a recipe

A bean definition is a **recipe**. Scope is chosen in configuration (`scope="singleton"` is the default; writing it is redundant), not baked into the Java class. That is the opposite of GoF Singleton, whose intent is: ensure a class has **only one instance** and provide a **global point of access** — the class itself intercepts creation.

```d2
direction: right
gof: "GoF Singleton\n1 instance / class\n(per ClassLoader)\nglobal getInstance()" {
  width: 240
  height: 110
  style.fill: "#fff3e0"
}
spring: "Spring singleton\n1 instance / definition\n/ container\ncache by bean name" {
  width: 240
  height: 110
  style.fill: "#e3f2fd"
}
```

**Fig. 1.** Spring singleton is **per-container and per-bean**, not per-class.

```xml
<bean id="accountService" class="com.something.DefaultAccountService"/>
<!-- equivalent; singleton is already the default -->
<bean id="accountService" class="com.something.DefaultAccountService" scope="singleton"/>
```

**Listing 1.** Conceptual XML (two alternative definitions, not two beans in one file). The cache is keyed by the bean **id** (and aliases), not by `Class`.

Consequences that follow from **per-bean** and **per-container**:

- Two singleton definitions of `DefaultAccountService` (`billingService` and `auditService`) are **two** instances. That is legal and common ([[Can you create two singleton beans of the same type in Spring]]).
- Two `ApplicationContext`s each keep their own singleton cache. The same bean name defined in two containers is two objects.
- `getBean("accountService")` twice returns the **cached** instance ([[What happens when you request the same singleton bean twice from ApplicationContext]]).
- Web `application` scope is a different knob: one object per `ServletContext`, not per `ApplicationContext` (a WAR can have several contexts).

The type need not hide constructors or expose `getInstance()`. Clients receive the object by **injection** or `getBean`, through `SingletonBeanRegistry` / the factory — not through a static on the class. See [[How would you explain the Singleton design pattern]] for the GoF shape.

As a rule, use `singleton` for **stateless** beans and `prototype` for **stateful** ones. Sharing one instance does **not** make mutable fields thread-safe ([[Is a singleton Spring bean thread-safe]]).

> [!warning] “Spring beans are GoF singletons” is the trap
> Interviewers want **per-container, per-definition**, not per-`ClassLoader`. The container only guarantees uniqueness **inside that factory’s cache for that name**.

> [!warning] Default singleton is not “one per JVM”
> Nested contexts, multiple WARs, and two `@Bean` methods of the same type all produce extra instances. `scope="singleton"` does not install a ClassLoader-wide lock.

> [!tip] Interview answer
> GoF Singleton is one instance of a class, usually per ClassLoader, with a global accessor on the type. Spring singleton is one instance per bean definition per container, which is the default. Two definitions or two containers mean two objects. It is a scope, not the pattern, and it is not automatically thread-safe.
