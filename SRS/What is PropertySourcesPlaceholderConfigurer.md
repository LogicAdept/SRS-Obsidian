<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #SRS

# What is PropertySourcesPlaceholderConfigurer?

> [!abstract] Short answer
> `PropertySourcesPlaceholderConfigurer` (since **3.1**) is a `BeanFactoryPostProcessor` that **rewrites bean-definition strings** — and `@Value("${…}")` — by resolving `${property}` placeholders **before** ordinary beans are instantiated. It is the general replacement for deprecated `PropertyPlaceholderConfigurer`. Values come from its `PropertySources`: the `Environment`, optional local files/`Properties`, or a set you pass to `setPropertySources`. XML `context:property-placeholder` registers this type (spring-context **3.1+** XSD).

## Metadata, not SpEL, not instances

A `BeanFactoryPostProcessor` edits **configuration metadata** (`BeanDefinition`s) before the container creates any beans other than post-processors ([[What is the difference between BeanFactoryPostProcessor and BeanPostProcessor]]). `${jdbc.username}` is Ant / log4j / JSP-EL style placeholder syntax, **not** SpEL (`#{…}`). `@Value("${maxReadResults}")` uses this placeholder mechanism; `@Value("#{…}")` is SpEL ([[How does the Value annotation inject properties]]).

Resolution order by default: **Environment** property sources first, then **local** properties from `setLocations` / `setProperties` (`localOverride` defaults to **`false`**, so files lose to the Environment). If you call `setPropertySources`, Environment and local files are **ignored**. After local files, the reference still notes a fallback to Spring `Environment` properties and JVM `System` properties when a key is missing from those files.

```xml
<bean class="org.springframework.context.support.PropertySourcesPlaceholderConfigurer">
    <property name="locations" value="classpath:jdbc.properties"/>
</bean>

<bean id="dataSource" class="example.DataSource">
    <property name="url" value="${jdbc.url}"/>
    <property name="username" value="${jdbc.username}"/>
</bean>
```

**Listing 1.** Conceptual. The configurer runs as a BFPP; `${…}` in the `DataSource` definition is replaced in the metadata.

Equivalent shortcut (one per application unless you use a **different** placeholder syntax):

```xml
<context:property-placeholder location="classpath:jdbc.properties"/>
```

**Listing 2.** Conceptual. Do not add a second `property-placeholder` for a second file; build one `PropertySourcesPlaceholderConfigurer` that merges locations instead.

You can change prefix, suffix, default-value separator, and escape character (`spring.placeholder.escapeCharacter.default` as a JVM / `SpringProperties` switch). `${custom.strategy.class}` can even replace a `class` attribute; a bad class name fails when that singleton is pre-instantiated.

`PropertyOverrideConfigurer` is a different BFPP: it **overrides** properties that already have defaults, rather than filling `${…}` holes.

Declare a `@Bean` factory method that returns this type as **`static`**, or the `@Configuration` class initializes too early for `@Value` / `@Autowired` / `@PostConstruct` on that class.

```d2
direction: down
env: "Environment PropertySources" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
local: "local files / Properties\n(localOverride false → last)" {
  width: 280
  height: 60
  style.fill: "#fff3e0"
}
pspc: "PSPC.postProcessBeanFactory\nreplace ${…} in BeanDefinitions" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
beans: "Then instantiate ordinary beans" {
  width: 260
  height: 50
  style.fill: "#f3e5f5"
}

env -> pspc
local -> pspc
pspc -> beans
```

**Fig. 1.** Placeholders are resolved in definitions; instances never see the `${…}` tokens if resolution succeeded.

> [!warning] `PropertyPlaceholderConfigurer` is not the current type
> It is `@Deprecated(since="5.2", forRemoval=true)` — **remove in 8.0**. It resolved against local + system properties / env vars and `systemPropertiesMode`, **not** the `Environment` `PropertySource` chain. Running **both** configurers can substitute the same `${…}` twice or against different source orders. Prefer PSPC (or a single `property-placeholder`).

> [!warning] Two `property-placeholder` elements
> Official guidance: **one** element for the properties you need. Several are allowed only with **distinct** placeholder syntax. To split files, use **one** PSPC with multiple locations, not two default `${…}` configurers.

> [!tip] Interview answer
> PropertySourcesPlaceholderConfigurer is the BeanFactoryPostProcessor that replaces ${placeholders} in bean definitions and @Value against the Environment and optional property files, before beans are created. context:property-placeholder registers it. Do not confuse it with SpEL, or with the deprecated PropertyPlaceholderConfigurer that ignored the Environment model.
