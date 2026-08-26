<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Java/Testing/Mockito #Testing/Mocking #Java/Annotations #SRS

# How do you test the service layer in Spring?

> [!abstract] Short answer
> Two official paths. **Plain unit:** construct the service with **`new`** (or **`@InjectMocks`**) and stub collaborators with Mockito **`@Mock`** under **`@ExtendWith(MockitoExtension.class)`** — **no `ApplicationContext`**. Boot’s testing chapter starts here: DI exists so you can unit-test **without Spring**. **Need a proxy** (`@Transactional`, `@Cacheable`, `@PreAuthorize`, `@Validated`)? Load a **narrow context** (`@SpringJUnitConfig` / `@SpringBootTest(classes = …)` / `webEnvironment = NONE`) and replace repositories with **`@MockitoBean`** (Framework **6.2+**; Boot **4** **removed `@MockBean`**). There is **no `@ServiceTest` slice**.

## `new` first; context only for AOP

`MockitoExtension` (`mockito-junit-jupiter`, on `spring-boot-starter-test`) processes **`@Mock` / `@Spy` / `@InjectMocks`**. `@InjectMocks` uses the **largest constructor**, then setters, then fields — **silent if nothing injects**. Prefer an explicit constructor over hoping Mockito wired the field.

`@MockitoBean` is a **TestContext bean override** (`REPLACE_OR_CREATE`). It lives on a **Spring** test (`SpringExtension`). The mock is a **bare Mockito object** — **not** wrapped in the production AOP proxy. Stub **`UserRepository`**, `@Autowired` the **real** `@Service`. Mocking the service itself tests **nothing** about its code.

`@SpringBootTest` without `classes` / a slice loads **the whole app** (auto-config, web MOCK by default). That is an **integration** test, not a service unit. Slices (`@DataJpaTest`, `@WebMvcTest`) do not target `@Service`. Method security: [[How do you test method security without replacing SecurityFilterChain]]. Override API: [[What is the difference between MockitoBean and MockBean]]. Full context: [[What is SpringBootTest]]. Slices: [[What are Spring Boot test slices]].

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTests {

    @Mock OrderRepository orders;
    @InjectMocks OrderService service;

    @Test
    void placesOrderWhenStockExists() {
        given(this.orders.findById("o-1")).willReturn(Optional.of(new Order("o-1")));
        this.service.place("o-1");
        then(this.orders).should().save(any(Order.class));
    }
}
```

**Listing 1.** Conceptual Mockito **5** / JUnit **5** unit test. **No** `@SpringBootTest`. Constructor injection is equivalent to `@InjectMocks`.

```java
@SpringJUnitConfig(ServiceTestConfig.class)
class OrderServiceSpringTests {

    @Autowired OrderService service;
    @MockitoBean OrderRepository orders;

    @Test
    void placesOrderWhenStockExists() {
        given(this.orders.findById("o-1")).willReturn(Optional.of(new Order("o-1")));
        this.service.place("o-1");
    }
}
```

**Listing 2.** Conceptual Framework **7** bean override. Use this when **`ServiceTestConfig`** includes **`@EnableMethodSecurity` / `@EnableTransactionManagement`**. Boot equivalent: **`@SpringBootTest(classes = ServiceTestConfig.class, webEnvironment = NONE)`**.

```d2
direction: down
unit: "@Mock + new/@InjectMocks\nno ApplicationContext" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
aop: "@MockitoBean collaborators\nnarrow Spring context" {
  width: 300
  height: 50
  style.fill: "#fff3e0"
}
full: "@SpringBootTest full app\nslow default" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}

unit -> aop: "need proxy"
aop -> full: "need auto-config"
```

**Fig. 1.** Escalate only when the behavior under test **is** the interceptor. `@MockitoBean` on the **service** skips that interceptor.

> [!warning] `@MockBean` is gone in Boot 4
> Dump samples that stub repos with **`@MockBean`** do not compile. Use **`@MockitoBean`**. **`@Mock`** never registers a Spring bean.

> [!warning] `@SpringBootTest` on every service test
> Default **`MOCK`** web context still refreshes **auto-config**. Context cache helps only **identical** keys. A Mockito unit test pays **zero** refresh.

> [!warning] `@InjectMocks` does not fail closed
> If constructor injection does not match, Mockito **leaves the field null** and the NPE is yours. `@MockitoBean` on a **prototype** still yields a **singleton mock**.

> [!tip] Interview answer
> **Unit-test a `@Service` with Mockito — `new` plus mocked repos.** Bring Spring only to prove **AOP** (transactions, `@PreAuthorize`, validation). Then **`@MockitoBean` the repository, not the service.** Do not start `@SpringBootTest` for arithmetic.
