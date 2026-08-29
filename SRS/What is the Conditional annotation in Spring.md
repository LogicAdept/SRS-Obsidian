<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Annotations #SRS

# What is the Conditional annotation in Spring?

> [!abstract] Short answer
> `@Conditional` (since **4.0**) marks a `@Component` / `@Configuration` type, a composed annotation, or a `@Bean` method as eligible for registration **only if every** listed `Condition` returns `true`. Conditions run **immediately before** the `BeanDefinition` would be registered. They follow `BeanFactoryPostProcessor` rules: **never touch bean instances**. `@Profile` is implemented as `@Conditional`. Boot’s `@ConditionalOnClass`, `@ConditionalOnMissingBean`, `@ConditionalOnProperty`, `@ConditionalOnWebApplication` are **composed** annotations on this same SPI — not a second framework.

## `matches` against metadata, then maybe register

`Condition.matches(ConditionContext, AnnotatedTypeMetadata)` sees:

- `getEnvironment()`, `getResourceLoader()`, `getClassLoader()`
- `getRegistry()` — the `BeanDefinitionRegistry`
- `getBeanFactory()` — may be `null`

`AnnotatedTypeMetadata` is the class or method’s annotation data (how `@Profile` reads its `value`). **All** `Condition` classes on `@Conditional` must match. Several conditions are ordered with `Ordered` / `@Order`.

If you put `@Conditional` on a `@Configuration` class, it also gates that class’s `@Bean` methods, `@Import`, and `@ComponentScan` ([[How does Import register beans in Spring]]). It is **not** `@Inherited`: superclass or overridden-method conditions are ignored. Nested `@Configuration` types scanned **on their own** (component scan / explicit register) do **not** inherit the enclosing class’s `@Conditional`; redeclare or use a composed annotation on both.

```java
public final class OnLinuxCondition implements Condition {

    @Override
    public boolean matches(ConditionContext context, AnnotatedTypeMetadata metadata) {
        String os = context.getEnvironment().getProperty("os.name", "");
        return os.toLowerCase().contains("linux");
    }
}

@Configuration
@Conditional(OnLinuxCondition.class)
class LinuxOnlyConfiguration {

    @Bean
    LinuxService linuxService() {
        return new LinuxService();
    }
}
```

**Listing 1.** Conceptual. The condition uses `Environment`, not `getBean`.

For checks that must see **already parsed** `@Configuration` classes (typical “is this bean already defined?”), implement `ConfigurationCondition` and return `ConfigurationPhase.REGISTER_BEAN`. `PARSE_CONFIGURATION` runs while a `@Configuration` class is parsed and can **keep that class out entirely**. `REGISTER_BEAN` does not block adding `@Configuration` classes.

```d2
direction: down
ann: "@Conditional(MyCondition.class)" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
match: "Condition.matches(context, metadata)" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
yes: "Register BeanDefinition" {
  width: 220
  height: 45
  style.fill: "#e8f5e9"
}
no: "Veto — no bean" {
  width: 200
  height: 45
  style.fill: "#fce4ec"
}

ann -> match
match -> yes: true
match -> no: false
```

**Fig. 1.** Gating is registration-time, before instances ([[What is BeanDefinitionRegistryPostProcessor]]).

Spring Boot auto-configuration is ordinary `@Configuration` plus extra `@Conditional…` meta-annotations ([[How do ConditionalOn annotations drive auto-configuration]], [[What is ConditionalOnProperty in Spring Boot]]). `@ConditionalOnProperty` is **one** Boot condition (Environment property), not a synonym for `@Conditional`. `@Profile` is the Framework specialization for environment profiles ([[What is the Profile annotation in Spring]]).

> [!warning] No live beans in `matches`
> Official restriction: same as a `BeanFactoryPostProcessor`. Looking up instances can instantiate too early and skip post-processors. Use the registry, Environment, classpath, and annotation metadata. Need other beans? `ConfigurationCondition` + `REGISTER_BEAN` after configuration classes are parsed — still definitions, not a finished object graph.

> [!warning] Nested `@Configuration` does not always inherit the outer condition
> If the nested class is found by `@ComponentScan` or registered directly, only **its** `@Conditional` annotations apply. Copy them, or extract a composed annotation used on both types.

> [!tip] Interview answer
> @Conditional registers a component or @Bean only when every Condition.matches is true, before the definition is registered. Conditions must not touch live beans. @Profile is built on it; Boot’s ConditionalOn* types are composed annotations around the same API. ConfigurationCondition lets you wait until REGISTER_BEAN if you need to see other configuration classes first.
