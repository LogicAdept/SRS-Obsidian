<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Testing/Mocking #Java/Annotations #SRS

# What is the RestClientTest annotation?

> [!abstract] Short answer
> **`@RestClientTest`** (module **`spring-boot-restclient-test`**, package **`org.springframework.boot.restclient.test.autoconfigure`**) is Boot’s **outbound HTTP-client slice**. It focuses on beans that use **`RestTemplateBuilder` or `RestClient.Builder`**, auto-configures Jackson/Gson/Jsonb plus those builders, and installs **`MockRestServiceServer`**. Name the client with **`value` / `components`**. Regular **`@Component` is not scanned**. It does **not** hit **your** `@RestController`. **`WebClient`** is **`@WebClientTest`** — **`MockRestServiceServer` does not bind `WebClient`**.

## Stub the factory, not the controller

`expect(requestTo(…)).andRespond(withSuccess(…))`, then **`verify()`**. If production used **`RestTemplateBuilder.baseUri`**, **omit** that prefix from **`requestTo`**. With **`RestClient.Builder`** (or no `baseUri`), match the **full URI**. Several builders: **`@AutoConfigureMockRestServiceServer`** is for **one** template/builder; otherwise **`MockServerRestClientCustomizer.getServer(…)`**. Jackson scan: **`@JacksonComponent`** (`@JsonComponent` deprecated). How-to: [[How do you mock external HTTP APIs in Spring tests]]. Inbound tests: [[What is the WebMvcTest annotation]], [[What is WebTestClient]]. Family: [[What are Spring Boot test slices]]. Full app: [[What is SpringBootTest]].

```java
@RestClientTest(RemoteVehicleDetailsService.class)
class MyRestTemplateServiceTests {

    @Autowired RemoteVehicleDetailsService service;
    @Autowired MockRestServiceServer server;

    @Test
    void getVehicleDetailsWhenResultIsSuccessShouldReturnDetails() {
        this.server.expect(requestTo("/greet/details"))
                .andRespond(withSuccess("hello", MediaType.TEXT_PLAIN));
        assertThat(this.service.callRestService()).isEqualTo("hello");
    }
}
```

**Listing 1.** Conceptual Boot **4.1**. Path-only matcher because the sample builder set **`baseUri`**.

```java
@RestClientTest(YourClient.class)
@AutoConfigureMockRestServiceServer(enabled = true)
class TunedClientTests { }
```

**Listing 2.** Conceptual: extra control when a **single** `RestClient.Builder` / `RestTemplateBuilder` is in play.

```d2
direction: down
slice: "@RestClientTest(YourClient)" {
  width: 280
  height: 40
  style.fill: "#e3f2fd"
}
mock: "MockRestServiceServer" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}
svc: "YourClient via RestClient/RestTemplate" {
  width: 320
  height: 45
  style.fill: "#e8f5e9"
}
ctrl: "@RestController\n(not in this slice)" {
  width: 260
  height: 45
  style.fill: "#ffebee"
}

slice -> mock -> svc
slice -> ctrl
```

**Fig. 1.** Outbound stub. Controllers stay on **`@WebMvcTest`**.

> [!warning] Not `@WebMvcTest`
> This slice **never** starts MockMvc against your mappings. A green `@RestClientTest` does not prove `/api` on **your** server.

> [!warning] Not `WebClient`
> **`@WebClientTest`** (`spring-boot-webclient-test`) configures **`WebClient.Builder`**. Point that client at a **mock HTTP server** (MockWebServer / WireMock).

> [!warning] One `MockRestServiceServer` bean
> Multiple `RestClient.Builder`s need **`MockServerRestClientCustomizer`**, not a single autowired server. Leftover expectations fail **`verify()`**.

> [!tip] Interview answer
> **`@RestClientTest` tests your outbound `RestClient` / `RestTemplate` client with `MockRestServiceServer`.** Specify the client class. It is not a controller test and not `WebClient`.
