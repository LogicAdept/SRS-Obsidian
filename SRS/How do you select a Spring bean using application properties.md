<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Properties #Java/Annotations #SRS

# How do you select a Spring bean using application properties?

> [!abstract] Short answer
> Put **`@ConditionalOnProperty`** on each implementation (or on the `@Bean` method that creates it). **`name`** (dashed form) plus **`havingValue`** must match the Environment. Only the matching type is **registered**, so you inject **by type**. Booleans: prefer **`@ConditionalOnBooleanProperty`**. Profiles (`@Profile` + `spring.profiles.active`) are the other Environment gate. Do **not** “select” with **`@Resource(name="${…}")`**.

## Register one implementation, not two names

`@ConditionalOnProperty` is `@Conditional`: the property must be **present** and, by default, **not** the string `false`. **`havingValue`** pins the expected string (`real` vs `mock`). **`matchIfMissing`** defaults to **`false`**. Multiple `name`s are **AND**. Prefix + name: `prefix = "app.config"` and `name = "my-value"` → **`app.config.my-value`**. Use **dashed** keys (`my-long-property`) ([[How do ConditionalOn annotations drive auto-configuration]], [[What is ConditionalOnProperty in Spring Boot]]).

```java
public interface GreetingService {
	String sayHello();
}

@Component
@ConditionalOnProperty(name = "application.greeting", havingValue = "real")
class RealGreetingService implements GreetingService {
	@Override
	public String sayHello() {
		return "I'm real";
	}
}

@Component
@ConditionalOnProperty(name = "application.greeting", havingValue = "mock")
class MockGreetingService implements GreetingService {
	@Override
	public String sayHello() {
		return "I'm mock";
	}
}
```

**Listing 1.** One `GreetingService` in the context. The controller takes **`GreetingService`** — no bean-name string, no `@Resource`.

```properties
application.greeting=real
```

**Listing 2.** Without `havingValue`, a present value other than `false` matches **every** such condition — both beans would load. Missing key: **neither** matches (`matchIfMissing` is false).

`@ConditionalOnBooleanProperty` (Boot **3.5+**): default is present and **equal to `true`**, not “anything but false”. `@ConditionalOnExpression` is SpEL on a condition; **do not** reference other beans in that expression (they initialize **too early** and skip post-processing).

`@Profile("mock")` plus `spring.profiles.active=mock` is the same idea with **named Environment groups** ([[What is the Profile annotation in Spring]], [[How do you activate a Spring profile]]).

```d2
direction: down
prop: "application.greeting=real" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
cond: "@ConditionalOnProperty\nhavingValue=real | mock" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
ctx: "One GreetingService bean" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}

prop -> cond -> ctx
```

**Fig. 1.** The property chooses **which definition is registered**. Conditions report (`/actuator/conditions`) shows the skip reason ([[How can you debug which auto-configuration classes applied]]).

> [!warning] `@Resource(name="${application.greeting}")` is not the documented API
> `@Resource`’s `name` is a **bean name** for `CommonAnnotationBeanPostProcessor` (or JNDI). Framework docs show **literals** like `myMovieFinder`, not property placeholders. The dump also injects **`GreeterService`** while the types are **`GreetingService`**, and it keeps **both** `@Component`s — `@Autowired` by type would then be **`NoUniqueBeanDefinitionException`**. `${…}` is a **placeholder**, not SpEL (`#{…}`). `@Value` is for **values**, not a bean selector ([[What is the difference between Value and ConfigurationProperties]]).

> [!warning] Collection indexes and `OnMissingBean` on user config
> `@ConditionalOnProperty` does **not** reliably see `spring.example.values[0]`. Bean conditions on **your** `@Configuration` are **not** ordered like auto-config — do not mix “pick by property” with `@ConditionalOnMissingBean` and expect every other user bean to exist yet.

> [!tip] Interview answer
> I put @ConditionalOnProperty on each implementation with the same name and different havingValue so only one GreetingService is registered, then I inject by type. For a boolean flag I use @ConditionalOnBooleanProperty. Profiles are the other switch. I do not use @Resource with a ${} bean name — that is a popular dump, not how Spring documents resource injection.
