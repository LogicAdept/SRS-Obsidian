<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Java/Testing/Mockito #Testing/Mocking #Java/Annotations #SRS

# What is the difference between Mock and MockBean?

> [!abstract] Short answer
> **`@Mock`** is **Mockito’s** annotation: a mock object in the **test class**, wired with **`MockitoExtension` / `@InjectMocks` / `new`**. **No `ApplicationContext`.** **`@MockBean`** was **Boot’s** annotation that **replaced a Spring bean** with a Mockito mock inside the test context. It was **deprecated in 3.4** and **removed in Boot 4** — the replacement is Framework **`@MockitoBean`**. Interview cue still says “MockBean”; on current Boot you **write `@MockitoBean`**. Mixing `@Mock` with `@Autowired` does **not** put that mock in the container.

## Two runtimes: test fields vs bean factory

`@Mock` (`org.mockito.Mock`) is processed by **`MockitoAnnotations.openMocks`** or **`@ExtendWith(MockitoExtension.class)`** (`mockito-junit-jupiter`). `@InjectMocks` fills the **largest constructor**. Boot’s testing chapter starts here: **unit-test with `new`**, no Spring.

`@MockitoBean` (`org.springframework.test.context.bean.override.mockito`) is a TestContext **bean override** (`REPLACE_OR_CREATE`). The test class needs **`SpringExtension`** (`@SpringBootTest`, `@WebMvcTest`, `@SpringJUnitConfig`, …). The mock is a **singleton** in that context and a **cache-key customizer**. Old **`@MockBean`** did the same job from **`org.springframework.boot.test.mock.mockito`**.

`@Mock` is cheaper (no refresh). `@MockitoBean` is how a **slice / integration** test stubs a `@Service` the controller constructor needs. Rename: [[What is the difference between MockitoBean and MockBean]]. Unit path: [[How do you test the service layer in Spring]]. Slice: [[What is the WebMvcTest annotation]]. Spy: [[What is SpyBean]].

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTests {
    @Mock OrderRepository orders;
    @InjectMocks OrderService service;
}
```

**Listing 1.** Conceptual Mockito **5** unit test. **`orders` is not a Spring bean.**

```java
@WebMvcTest(OrderController.class)
class OrderControllerTests {
    @MockitoBean OrderService orders; // Boot 4; not @Mock, not @MockBean
}
```

**Listing 2.** Conceptual Boot **4.1** slice. The controller is a **real bean**; the collaborator is a **context mock**.

```d2
direction: down
unit: "@Mock + @InjectMocks\nno ApplicationContext" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
ctx: "@MockitoBean\nbean override in the context" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
old: "@MockBean\nBoot 3.x only" {
  width: 240
  height: 40
  style.fill: "#ffebee"
}

old -> ctx: "renamed / moved"
```

**Fig. 1.** Same Mockito mock type; **different who creates and injects it.**

> [!warning] `@Mock` is invisible to `@Autowired`
> A slice test that `@Mock`s `UserService` and expects the controller to receive it **fails at wiring** (or injects the **real** bean). Use **`@MockitoBean`**.

> [!warning] `@MockBean` does not compile on Boot 4
> Cue name stays “MockBean.” Source code uses **`@MockitoBean`**. **`@Spy` vs `@MockitoSpyBean`** is the same split.

> [!warning] `@InjectMocks` is not a Spring context
> It will **not** apply `@Transactional` / `@PreAuthorize`. Need those interceptors → Spring test + mock the **collaborators**.

> [!tip] Interview answer
> **`@Mock` is Mockito, no Spring. “MockBean” means a mock registered as a bean — on Boot 4 that annotation is `@MockitoBean`.** Use `@Mock` for `new` service tests; use `@MockitoBean` in `@WebMvcTest` / `@SpringBootTest`. Do not mix `@Mock` with `@Autowired`.
