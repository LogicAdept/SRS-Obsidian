<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Java/Annotations #SRS

# What are Spring Boot test slices?

> [!abstract] Short answer
> A **slice** is a `@…Test` annotation that loads **only the auto-config and bean types for one layer**. Boot **4.1** ships them as focused **`-test` modules** (`spring-boot-webmvc-test` → **`@WebMvcTest`**, `spring-boot-data-jpa-test` → **`@DataJpaTest`**, plus **`@JsonTest`**, **`@RestClientTest`**, **`@JdbcTest`**, **`@WebFluxTest`**, **`@WebClientTest`**, …). Regular **`@Component` / `@Service` / `@ConfigurationProperties` are not scanned** (add **`@MockitoBean`**, **`@Import`**, or **`@EnableConfigurationProperties`**). **`@SpringBootTest` is not a slice** — it runs **full** `SpringApplication` auto-config. **Two `@…Test` annotations on one class are not supported**; pick one and add the other slice’s **`@AutoConfigure…`**.

## Restricted scan, restricted auto-config

Each slice **restricts component scan** and imports a **short** auto-config list (appendix *Test Slices*). **`excludeAutoConfiguration`** (or **`@ImportAutoConfiguration(exclude=…)`**) drops one of those classes. You can hang **`@AutoConfigure…`** on **`@SpringBootTest`** when you want test beans **without** slicing.

Interview set:

| Annotation | What it keeps | Typical driver |
| --- | --- | --- |
| **`@WebMvcTest`** | `@Controller` / advice / MVC / **SecurityFilterChain** | **MockMvc** / **MockMvcTester** |
| **`@DataJpaTest`** | `@Entity` + Spring Data JPA repos; **embedded DB**; **`@Transactional` rollback** | **`TestEntityManager`** |
| **`@JdbcTest`** | **`DataSource` + `JdbcTemplate`**, no Spring Data | SQL / `JdbcTemplate` |
| **`@JsonTest`** | JSON mapper + **`JacksonTester`** | serialize / `isEqualToJson` |
| **`@RestClientTest`** | `RestClient` / `RestTemplate` builders | **`MockRestServiceServer`** |
| **`@WebFluxTest`** | WebFlux `@Controller` | **`WebTestClient`** (no server) |

`@WebMvcTest` **does auto-configure Spring Security** when Security is on the classpath — not an optional `secure` flag. Collaborators: **`@MockitoBean`** (Boot **4** **removed `@MockBean`**). MVC: [[What is the WebMvcTest annotation]]. JPA: [[What is the DataJpaTest annotation]]. Full app: [[What is SpringBootTest]]. JSON: [[What is the JsonTest annotation]]. HTTP client: [[What is the RestClientTest annotation]].

```java
@WebMvcTest(UserVehicleController.class)
class MyControllerTests {
    @Autowired MockMvcTester mvc;
    @MockitoBean UserVehicleService userVehicleService;
}
```

**Listing 1.** Conceptual Boot **4.1** web slice. No `@Repository`, no embedded server.

```java
@DataJpaTest
class MyRepositoryTests {
    @Autowired TestEntityManager entityManager;
    @Autowired UserRepository repository;
}
```

**Listing 2.** Conceptual JPA slice. Default in-memory `DataSource` and method rollback. **`@AutoConfigureTestDatabase(replace = NONE)`** keeps the app DB.

```d2
direction: down
full: "@SpringBootTest\nall auto-config" {
  width: 260
  height: 45
  style.fill: "#ffebee"
}
mvc: "@WebMvcTest\ncontrollers + MockMvc" {
  width: 260
  height: 45
  style.fill: "#e3f2fd"
}
jpa: "@DataJpaTest\nentities + repos" {
  width: 260
  height: 45
  style.fill: "#fff3e0"
}
json: "@JsonTest / @RestClientTest\n…" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}

full -> mvc: "too much for MVC-only"
full -> jpa: "too much for a query"
full -> json
```

**Fig. 1.** A slice is still an **`ApplicationContext`** (and is **cached**). It is **not** Mockito-only `new`. Combining **`@WebMvcTest` + `@DataJpaTest`** on one class is **unsupported**.

> [!warning] `@ComponentScan` on `@SpringBootApplication` breaks slices
> An explicit scan can **disable the slice exclude filters**, so `@DataJpaTest` suddenly loads **the whole app**. Keep default scanning or move the custom scan off the application class.

> [!warning] `@Configuration` `@Bean` types are not filtered by stereotype
> A mixed config with **`SecurityFilterChain` and a `DataSource`** may be **invisible** to `@WebMvcTest` until **`@Import`**. Split those configs. **`@ConfigurationProperties` need `@EnableConfigurationProperties`.**

> [!warning] Two slice annotations do not stack
> Use **one** `@…Test` and import the other slice’s **`@AutoConfigure…`**. `@MockBean` dump samples **do not compile** on Boot **4**.

> [!tip] Interview answer
> **Slices load one layer: `@WebMvcTest` for controllers, `@DataJpaTest` for repositories.** They skip `@Service` unless you mock or import it. **`@SpringBootTest` is the full context** when you need wiring across layers. Do not put two `@…Test` annotations on the same class.
