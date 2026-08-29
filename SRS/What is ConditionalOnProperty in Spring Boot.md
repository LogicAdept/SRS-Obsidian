<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/AutoConfiguration #Java/Annotations #SRS

# What is ConditionalOnProperty in Spring Boot?

> [!abstract] Short answer
> **`@ConditionalOnProperty`** is a Boot **`@Conditional`**: register a `@Configuration` / `@Bean` / `@Component` only when an **`Environment`** property **matches**. Specify **`prefix` + `name`** (dashed form). **Default:** the property is **set** and **not** the string **`false`**. Pin a value with **`havingValue`**. **`matchIfMissing`** defaults to **`false`**. Several `name`s are **AND**. Booleans: prefer **`@ConditionalOnBooleanProperty`**.

## Property condition, not a binder

It does **not** inject the value (`@Value` / `@ConfigurationProperties` do). It **skips registration**. Auto-config uses the same family as `@ConditionalOnClass` / `@ConditionalOnMissingBean` ([[How do ConditionalOn annotations drive auto-configuration]]). Relaxed binding applies (`my-long-property` / `MY_LONG_PROPERTY`).

```java
@Configuration(proxyBeanMethods = false)
@ConditionalOnProperty(prefix = "app.payment", name = "enabled", havingValue = "true")
public class PaymentConfiguration {

	@Bean
	PaymentClient paymentClient() {
		return new PaymentClient();
	}
}
```

**Listing 1.** Checks **`app.payment.enabled`**. Dump’s `havingValue = "true"` is the **string** `"true"`, not a Java boolean. Without `havingValue`, `"true"`, `"on"`, `"1"`, and any other non-`false` string all match — including `"yes"`. Missing key → **no match** unless **`matchIfMissing = true`**.

```java
@Component
@ConditionalOnProperty(name = "app.mode", havingValue = "fast")
class FastPath { }
```

**Listing 2.** User `@Component`s can use it too — typical “pick one implementation” pattern ([[How do you select a Spring bean using application properties]]). Do **not** use `@Resource(name = "${…}")` for that.

```d2
direction: down
env: "Environment\napp.payment.enabled" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
ann: "@ConditionalOnProperty\nhavingValue / matchIfMissing" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
reg: "register @Bean / skip" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}

env -> ann -> reg
```

**Fig. 1.** `--debug` / Actuator **conditions** shows the match reason ([[How can you debug which auto-configuration classes applied]]). `@ConditionalOnExpression` is SpEL; **do not** reference other beans there (they initialize too early).

> [!warning] Default is “present and not `false`,” not “equals true”
> `enabled=false` **fails**. `enabled=true` **passes**. A missing key **fails** (`matchIfMissing` is false). Injecting the skipped bean → **`NoSuchBeanDefinitionException`**. Indexed keys like `values[0]` are **not** a reliable `OnProperty` target.

> [!warning] `@ConditionalOnBooleanProperty` is the boolean API
> Boot **3.5+**: default match is present and **equal to `true`**. Do not copy `havingValue = "true"` onto every flag if you can use that annotation. This is **not** `@Profile` ([[What is a Spring profile]]) and **not** `@ConditionalOnMissingBean` (bean conditions belong on **auto-config**, after user beans).

> [!tip] Interview answer
> @ConditionalOnProperty registers a bean only if an Environment property matches. I set prefix and name, havingValue if I need an exact string, and matchIfMissing if the default should be on. The default rule is the key exists and is not false. I debug skips with the conditions report.
