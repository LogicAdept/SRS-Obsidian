<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Java/Spring/Framework/WebMvc #Testing/Mocking #Java/Annotations #SRS

# What is the WebMvcTest annotation?

> [!abstract] Short answer
> **`@WebMvcTest`** is Boot’s **MVC test slice** (module **`spring-boot-webmvc-test`**, package **`org.springframework.boot.webmvc.test.autoconfigure`**). It enables **MVC-relevant auto-config only**, scans **`@Controller` / `@ControllerAdvice`**, converters, filters, interceptors, **`WebMvcConfigurer`**, **`SecurityFilterChain`**, … — **not** regular **`@Component` / `@Service` / `@Repository` / DB**. It **auto-configures `MockMvc`** and, with AssertJ, **`MockMvcTester`**. Limit the set with **`controllers` / `value`**. Stub constructor collaborators with **`@MockitoBean`** or **`@Import`**. **`@MockBean` is gone in Boot 4.** There is **no `secure` attribute**. Security on the classpath is **auto-configured**, not skipped.

## Web layer only, in-process HTTP

Boot’s *Auto-configured Spring MVC Tests*: you want URL mapping **without** database calls. Full app + MockMvc is **`@SpringBootTest` + `@AutoConfigureMockMvc`**, not this annotation. JUnit **4** still needs **`@RunWith(SpringRunner.class)`**; Boot **4.1** / JUnit **6** already meta-annotates **`SpringExtension`**.

Unauthenticated MockMvc against a secured matcher is **401** or **302**, not a free pass. Use **`@WithMockUser`**. A `@Bean` `SecurityFilterChain` on a mixed `@Configuration` the slice **does not scan** is **missing** until **`@Import`**. **`@ConfigurationProperties`** need **`@EnableConfigurationProperties`**. Two `@…Test` annotations on one class are **unsupported**.

How to drive it: [[How do you test a Spring MVC controller in isolation]]. Full context: [[What is SpringBootTest]]. Family: [[What are Spring Boot test slices]]. MockMvc API: [[What is MockMvc]]. Mocks: [[What is the difference between MockitoBean and MockBean]]. Security: [[How do you test Spring Security in MockMvc tests]].

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

**Listing 1.** Conceptual Boot **4.1** sample. Hamcrest: `mockMvc.perform(get("/sboot/vehicle")).andExpect(status().isOk())`. Empty `@WebMvcTest` (no `controllers`) registers **all** `@Controller` beans.

```java
@SpringBootTest
@AutoConfigureMockMvc
class FullContextMockMvcTests { }
```

**Listing 2.** Conceptual: **not** a slice — whole auto-config, still no listen port unless **`RANDOM_PORT`**.

```d2
direction: down
slice: "@WebMvcTest(Controller)" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
keep: "@Controller, advice, MVC, SecurityFilterChain" {
  width: 340
  height: 50
  style.fill: "#fff3e0"
}
drop: "@Service / @Repository / DataSource" {
  width: 300
  height: 45
  style.fill: "#ffebee"
}
mvc: "MockMvc / MockMvcTester" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}

slice -> keep -> mvc
slice -> drop
```

**Fig. 1.** No Tomcat. Filters registered with MockMvc still run (`addFilters` defaults **true**). Servlet **error pages** need a real server.

> [!warning] `secure = false` does not compile
> Current `@WebMvcTest` has **`controllers`**, **`properties`**, **`excludeAutoConfiguration`** — not **`secure`**. Do not disable the chain to green the test.

> [!warning] `@MockBean` is not Boot 4
> Use **`@MockitoBean`**. Missing it, the controller **constructor fails to wire** because `@Service` was never scanned.

> [!warning] Security is on in the slice
> Unauthenticated calls **401 / 302**. **`@WithMockUser`** (or `.with(user(…))`), plus **`csrf()`** on POST.

> [!tip] Interview answer
> **`@WebMvcTest(TheController.class)` is the MVC slice: MockMvc, no database, no `@Service` unless mocked.** `@MockitoBean` the collaborator. Security stays enabled — there is no `secure = false`. For the whole app, `@SpringBootTest` + `@AutoConfigureMockMvc`.
