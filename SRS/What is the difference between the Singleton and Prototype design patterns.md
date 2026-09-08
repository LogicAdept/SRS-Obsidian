<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Creational #Java/Spring #SRS

# What is the difference between the Singleton and Prototype design patterns?

> [!abstract] Short answer
> **GoF Singleton** hard-codes “**one instance of this class per ClassLoader**” in the type (`private` constructor / `getInstance`). **Spring `singleton` scope** is **one instance per bean definition per IoC container** — two `@Bean` methods of the same class are **two** cached objects. **Spring `prototype` scope** is a **new instance on every `getBean` / fresh injection** from the same recipe; the container **does not** implement GoF Prototype-by-`clone()`. Use singleton for **stateless** services, prototype for **stateful** objects that must not be shared.

## One instance vs many from a recipe

Spring’s scopes chapter: a bean definition is a **recipe**. **Singleton** (default): create once, cache, return the same object for that **id**. **Prototype**: every request for that id runs the recipe again (`new`-like). Scope is **configuration** (`scope="prototype"`, `@Scope("prototype")`), not a field on the class ([[How does a Spring singleton differ from the Gang of Four Singleton pattern]], [[What are Spring bean scopes]], [[When would you use prototype scope in Spring]]).

GoF Singleton (as Spring cites it) is **per ClassLoader**, baked into the Java type. You cannot have two “accountService” identities of that class without another loader or a broken singleton. Spring lets you register **`jpaAccountService`** and **`stubAccountService`** as two singletons of `DefaultAccountService`.

Spring **prototype** is **not** “call `clone()` on a prototypical instance.” The container **instantiates, injects, runs init**, then **forgets** the object: **no `@PreDestroy`**. Client cleans up. Injecting a prototype into a singleton **once** at constructor time gives that singleton **one** prototype forever — later `getBean` is required (or lookup method injection).

```xml
<bean id="accountService" class="com.example.DefaultAccountService"/>
<bean id="protoService" class="com.example.DefaultAccountService" scope="prototype"/>
```

**Listing 1.** Same class; left is one cached instance per container, right is a new instance per lookup.

```d2
direction: down
gof: "GoF Singleton\none per ClassLoader" {
  width: 220
  height: 50
  style.fill: "#fce4ec"
}
ss: "Spring singleton\nper container, per bean id" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
sp: "Spring prototype\nnew instance per getBean" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
recipe: "BeanDefinition recipe" {
  width: 200
  height: 40
  style.fill: "#fff3e0"
}
recipe -> ss
recipe -> sp
```

**Fig. 1.** GoF locks the **class**. Spring locks (or not) the **bean id**.

> [!warning] Prototype into singleton is still one object
> Constructor injection of a prototype collaborator is resolved **once**. The singleton keeps that instance. You do not get a new prototype per method call unless you look it up again.

> [!warning] Prototype has no container destroy
> `@PreDestroy` / `DisposableBean` **do not** run for prototypes. Holding a connection or a thread in a prototype leaks unless **you** close it.

> [!tip] Interview answer
> GoF Singleton is “this class has one instance.” Spring singleton is “this bean id has one instance in this context.” Prototype in Spring means a new object from the same definition on each request, not Cloneable. Default is singleton; pick prototype only when sharing state would be wrong.
