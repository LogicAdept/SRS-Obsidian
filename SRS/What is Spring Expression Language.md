<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/SpEL #SRS

# What is Spring Expression Language?

> [!abstract] Short answer
> **SpEL** is Spring’s expression language for **querying and manipulating an object graph at runtime**. Syntax is close to Jakarta EL, plus **method calls**, constructors, bean lookups, collection selection/projection, and string templating. In bean XML and `@Value`, a SpEL string is wrapped as `#{…}`. That is **not** `${…}`, which is a **property placeholder** resolved by `PropertySourcesPlaceholderConfigurer` / the `Environment` ([[What is PropertySourcesPlaceholderConfigurer]], [[How does the Value annotation inject properties]]). The language is portfolio-wide (Security method expressions, cache keys, event `condition`s) but the **`EvaluationContext`** (root object, variables, what `hasRole` means) is per feature.

## Language vs parser vs bean `#{…}`

SpEL is **not** tied to the IoC container. You can parse with `SpelExpressionParser` (`org.springframework.expression`) against any root object. Most application code never touches the parser: you only write expression **strings**. The container supplies parser, context, and predefined variables.

```java
ExpressionParser parser = new SpelExpressionParser();
Expression exp = parser.parseExpression("'Hello World'.concat('!')");
String message = exp.getValue(String.class);
```

**Listing 1.** Conceptual. Parse once; `getValue` evaluates. Failures are `ParseException` / `EvaluationException`.

In bean definitions the delimiter is `#{ }`. Other beans are **predefined variables** by bean name (no `#` prefix). So are `environment`, `systemProperties`, and `systemEnvironment`.

```java
@Value("#{ systemProperties['user.region'] }")
private String defaultLocale;
```

```xml
<property name="initialShapeSeed" value="#{ numberGuess.randomNumber }"/>
```

**Listing 2.** Conceptual. Field `@Value` and XML property — same language. `#{ numberGuess.randomNumber }` reads another bean’s property.

The language includes literals, properties/indexers, `T(…)` types, constructors, operators (including `matches`, Elvis `?:`, safe-navigation `?.`), assignment, `#variables`, `@beanName` (and `&factoryBean` for the factory itself when a `BeanResolver` is set), and templated expressions. Default max length is **10,000** characters (`spring.context.expression.maxLength` for context-embedded parse).

Two evaluation contexts:

- `StandardEvaluationContext` — **full** language (types, constructors, beans). **Never** evaluate an expression from an untrusted source with it.
- `SimpleEvaluationContext` — restricted subset (no type/constructor/bean refs); still **not** a sandbox if the root object exposes dangerous methods (`File.delete()` is “accessor-shaped”).

```d2
direction: down
str: "#{ expression string }" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
parser: "SpelExpressionParser\n→ Expression AST" {
  width: 240
  height: 60
  style.fill: "#fff3e0"
}
ctx: "EvaluationContext + root\n(beans, Security, events…)" {
  width: 280
  height: 60
  style.fill: "#e8f5e9"
}
val: "typed value / side effects" {
  width: 240
  height: 50
  style.fill: "#f3e5f5"
}

str -> parser
parser -> ctx
ctx -> val
```

**Fig. 1.** Same grammar; the context decides which beans, methods, and variables exist ([[What are Spring Security expressions]]).

> [!warning] `#{…}` is SpEL; `${…}` is not
> `${jdbc.url}` is placeholder substitution into the bean definition **before** instances exist. `#{ systemProperties['user.region'] }` **evaluates** against a graph (here the `systemProperties` map). Mixing the delimiters is the usual interview miss. You can nest a placeholder inside SpEL only if the placeholder is resolved first by the configurer.

> [!warning] Untrusted SpEL is arbitrary code
> Full SpEL can call constructors and methods via reflection. Official rule: treat only developer/admin-authored strings as trusted. User input, query params, or uploaded rules must not be parsed as SpEL. `SimpleEvaluationContext` is a **best-effort subset**, not a guarantee.

> [!tip] Interview answer
> SpEL evaluates expressions against an object graph at runtime — properties, methods, beans, operators. In Spring config you write #{…}; ${…} is a property placeholder, not SpEL. Security annotations use the same language with a security EvaluationContext. Do not eval strings you did not write.
