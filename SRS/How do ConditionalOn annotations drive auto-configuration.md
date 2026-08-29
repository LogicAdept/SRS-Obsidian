<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/AutoConfiguration #Java/Annotations #SRS

# How do ConditionalOn annotations drive auto-configuration?

> [!abstract] Short answer
> Auto-configuration classes are ordinary `@Configuration` types (`@AutoConfiguration`) gated by Spring **`@Conditional`** variants. Boot’s **`@ConditionalOn*`** annotations decide whether a class or `@Bean` method is registered: **classpath** (`OnClass` / `OnMissingClass`), **already-defined beans** (`OnBean` / `OnMissingBean`), **Environment properties**, and **web vs non-web**. A user `@Bean` of the same type wins because auto-config methods typically carry **`@ConditionalOnMissingBean`**, and auto-config is processed **after** user definitions.

## Conditions are how auto-config stays optional

`@AutoConfiguration` is meta-annotated with `@Configuration`. Extra `@Conditional` annotations constrain *when* that configuration applies. The usual pair is **`@ConditionalOnClass`** (the library is actually on the classpath) and **`@ConditionalOnMissingBean`** (you have not already declared the bean). That is why adding your own `DataSource` makes Boot’s embedded-database auto-config back away — not because Boot “detects intent”, but because the missing-bean condition no longer matches.

These annotations live in `org.springframework.boot.autoconfigure.condition`. They are reusable on **your** `@Configuration` classes and `@Bean` methods as well as on Boot’s own auto-config; they are not a private auto-config DSL.

```java
@AutoConfiguration
public final class MyAutoConfiguration {

	@Configuration(proxyBeanMethods = false)
	@ConditionalOnClass(SomeService.class)
	static class SomeServiceConfiguration {

		@Bean
		@ConditionalOnMissingBean
		SomeService someService() {
			return new SomeService();
		}
	}
}
```

**Listing 1.** Conceptual pattern from Boot’s auto-configuration guide: isolate `@ConditionalOnClass` on a nested `@Configuration` so the JVM does not load `SomeService` before the condition runs; `@ConditionalOnMissingBean` on the `@Bean` method defaults the check to the return type.

```d2
direction: right
inputs: "Classpath · beans so far\nEnvironment · web type" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
conds: "@ConditionalOnClass\n@ConditionalOnMissingBean\n@ConditionalOnProperty\n@ConditionalOnWebApplication" {
  width: 280
  height: 110
  style.fill: "#fff3e0"
}
apply: "Register @Configuration / @Bean" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
skip: "Skip (see conditions report)" {
  width: 220
  height: 70
  style.fill: "#ffebee"
}

inputs -> conds
conds -> apply
conds -> skip
```

**Fig. 1.** Each `On*` annotation is a `Condition` that can skip a `@Configuration` class or a `@Bean` method ([[How can you debug which auto-configuration classes applied]]).

## The annotations dumps actually name

| Annotation | Matches when |
|---|---|
| **`@ConditionalOnClass`** / **`@ConditionalOnMissingClass`** | Named types **are** / **are not** on the classpath. Class references are parsed with **ASM**, so `value = Foo.class` is safe on a `@Configuration` type even if `Foo` is absent. Use `name` (a `String`) for meta-annotations. |
| **`@ConditionalOnBean`** / **`@ConditionalOnMissingBean`** | A matching bean **is** / **is not** already in the `BeanFactory` (by `value` type, `name`, or `search` across parent contexts). On a `@Bean` method with no attributes, the type defaults to the **return type**. |
| **`@ConditionalOnProperty`** | An Environment property (`prefix` + `name`) is present and **not** equal to `false`. `havingValue` tightens the expected string; `matchIfMissing` defaults to **`false`**. Multiple `name`s are **AND**. Prefer `@ConditionalOnBooleanProperty` for booleans. |
| **`@ConditionalOnWebApplication`** / **`@ConditionalOnNotWebApplication`** | The context **is** / **is not** a web application (`type` defaults to `ANY`; can require servlet or reactive). A servlet app uses `WebApplicationContext`, `session` scope, or `ConfigurableWebEnvironment`. |

If a whole auto-configuration should stay off, exclude the class ([[How do you disable a specific auto-configuration class]]) rather than fighting each nested condition.

> [!warning] `@ConditionalOnMissingBean` only sees beans registered so far
> Bean conditions are evaluated against **definitions already processed**. Auto-configuration is guaranteed to run **after** user `@Bean` methods, which is why your `DataSource` (or `SomeService`) wins. Do **not** put `@ConditionalOnBean` / `@ConditionalOnMissingBean` on ordinary application `@Configuration` and expect them to see every other user bean — order is not guaranteed. If another auto-config might create the candidate, the consumer must run **`@AutoConfigureAfter`** that class. Class-level bean conditions skip registering the `@Configuration` **bean**; they do not skip creating the Java class. Keep `@Bean` return types **concrete**: the condition can see only the method signature.

> [!warning] Class conditions on `@Bean` methods can load the class anyway
> `@ConditionalOnClass` on a `@Bean` method is too late: the JVM may already have loaded the return type and failed if the library is missing. Put the class condition on a **nested `@Configuration`**, as in Listing 1. `@ConditionalOnProperty` is **not** “true-only”: a present value other than `false` matches unless you set `havingValue`. It also does **not** reliably match collection-style keys such as `spring.example.values[0]`. The dump name `@ConditionalOnMissingWebApplication` is wrong — the annotation is **`@ConditionalOnNotWebApplication`**.

> [!tip] Interview answer
> Auto-config is `@Configuration` plus `@ConditionalOn*` so beans appear only when they make sense. OnClass keys off the classpath without loading missing types; OnMissingBean is why a user `@Bean` replaces Boot’s default, because auto-config runs after user definitions. OnProperty checks the Environment — present and not false unless you set havingValue or matchIfMissing. OnWebApplication versus OnNotWebApplication switches servlet or reactive stacks. The usual interview trap is using OnMissingBean on your own config, where bean order is not guaranteed.
