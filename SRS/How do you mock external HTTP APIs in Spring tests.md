<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Testing/Mocking #Java/Testing/WireMock #SRS

# How do you mock external HTTP APIs in Spring tests?

> [!abstract] Short answer
> For **`RestClient` / `RestTemplate`**: Boot **`@RestClientTest`** (module **`spring-boot-restclient-test`**) auto-configures **`MockRestServiceServer`**. Call **`expect(requestTo(…)).andRespond(withSuccess(…))`**, then **`verify()`**. Framework also recommends a **real mock HTTP server** (OkHttp **MockWebServer** or **WireMock**) so the production client still does network I/O. **`WebClient`** is **`@WebClientTest`** + a mock server — **`MockRestServiceServer` does not bind `WebClient`**. **`@MockitoBean` on the client** stubs Java methods and **skips** HTTP. This is **not** **`WebTestClient`**, which hits **your** app.

## Stub the client’s request factory, or listen on a port

Framework *Testing Client Applications*: **`MockRestServiceServer`** replaces the **`ClientHttpRequestFactory`** on **`RestClient` / `RestTemplate`** (`bindTo(builder)` / `bindTo(restTemplate)`). Expectations are **in declaration order** unless **`ignoreExpectOrder(true)`**. Each request matches **once** unless you pass **`ExpectedCount`** (`times(2)`, …). **`verify()`** fails if leftovers remain.

That path **predates** mock web servers. Official recommendation **now**: MockWebServer or WireMock for **transport-level** behavior. **`@RestClientTest(YourClient.class)`** still wires **`MockRestServiceServer`** for the slice. Specify **`components` / `value`**. Regular `@Component` is **not** scanned. If **`RestTemplateBuilder.baseUri`** was used, **omit** the base from **`requestTo`**. With **`RestClient.Builder`** (or no `baseUri`), match the **full URI**.

Several builders: **`@AutoConfigureMockRestServiceServer`** is for **one** `RestTemplate` / `RestClient.Builder`. Otherwise inject **`MockServerRestClientCustomizer`** / **`MockServerRestTemplateCustomizer`** and **`getServer(…)`**.

`@WebClientTest` (Boot **4**, **`spring-boot-webclient-test`**) focuses on **`WebClient.Builder`** beans. It does **not** install **`MockRestServiceServer`**. Point `WebClient` at a mock server URL (or a test `ExchangeFunction`). Slice: [[What is the RestClientTest annotation]]. Your app’s HTTP API: [[What is WebTestClient]]. Full context: [[What is SpringBootTest]]. Bean stubs: [[What is the difference between MockitoBean and MockBean]].

```java
@RestClientTest(RemoteVehicleDetailsService.class)
class RemoteVehicleDetailsServiceTests {

    @Autowired RemoteVehicleDetailsService service;
    @Autowired MockRestServiceServer server;

    @Test
    void getVehicleDetailsWhenResultIsSuccessShouldReturnDetails() {
        this.server.expect(requestTo("/greet/details"))
                .andRespond(withSuccess("hello", MediaType.TEXT_PLAIN));
        assertThat(this.service.callRestService()).isEqualTo("hello");
        this.server.verify();
    }
}
```

**Listing 1.** Conceptual Boot **4.1** `@RestClientTest` sample (path-only matcher because the production builder used **`baseUri`**). Without `baseUri`, the matcher must include scheme and host.

```d2
direction: down
app: "Your service\nRestClient / RestTemplate" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
mrs: "MockRestServiceServer\ncustom ClientHttpRequestFactory" {
  width: 320
  height: 55
  style.fill: "#fff3e0"
}
tcp: "MockWebServer / WireMock\nreal HTTP on a port" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}

app -> mrs: "no TCP"
app -> tcp: "same client I/O"
```

**Fig. 1.** Factory stub vs a listen-port fake. **`WebClient` uses the right-hand path** (or a mock `ExchangeFunction`), not `MockRestServiceServer`.

> [!warning] `MockRestServiceServer` is not `WebClient`
> It wraps **`RestClient` / `RestTemplate`**. A `@Bean WebClient` still talks to the network unless you change its base URL or connector.

> [!warning] `@MockitoBean RestClient` is not an HTTP mock
> You never exercise URI building, converters, or error status handling. Use it when the test must not care about HTTP.

> [!warning] `WebTestClient` tests your controllers
> Auto-configured MockMvc/`WebTestClient` is **inbound** to this app. Vendor APIs need **`@RestClientTest`** or a mock server in front of **your outbound client**.

> [!warning] One auto-configured `MockRestServiceServer` per slice
> Two `RestClient.Builder` beans: the single server bean is the wrong tool. Use the **customizer** `getServer` methods, or bind **`MockRestServiceServer`** yourself.

> [!tip] Interview answer
> **`@RestClientTest` plus `MockRestServiceServer.expect(…).andRespond(…)` and `verify()`.** That stubs `RestClient`/`RestTemplate` without opening a port. For `WebClient` or real I/O quirks, use MockWebServer or WireMock. Do not confuse that with `WebTestClient`, which calls **your** HTTP API.
