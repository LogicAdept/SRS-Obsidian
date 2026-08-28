<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS

# What is the `@ContextConfiguration` annotation?

> [!abstract] Short answer
> **`@ContextConfiguration`** (Spring Framework 2.5+, `org.springframework.test.context`) is the TestContext metadata for **how to load** the test `ApplicationContext`: classpath **XML / Groovy `locations`**, **component `classes`**, and/or **`ApplicationContextInitializer`s**. It does **not** start a test by itself — [[What is SpringExtension]] or [[What is SpringRunner]] still has to drive [[What is the Spring TestContext Framework]].

## What you declare

`value` is an alias for `locations` (do not set both). `classes` (since 3.1) are **component classes**: `@Configuration`, `@Component` / `@Service` / `@Repository`, JSR-330 types, any type with `@Bean` methods, or a class meant to be registered as a bean. Resource paths are typically classpath XML or Groovy; they may also be file-system paths. Optional: `initializers`, custom `loader`, and `name` (hierarchy level — see [[What is ContextHierarchy]]).

You usually **omit `loader`**. Runtime default is **`DelegatingSmartContextLoader`**, or **`WebDelegatingSmartContextLoader`** when **`@WebAppConfiguration`** is present.

```java
@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = PaymentConfiguration.class)
class PaymentServiceTests {

	@Autowired
	PaymentService paymentService;
}
```

**Listing 1.** Conceptual Jupiter test. JUnit 4 equivalent: `@RunWith(SpringRunner.class)` plus the same annotation. Shorthand: `@SpringJUnitConfig(PaymentConfiguration.class)` (meta-annotates `@ExtendWith(SpringExtension.class)` + `@ContextConfiguration`).

If `classes` is empty, `AnnotationConfigContextLoader` may **detect default configuration classes**: **static nested** types that qualify as `@Configuration`. If you use locations instead, `AbstractContextLoader` can **generate default XML locations** when none are listed. `@SpringBootTest` is **Boot**: it searches for `@SpringBootConfiguration` and does **not** require this annotation.

`inheritLocations` and `inheritInitializers` default to **`true`**. A subclass **appends** its locations/classes (or adds initializers) to those from superclasses and enclosing classes. `false` **replaces** the inherited list.

```d2
direction: down
ann: "@ContextConfiguration" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
loader: "DelegatingSmartContextLoader\n(or Web* if @WebAppConfiguration)" {
  width: 300
  height: 50
  style.fill: "#fff3e0"
}
ctx: "ApplicationContext" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}

ann -> loader
loader -> ctx
```

**Fig. 1.** The annotation is metadata. The `SmartContextLoader` builds the context; the static cache key includes these attributes — [[How does the Spring TestContext framework cache the ApplicationContext]].

> [!warning]InheritLocations is true by default
> `@ContextConfiguration(classes = ExtraConfig.class)` on a subclass **adds** `ExtraConfig` next to the superclass classes. It does **not** drop the parent config unless you set **`inheritLocations = false`**.

> [!tip] Interview answer
> **`@ContextConfiguration` tells TestContext which XML, component classes, or initializers to load.** Pair it with `SpringExtension` (or JUnit 4 `SpringRunner`). `@SpringJUnitConfig` folds the extension in. Boot’s `@SpringBootTest` is a different, higher-level loader. Subclasses inherit and append locations unless you turn inheritance off.
