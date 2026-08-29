<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #SRS

# What happens when you request the same singleton bean twice from `ApplicationContext`?

> [!abstract] Short answer
> You get the **same object** — **reference equality** (`==`), not a second construction. Default scope is **singleton**: one instance **per bean definition per container**, held in the singleton **cache**. The scopes chapter: every request for that **id** (or an alias of it) returns **that cached instance**. The second `getBean` is a **lookup**, not another `createBean`. Eager `ApplicationContext` usually built it at `refresh()` already ([[How do you create a singleton Spring bean at application startup]]). Two **names** of the same Java type are **two** singletons ([[Can you create two singleton beans of the same type in Spring]]).

## Cache hit, not `new`

`ApplicationContext.getBean` is the `BeanFactory` API. For `scope="singleton"` (the default), the factory stores the object after first creation (init callbacks and AOP wrap included). Later `getBean("invoiceService")`, `getBean(InvoiceService.class)` when that type is **unique**, and every injection of that name all see **one** reference.

```java
ApplicationContext ctx = new AnnotationConfigApplicationContext(AppConfig.class);
InvoiceService a = ctx.getBean("invoiceService", InvoiceService.class);
InvoiceService b = ctx.getBean("invoiceService", InvoiceService.class);
boolean same = (a == b); // true
```

**Listing 1.** Same **name**, same container: `a` and `b` are one instance. Do not use `equals` to prove the cache — prove **`==`**.

```d2
Ctx: ApplicationContext
Cache: "singleton cache\ninvoiceService → instance"
G1: "getBean(\"invoiceService\")"
G2: "getBean(\"invoiceService\")"
G1 -> Cache: miss then create (or already at refresh)
G2 -> Cache: hit
```

**Fig. 1.** Second request does not run the constructor again.

Contrast **prototype**: each `getBean` / fresh injection is a **new** instance ([[What are Spring bean scopes]]). Contrast **two `@Bean` methods** returning `InvoiceService`: `getBean(InvoiceService.class)` throws `NoUniqueBeanDefinitionException`; `getBean("jpa")` and `getBean("stub")` are **two** cached objects.

**`FactoryBean`:** `getBean("id")` twice returns the **same** `getObject()` result when that factory is a singleton (`FactoryBean.isSingleton()` default **true**). `getBean("&id")` twice returns the **same** factory bean instance ([[What is the difference between BeanFactory and FactoryBean]]).

Shared mutable fields are still shared Java state ([[Is a singleton Spring bean thread-safe]]). A JDK/CGLIB **proxy** is what is cached: both calls return **that proxy**, not two targets.

> [!warning] Same class, two ids, two instances
> `getBean` **twice** is “same singleton” only for the **same definition** (name/alias) in **this** container. `getBean(Foo.class)` is not “the class’s singleton in the JVM.” A child context can hide a parent bean of the same **local** name. After `close()`, do not keep calling `getBean`.

> [!tip] Interview answer
> Singleton `getBean` twice → **one object** from the per-container cache (`==`). Prototype → two objects. Identity is the **bean name**, not the Java type. The instance is usually already there from `refresh()`, not created on the second call.
