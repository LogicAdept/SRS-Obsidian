<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS

# What is the difference between BeanFactory and FactoryBean?

> [!abstract] Short answer
> `BeanFactory` is the **container**: the root API that holds named definitions and returns bean instances (`getBean`, scopes, parent factories). `ApplicationContext` **extends** it with messages, events, and resources ([[What is the difference between BeanFactory and ApplicationContext]]). `FactoryBean` is a **bean type inside that container** whose job is to **create another object**. `getBean("id")` returns `FactoryBean.getObject()`, not the factory. `BeanFactory.FACTORY_BEAN_PREFIX` (`"&"`) is how the **container** API asks for the `FactoryBean` instance itself. The names look related; they are not aliases.

## Registry vs instantiation plugin

`BeanFactory` is the client view of the IoC container: unique `String` names, prototype vs singleton (and further scopes on a context), dependency injection as **push** configuration rather than objects pulling from the factory. Implementations load XML, Java config, or other sources. Lifecycle (`BeanNameAware` … `InitializingBean` … destroy) is the factory’s job ([[What is a Spring bean]]).

`FactoryBean<T>` is **pluggability into instantiation**. You implement `getObject()`, `getObjectType()`, and optionally `isSingleton()` when creation is awkward as XML. Spring ships **more than 50** implementations (`ProxyFactoryBean`, JNDI/JPA factories, and so on). The factory is itself a managed bean; only types that **implement the interface** get the `&` / `getObject()` split — not every bean ([[What is FactoryBean and how do you retrieve the factory itself]]).

Docs also say **“factory bean”** (lowercase) for a plain bean with `factory-method` / `factory-bean`. That is **not** `FactoryBean`.

```java
BeanFactory factory = applicationContext; // ApplicationContext is a BeanFactory
Object product = factory.getBean("myJndiObject");
FactoryBean<?> fb = factory.getBean("&myJndiObject", FactoryBean.class);
```

**Listing 1.** Conceptual. Same id; `&` selects the `FactoryBean` (`FACTORY_BEAN_PREFIX` / `FACTORY_BEAN_PREFIX_CHAR`).

```d2
direction: down
bf: "BeanFactory\n(container API)" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
def: "Bean definition myJndiObject\nclass implements FactoryBean" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
prod: "getBean(\"id\") → getObject()" {
  width: 240
  height: 45
  style.fill: "#e8f5e9"
}
self: "getBean(\"&id\") → FactoryBean" {
  width: 260
  height: 45
  style.fill: "#fce4ec"
}

bf -> def
def -> prod
def -> self
```

**Fig. 1.** The container (`BeanFactory`) hosts a `FactoryBean`; lookups choose product vs factory.

Writing a custom `FactoryBean` is a supported extension when Java is clearer than a huge XML recipe. It is **not** a general-purpose factory for use outside the container: the `&` dereference and `getObject()` exposure are `BeanFactory` behavior. Prefer `@Bean` methods for most application factories; keep `FactoryBean` when you need that plugin contract (or are using one Spring already provides).

> [!warning] `BeanFactory` ≠ `FactoryBean`
> One is the registry you almost never implement. The other is an optional bean you (or Spring) implement so the registry can publish a **different** runtime type than the definition’s class.

> [!warning] `getBean` never returns the `FactoryBean` by default
> Forgetting `&` is why a lookup “is the product type, not FactoryBean.” Type-based injection follows the same dereference.

> [!tip] Interview answer
> BeanFactory is the IoC container interface — names in, bean instances out. FactoryBean is a special bean that manufactures another object; the container exposes getObject() under the bean id. Use an ampersand prefix on getBean to get the factory itself. ApplicationContext is a BeanFactory; FactoryBean is not.
