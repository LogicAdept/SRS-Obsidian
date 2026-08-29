<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS

# What is the difference between a Spring bean id and a bean alias?

> [!abstract] Short answer
> Every bean has **one or more identifiers**, unique in that container. The usual one is the **id** (XML `id`, `@Bean` method name, `@Component` value / decapitalized class name). **Aliases** are **extra names for the same definition and the same instance** — not a second bean. In XML, extra names go on `name` (comma, semicolon, or whitespace) and/or a later `<alias name="…" alias="…"/>`. `getBean` and `ref` accept **any** of those names. `@Bean({"dataSource", "subsystemA-dataSource"})` is the Java equivalent: one factory method, several names.

## One recipe, several lookup keys

XML: `id` is **at most one** identifier. Put further names on `name`. You may omit `id` and use only `name`, or omit both and let the container generate a unique name (typical for inner beans you never `ref` ([[What is a Spring inner bean]])). Uniqueness of `id` is enforced by the **container**, not by the XML parser.

Dump wording that “the first token of `name` becomes the id” is **wrong**. `id` and each `name` token are **equivalent aliases** for the same bean — useful when each subsystem wants its own name for a shared collaborator ([[What is a Spring bean]]).

```xml
<bean id="myApp-dataSource" class="example.AppDataSource"
      name="subsystemA-dataSource, subsystemB-dataSource"/>
```

**Listing 1.** Conceptual. One definition; three identifiers.

To alias a bean **defined elsewhere** (split XML):

```xml
<alias name="myApp-dataSource" alias="subsystemA-dataSource"/>
```

**Listing 2.** Conceptual. `fromName` remains valid; `toName` now resolves to the same object.

```java
@Bean({"dataSource", "subsystemA-dataSource", "subsystemB-dataSource"})
DataSource dataSource() {
    return new AppDataSource();
}
```

**Listing 3.** Conceptual. `@Bean("myThing")` equals `@Bean(name = "myThing")`. Default without `name` is the method name (Spring Framework 7.0 can swap that via `ConfigurationBeanNameGenerator`).

Convention: camelCase like a Java field (`accountService`). Component scan uses `@Component("explicit")` or `Introspector.decapitalize` on the simple class name.

XML `autowire="byName"` matches the **property name** to a bean **id or alias**, not to the Java type name ([[What XML autowiring modes exist in Spring]]). Two **definitions** that reuse the same identifier are **bean overriding**, not aliasing (overriding is discouraged and slated for deprecation; `allowBeanDefinitionOverriding=false` throws).

```d2
direction: down
def: "One BeanDefinition\n(one instance for a singleton)" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
id: "id / primary name" {
  width: 180
  height: 45
  style.fill: "#e8f5e9"
}
a1: "alias A" {
  width: 120
  height: 40
  style.fill: "#fff3e0"
}
a2: "alias B" {
  width: 120
  height: 40
  style.fill: "#fff3e0"
}

id -> def
a1 -> def
a2 -> def
```

**Fig. 1.** Aliases are extra keys in the factory map, not extra objects.

> [!warning] An alias is not another singleton
> `getBean("id")` and `getBean("alias")` return the **same** managed instance (for a singleton). Do not register a second `<bean id="alias">` expecting an alias — that is a **second definition** / override.

> [!warning] Inner-bean `id` is not a public name
> A nested `<bean id="…">` does not become a container lookup key. Aliasing that inner id from the outside will not share it.

> [!tip] Interview answer
> The id is the bean’s main name in the container. Aliases are extra names for that same definition so other modules can ref it under their own name. XML name or alias, or @Bean’s name array, never create a second instance. byName autowire matches the property name to those identifiers, not to the class name.
