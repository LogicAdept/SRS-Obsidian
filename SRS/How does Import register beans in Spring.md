<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Annotations #SRS

# How does `@Import` register beans in Spring?

> [!abstract] Short answer
> Put `@Import` on a configuration class and name the types to pull in. The parser loads `@Bean` definitions from imported `@Configuration` classes, registers regular component classes as beans (since **4.2**), and can run `ImportSelector`, `ImportBeanDefinitionRegistrar`, or (Framework **7.0**) `BeanRegistrar`. That is explicit class-by-class registration, not a package scan. `@ImportResource` is the XML counterpart.

## What `@Import` accepts

`@Import` is the Java equivalent of XML `<import/>`. You typically place it on a `@Configuration` class (or as a meta-annotation; since **7.0**, also on interfaces that a `@Configuration` class implements). You then bootstrap **one** entry class; imported types do not need to be listed again on `AnnotationConfigApplicationContext`.

The `value` array may contain:

- Other `@Configuration` classes — their `@Bean` methods become definitions in the **same** container. Cross-config injection uses `@Bean` method parameters (preferred) or `@Autowired` on the config class.
- Regular component classes — same idea as `AnnotationConfigApplicationContext.register(Class…)`. Useful when you want a few entry configs and **no** [[What is the Spring ComponentScan annotation]].
- `ImportSelector` — `selectImports` returns class names to import (optionally deferred via `DeferredImportSelector`).
- `ImportBeanDefinitionRegistrar` — `registerBeanDefinitions` writes into the `BeanDefinitionRegistry` (bean-definition level, not `@Bean` instance level). Registrars must not register `BeanDefinitionRegistryPostProcessor` types here.
- `BeanRegistrar` — Framework **7.0** programmatic registration, still triggered through `@Import`.

Class-level `@Import` is processed **after** `@Import` meta-annotations (and after interface-level `@Import` in 7.0), so a local list can override beans those meta-imports registered.

```java
@Configuration
public class ConfigA {
    @Bean
    public A a() {
        return new A();
    }
}

@Configuration
@Import(ConfigA.class)
public class ConfigB {
    @Bean
    public B b() {
        return new B();
    }
}

// ctx = new AnnotationConfigApplicationContext(ConfigB.class)
// both A and B are in the container
```

**Listing 1.** Conceptual. Only `ConfigB` is supplied to the context; `@Import` pulls in `ConfigA` and its `@Bean` methods ([[What is the Spring Bean annotation]]).

```java
@Configuration
@Import({Dog.class, Cat.class, MySelector.class, MyRegistrar.class})
public class AppConfig {
}
```

**Listing 2.** Conceptual. Since 4.2, `Dog` and `Cat` need not be `@Configuration`; selectors and registrars are further `@Import` targets.

```d2
direction: down
entry: "@Configuration\n@Import({...})" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
parser: "Configuration class parser" {
  width: 240
  height: 55
  style.fill: "#fff3e0"
}
cfg: "Imported @Configuration\n@Bean methods" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
comp: "Component classes\n(register, 4.2+)" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
sel: "ImportSelector\nclass names" {
  width: 200
  height: 70
  style.fill: "#fce4ec"
}
reg: "ImportBeanDefinitionRegistrar\n/ BeanRegistrar" {
  width: 260
  height: 70
  style.fill: "#fce4ec"
}

entry -> parser
parser -> cfg
parser -> comp
parser -> sel
parser -> reg
```

**Fig. 1.** `@Import` is processed while configuration classes are parsed. Selectors feed more types back into the same pipeline; registrars write definitions directly.

Imported `@Configuration` classes are themselves beans. Prefer parameter injection of collaborators over `@Autowired` fields on the config type: configuration is processed early, and a `@PostConstruct` on the same class that calls a local `@Bean` method is a circular reference.

`@ImportResource` loads XML (or other non-`@Configuration` resources) when Java config is primary. The other direction is XML-centric: declare the `@Configuration` class as a `<bean/>` with `annotation-config`, or pick it up with component scanning.

If a `@Configuration` class is `@Conditional`, **all** of its `@Bean` methods, `@Import` annotations, and `@ComponentScan` annotations are subject to those conditions ([[What is the Conditional annotation in Spring]]). A `ConfigurationCondition` can run at `PARSE_CONFIGURATION` (if it fails, the configuration class is **not** added) or at `REGISTER_BEAN` (the class is still parsed; the condition does **not** block adding `@Configuration` classes). Nested `@Configuration` types inherit the enclosing class’s `@Conditional` only when reached by parser recursion or `@Import` — **not** when found independently via `@ComponentScan` or direct registration.

> [!warning] Explicit types, not a package
> `@Import(Dog.class)` registers that class. It does not scan `Dog`’s package. A sibling you forgot to name never becomes a bean. That is the point of using `@Import` as an alternative to [[How do ComponentScan include and exclude filters work]].

> [!warning] The importer’s `@Conditional` gates `@Import`
> A failing type-level condition on the importing `@Configuration` class can skip its `@Import` (and `@ComponentScan`) entirely — especially at `PARSE_CONFIGURATION`. A nested config registered only through scan or `register(…)` uses **its own** `@Conditional` annotations, not the enclosing class’s.

> [!tip] Interview answer
> @Import is how a Java config class pulls other types into the same container: other @Configuration classes and their @Bean methods, and since 4.2 named component classes without scanning a package. You can also import an ImportSelector or ImportBeanDefinitionRegistrar, or use @Import as a meta-annotation. @ImportResource is the XML sibling, and @Conditional on the importing configuration applies to those imports.
