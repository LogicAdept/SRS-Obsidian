<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Java/Spring/Framework/WebMvc #Testing/Mocking #Java/Annotations #SRS

# How do you test a Spring MVC controller in isolation?

> [!abstract] Short answer
> Two official setups. **Boot slice:** **`@WebMvcTest(YourController.class)`** (`spring-boot-webmvc-test`) loads **MVC only** (no `@Service` / `@Repository` / DB), auto-configures **MockMvc** / **MockMvcTester**, and you replace collaborators with **`@MockitoBean`**. **Framework standalone:** **`MockMvcBuilders.standaloneSetup(controller)`** — instantiate the controller, inject mocks yourself, **no** Spring MVC config loaded. Neither starts a servlet container. JUnit **4** still needs **`@RunWith(SpringRunner.class)`**; Boot **4.1** / JUnit **6** does not. **`@MockBean`** was removed in Boot **4** (deprecated **3.4** → **`@MockitoBean`**). There is **no `secure` attribute** on `@WebMvcTest`.

## Slice vs standalone

`@WebMvcTest` scans `@Controller`, `@ControllerAdvice`, converters, filters, interceptors, `WebMvcConfigurer`, `SecurityFilterChain`, … — **not** regular `@Component`. Limit with **`controllers` / `value`**. Stub the constructor collaborator with **`@MockitoBean`** (or `@Import`). Drive HTTP with **`MockMvcTester`** (AssertJ, Boot 4 samples) or **`mockMvc.perform(get(…)).andExpect(…)`** (`jsonPath`, status). Full app + MockMvc: **`@SpringBootTest` + `@AutoConfigureMockMvc`**.

Framework *Setup Options*: **`WebApplicationContext`** MockMvc (what `@WebMvcTest` uses) hits **your real MVC config** and caches the context. **`standaloneSetup`** is closer to a unit test: one controller, manual mocks, **you must still write integration tests** if you skip WAC. Override services with **`@MockitoBean` or `@TestBean`**.

Security on the classpath: `@WebMvcTest` **auto-configures Spring Security**. Unauthenticated calls are **401 / 302**, not a free pass. Use **`@WithMockUser`**, not a removed `secure = false`. Slice: [[What is the WebMvcTest annotation]]. MockMvc: [[What is MockMvc]]. Mocks: [[What is the difference between MockitoBean and MockBean]]. Security: [[What is the purpose of WithMockUser in Spring Security tests]].

```java
@WebMvcTest(UserVehicleController.class)
class MyControllerTests {

    @Autowired MockMvcTester mvc;
    @MockitoBean UserVehicleService userVehicleService;

    @Test
    void testExample() {
        given(this.userVehicleService.getVehicleDetails("sboot"))
                .willReturn(new VehicleDetails("Honda", "Civic"));
        assertThat(this.mvc.get().uri("/sboot/vehicle").accept(MediaType.TEXT_PLAIN))
                .hasStatusOk()
                .hasBodyTextEqualTo("Honda Civic");
    }
}
```

**Listing 1.** Conceptual Boot **4.1** slice. Hamcrest equivalent: `mockMvc.perform(get("/sboot/vehicle")).andExpect(status().isOk())`. JSON: **`jsonPath`**, not a required **JSONAssert** library.

```java
MockMvc mvc = MockMvcBuilders.standaloneSetup(new SurveyController(mockService)).build();
```

**Listing 2.** Conceptual Framework **standalone** setup: no Boot slice, no `@WebMvcTest` filters. Does **not** prove `WebMvcConfigurer` / Security wiring.

```d2
direction: down
slice: "@WebMvcTest(Controller)\nWAC + MockMvc + @MockitoBean" {
  width: 340
  height: 55
  style.fill: "#e3f2fd"
}
stand: "standaloneSetup(controller)\nno Spring MVC config" {
  width: 300
  height: 50
  style.fill: "#fff3e0"
}
http: "No embedded Tomcat" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}

slice -> http
stand -> http
```

**Fig. 1.** Isolation means **no full Boot context and no real port**. The slice still loads **MVC + Security** beans; standalone loads **neither**.

> [!warning] `secure = false` is gone
> `@WebMvcTest` has **`controllers` / `value`**, not `secure`. Dump samples that disable Security that way **do not compile** on current Boot.

> [!warning] `@MockBean` is not Boot 4
> Replaced by **`@MockitoBean`**. `@RunWith(SpringRunner.class)` is **JUnit 4 only**.

> [!warning] Security still runs in the slice
> A green test without a user often means you never hit a protected matcher — or you got **401**. Use **`@WithMockUser`**. `@Service` is **missing** unless mocked: the controller constructor fails to wire.

> [!tip] Interview answer
> **`@WebMvcTest(TheController.class)`, `@MockitoBean` the service, `MockMvc` or `MockMvcTester` for the request.** That is the web-layer slice, not the database. For a no-Spring unit test, `standaloneSetup`. Do not use `secure = false` or `@MockBean` on Boot 4.
