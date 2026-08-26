<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Testing/Integration #SRS

# What is TestRestTemplate?

> [!abstract] Short answer
> **`TestRestTemplate`** (`org.springframework.boot.resttestclient`, module **`spring-boot-resttestclient`**) is Boot’s **test HTTP client** with a **`RestTemplate`-shaped API**. It is **fault-tolerant: 4xx and 5xx do not throw** — you read **`ResponseEntity` and the status**. It **does not extend `RestTemplate`** (`getRestTemplate()` if you need the real one). Against **`@SpringBootTest` + `RANDOM_PORT` / `DEFINED_PORT`**, add **`@AutoConfigureTestRestTemplate`** and **`@Autowired`** it; **relative URIs hit the embedded server**. Also needs **`spring-boot-restclient`** on the classpath.

## RestTemplate-shaped, test-friendly errors

Same verbs as production **`RestTemplate`**: **`getForObject`**, **`getForEntity`**, **`exchange`**, … Production `RestTemplate` with the default error handler **throws** on 4xx/5xx; this type **does not**, so a 404 test stays in the assertion. Optional **Basic** on the instance: constructor credentials or **`withBasicAuth(user, password)`** (new template). Apache **HttpClient 5.1+** is recommended; Boot then wires it.

Boot **4.1** running-server sample prefers **`RestTestClient`** + **`@AutoConfigureRestTestClient`** when you want **`expectStatus()`**. **`WebTestClient`** if you are on **WebFlux** (mock bind or live). **`TestRestTemplate`** is the blocking, entity-returning option. Modes: [[What is SpringBootTest WebEnvironment]]. Live HTTP: [[How do you test REST endpoints end to end]]. Port: [[What is LocalServerPort]]. Reactive test client: [[What is WebTestClient]]. In-process MVC: [[What is MockMvc]]. JSON body compare: [[What is JSONAssert]].

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureTestRestTemplate
class MyRandomPortTestRestTemplateTests {

    @Test
    void exampleTest(@Autowired TestRestTemplate restTemplate) {
        String body = restTemplate.getForObject("/", String.class);
        assertThat(body).isEqualTo("Hello World");
    }
}
```

**Listing 1.** Conceptual Boot **4.1**. No `http://localhost:` + port for relative URIs.

```java
ResponseEntity<String> response = this.template.getForEntity("/example", String.class);
assertThat(response.getStatusCode()).isEqualTo(HttpStatus.NOT_FOUND);
```

**Listing 2.** Conceptual test-utilities sample shape. A production **`RestTemplate`** would often have **thrown** already.

```d2
direction: down
t: "TestRestTemplate\ngetForEntity / exchange" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
http: "real HTTP\nRANDOM_PORT server" {
  width: 240
  height: 45
  style.fill: "#fff3e0"
}
mvc: "MockMvc\nno socket" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}

t -> http
```

**Fig. 1.** MockMvc never leaves the Spring MVC layer. This client does (when the server is real).

> [!warning] Not a `RestTemplate` subclass
> Do not `@Autowired RestTemplate` expecting this bean. Customize with a **`RestTemplateBuilder` `@Bean`**, not by subclassing.

> [!warning] Boot 4 does not auto-wire it from `@SpringBootTest` alone
> You need **`@AutoConfigureTestRestTemplate`**. Putting **`spring-boot-restclient` only on the test classpath** auto-configures **`RestClient.Builder`** in tests and can **diverge** from production — keep it on the **main** classpath if production uses that builder.

> [!warning] Different thread than the test
> **`@WithMockUser` does not** ride **`RANDOM_PORT`**. `@Transactional` on the test **does not** roll back the **server**’s work. Authenticate on the **request** (Basic / token).

> [!tip] Interview answer
> **`TestRestTemplate` is Boot’s RestTemplate for tests: 4xx/5xx become a `ResponseEntity`, not an exception.** Auto-configure it on `RANDOM_PORT` and use relative URIs. It is not MockMvc and not a production `RestTemplate` bean.
