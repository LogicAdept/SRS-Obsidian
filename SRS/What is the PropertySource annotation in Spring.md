<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Spring/Boot/Properties #Java/Annotations #SRS

# What is the PropertySource annotation in Spring?

> [!abstract] Short answer
> `@PropertySource` (since **3.1**, on a `@Configuration` class) **adds a `PropertySource` to the `Environment`** so `Environment.getProperty` and `${…}` placeholders can see those keys. It is **not** SpEL (`#{…}`). Repeat it (or wrap with `@PropertySources`) for several locations. Default factory loads **`.properties` and XML `Properties`**, not YAML. In **Spring Boot**, these sources attach only at **refresh** — too late for `logging.*` / `spring.main.*` — and sit **below** `application.properties`, OS env, and command line in Boot’s override order.

## Add files to the `Environment`

```java
@Configuration
@PropertySource("classpath:/com/myco/app.properties")
public class AppConfig {

    @Autowired
    Environment env;

    @Bean
    public TestBean testBean() {
        TestBean bean = new TestBean();
        bean.setName(env.getProperty("testbean.name"));
        return bean;
    }
}
```

**Listing 1.** Conceptual. `env.getProperty` reads the `Environment` directly. `@Value("${…}")` needs an embedded placeholder resolver / `PropertySourcesPlaceholderConfigurer` ([[What is PropertySourcesPlaceholderConfigurer]], [[How does the Value annotation inject properties]]).

`${…}` in the **location string** is resolved against sources **already** registered (system properties, env vars, …). `${my.placeholder:default/path}` supplies a default; with no default, a missing key throws `IllegalArgumentException`.

As of Framework **6.1**, locations may use wildcards (`classpath*:/config/*.properties`). Each location becomes its **own** `PropertySource`, in declaration (or wildcard-resolution) order. Optional attributes: `name`, `encoding` (since **4.3**), `ignoreResourceNotFound` (default **`false`**, since **4.0**), custom `factory`. Repeatable; also usable as a meta-annotation.

**Last `@PropertySource` processed wins** on duplicate keys. That order is the order `@Configuration` classes are **registered**. Component-scanning makes override order **hard to predict** — use `MutablePropertySources` when you must control it.

```d2
direction: down
file: "app.properties" {
  width: 180
  height: 40
  style.fill: "#fff3e0"
}
ann: "@PropertySource on @Configuration" {
  width: 260
  height: 45
  style.fill: "#e3f2fd"
}
env: "Environment PropertySources" {
  width: 240
  height: 45
  style.fill: "#e8f5e9"
}
use: "getProperty / ${…} / @Value" {
  width: 240
  height: 40
  style.fill: "#f3e5f5"
}

file -> ann
ann -> env
env -> use
```

**Fig. 1.** The annotation contributes a source; it does not bind a typed prefix (`@ConfigurationProperties`) and does not evaluate SpEL.

In Boot, `@PropertySource` is an early, **low-precedence** source. Config data, environment variables, and command-line arguments override it. YAML is **not** loaded by `@PropertySource` / `@TestPropertySource` — use a `.properties` file (or a custom `PropertySourceFactory`). Multi-document property files are also unsupported there.

> [!warning] Too late for `logging.*` and `spring.main.*`
> Boot adds `@PropertySource` entries only when the context **refreshes**. Logging and `SpringApplication` already read `Environment` keys before that. Put those settings in `application.properties`, system properties, or env vars.

> [!warning] Missing file fails refresh by default
> `ignoreResourceNotFound` defaults to `false`. An optional classpath file must set it `true`, or startup throws. Duplicate keys across files follow **registration order**, not “first file wins.”

> [!tip] Interview answer
> PropertySource on a configuration class dumps a properties or XML Properties file into the Environment so getProperty and dollar-brace placeholders can see it. It is not SpEL, not YAML by default, and in Boot it is a low-precedence source that appears only at refresh — too late for logging and spring.main. Last registered source wins on clashes.
