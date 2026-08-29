<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS

# What is FactoryBean and how do you retrieve the factory itself?

> [!abstract] Short answer
> `org.springframework.beans.factory.FactoryBean` is a **pluggability hook** for instantiation: the bean you declare **is** a factory; the object the container normally exposes is whatever `getObject()` returns. `getBean("id")` (and type-matched injection) therefore yield the **product**, not the `FactoryBean`. To obtain the factory instance, prefix the id with `&` (`BeanFactory.FACTORY_BEAN_PREFIX`): `getBean("&id")`. Only beans that **implement** `FactoryBean` behave this way — it is not a hidden wrapper around every bean.

## Three methods, two objects under one id

Use a `FactoryBean` when creation is awkward in XML (or you want a reusable factory type). Spring Framework itself ships **more than 50** implementations (`ProxyFactoryBean`, JNDI/JPA factories, and so on). The interface is:

- `T getObject()` — the instance this factory creates (shared or not).
- `Class<?> getObjectType()` — the product type, or `null` if not known yet.
- `boolean isSingleton()` — `true` if `getObject()` returns a singleton; **default `true`**. `false` means independent instances (prototype-style **products**).

The factory object is still a container-managed bean (dependency injection, lifecycle). `isSingleton()` describes the **product**, not the factory’s own scope. If you set `scope` on the `FactoryBean` **definition**, that scope applies to the **factory bean itself**, not to `getObject()` ([[How does a prototype Spring bean behave when injected into a singleton]]).

```java
Object product = context.getBean("myBean");
FactoryBean<?> factory = context.getBean("&myBean", FactoryBean.class);
```

**Listing 1.** Conceptual. Same id; `&` selects the factory. The constant is `BeanFactory.FACTORY_BEAN_PREFIX` (`"&"`).

```java
public final class ComponentFactoryBean implements FactoryBean<Component> {

    @Override
    public Component getObject() {
        return new Component();
    }

    @Override
    public Class<Component> getObjectType() {
        return Component.class;
    }
}
```

**Listing 2.** Conceptual. Default `isSingleton()` is `true`, so the container treats the product as a singleton unless you override it.

Injection follows the same dereference: a collaborator typed as the **product** receives `getObject()`. Asking for `FactoryBean<Product>` (or using `&id`) is how you wire the factory. Forgetting `&` / requesting the product type is the usual “wrong type” surprise.

```d2
direction: down
id: "Bean id myBean\n(FactoryBean in the definition)" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
product: "getBean(\"myBean\")\n→ getObject() product" {
  width: 260
  height: 60
  style.fill: "#e8f5e9"
}
factory: "getBean(\"&myBean\")\n→ FactoryBean instance" {
  width: 260
  height: 60
  style.fill: "#fff3e0"
}

id -> product
id -> factory
```

**Fig. 1.** One definition, two lookup results. Ordinary beans have no `&` twin.

`FactoryBean` is **opt-in**. A normal `@Bean` / `<bean class="…">` is not backed by a `FactoryBean`. That is a different type from `BeanFactory` (the container API) ([[What is the difference between BeanFactory and FactoryBean]]). Singleton `FactoryBean`s are published like other singletons (including under the container’s singleton lock) ([[Is a singleton Spring bean thread-safe]]).

> [!warning] `getBean("id")` never returns the `FactoryBean`
> The ampersand is required for the factory. Type-based autowiring of the product type does the same dereference as `getBean("id")`. If you meant to configure the factory, inject `FactoryBean<…>` or look up `&id`.

> [!warning] `scope` on the definition is the factory’s scope
> Prototype/request/`isSingleton() == false` are easy to mix up. The definition’s `scope` scopes the `FactoryBean` instance. `isSingleton()` only answers whether **products** are cached as one shared object.

> [!tip] Interview answer
> A FactoryBean is a Spring bean whose job is to create another object; the container exposes getObject() under the bean id. Call getBean with an ampersand prefix — BeanFactory.FACTORY_BEAN_PREFIX — to get the factory itself. isSingleton describes the product, default true, and not every bean has a FactoryBean: only types that implement the interface.
