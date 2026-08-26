<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Java/Testing/Mockito #Testing/Mocking #Java/Annotations #SRS

# What is the difference between MockitoBean and MockBean?

> [!abstract] Short answer
> They are **two generations of the same Spring idea**: replace (or create) a **bean in the test `ApplicationContext` with a Mockito mock**. **`@MockBean`** lived in Boot (`org.springframework.boot.test.mock.mockito`), **deprecated in 3.4**, **removed in 4.0**. **`@MockitoBean`** is **Spring Framework 6.2+** (`org.springframework.test.context.bean.override.mockito`) — Boot **4.1** samples use only this. Neither is Mockito’s **`@Mock`**, which **never** registers a Spring bean. Dump “`@MockitoBean` is Mockito-specific” is **false**.

## Same job, new package, stricter lifecycle

`@MockitoBean` is a TestContext **bean override** with strategy **`REPLACE_OR_CREATE`** (fail if missing: **`enforceOverride = true`** → **`REPLACE`**). The mock is a **bare Mockito object** — **not** an AOP proxy (`@Transactional` / `@Cacheable` on the original type **do not wrap** the mock). Field name / `@Qualifier` is part of the **context cache key** — name fields **consistently** across classes. Spy counterpart: **`@MockitoSpyBean`** (Boot **`@SpyBean`** also removed).

`@Mock` + `MockitoExtension` is a **unit** test with **no** context. Mixing `@Mock` on a field you then `@Autowired` as a collaborator **does not** put that mock in the container. Unit vs context: [[What is the difference between Mock and MockBean]]. Spy: [[What is SpyBean]]. Slice usage: [[What is the WebMvcTest annotation]]. Cache: [[How does the Spring TestContext framework cache the ApplicationContext]]. Service tests: [[How do you test the service layer in Spring]].

```java
@WebMvcTest(UserVehicleController.class)
class MyControllerTests {
    @MockitoBean UserVehicleService userVehicleService;
}
```

**Listing 1.** Conceptual Boot **4.1**. Import **`org.springframework.test.context.bean.override.mockito.MockitoBean`**. The old **`org.springframework.boot.test.mock.mockito.MockBean`** **does not exist** on Boot 4.

```java
@SpringJUnitConfig(TestConfig.class)
class BeanOverrideTests {
    @MockitoBean CustomService customService;
}
```

**Listing 2.** Conceptual Framework **7**: works on **any** TestContext test, not only Boot slices.

```d2
direction: down
mock: "@Mock\nMockitoExtension, no context" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
bean: "@MockitoBean\nREPLACE_OR_CREATE in ApplicationContext" {
  width: 340
  height: 55
  style.fill: "#e3f2fd"
}
gone: "@MockBean (Boot)\nremoved in 4.0" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}

gone -> bean: "replaced by"
```

**Fig. 1.** One Spring override API now. Mockito **`@Mock`** is the other column.

> [!warning] `@MockBean` does not compile on Boot 4
> Course dumps still import **`boot.test.mock.mockito.MockBean`**. Change the import and the name. **`@SpyBean` → `@MockitoSpyBean`**.

> [!warning] The mock is not the production proxy
> Stubbing a `@MockitoBean` **`@Service`** does **not** run `@Transactional` / `@PreAuthorize` on that mock. Mock **collaborators**, keep the real bean under test if you need AOP.

> [!warning] Prototype becomes a singleton mock
> Scoped / `FactoryBean` targets are replaced with a **singleton** mock. Field names that differ across test classes **split the context cache**.

> [!tip] Interview answer
> **`@MockitoBean` is Spring’s bean override that puts a Mockito mock in the test context. `@MockBean` was Boot’s older annotation — deprecated 3.4, gone in 4.** `@Mock` is Mockito-only and never a Spring bean. On Boot 4, say MockitoBean, not MockBean.
