<!--
reps: 0
priority: 0
-->
#Java/Testing/WireMock #SRS

# How would you explain WireMock

> [!abstract] Short answer
> **WireMock is an HTTP mock server embedded in your tests: it starts a real HTTP endpoint, you register stubs — URL/method/headers in, status/headers/body out — and every request is journaled for later verification.** It replaces third-party HTTP dependencies with deterministic answers, including failures and delays.

## A real server on a random port

WireMock is not a fake object — it binds an actual socket, so anything that speaks HTTP (your service, `HttpClient`, a browser) hits it. Stubs are registered per test: first matching stub wins, otherwise the server answers 404.

```d2
direction: right
test: "Test starts\nWireMockServer" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
stub: "stubFor(get(\"/api/rates\")\n-> 200 okJson)" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
svc: "Service under test\ngets the base URL" {
  width: 250
  height: 80
  style.fill: "#fff3e0"
}
journal: "Every request recorded\n-> verify afterwards" {
  width: 270
  height: 80
  style.fill: "#e8f5e9"
}
test -> stub
test -> svc
svc -> journal: "HTTP GET"
stub -> journal
```

**Fig. 1.** The test configures the server, the service calls it over real HTTP, and the journal keeps the evidence.

```java
WireMockServer wm = new WireMockServer(WireMockConfiguration.wireMockConfig().dynamicPort());
wm.start();
configureFor(wm.port());

stubFor(get(urlEqualTo("/api/rates"))
        .willReturn(okJson("{\"USD\":90.5}")));
stubFor(get(urlEqualTo("/api/broken"))
        .willReturn(serverError()));
stubFor(get(urlEqualTo("/api/slow"))
        .willReturn(aResponse().withFixedDelay(2000).withBody("late")));

HttpClient client = HttpClient.newHttpClient();
System.out.println("rates : " + send(client, wm.baseUrl() + "/api/rates"));
System.out.println("broken: " + send(client, wm.baseUrl() + "/api/broken"));
long t0 = System.nanoTime();
send(client, wm.baseUrl() + "/api/slow");
System.out.println("slow  : " + ((System.nanoTime() - t0) / 1_000_000) + " ms, body=late");
wm.stop();
```

**Listing 1.** Three stubs: success, server error, and a 2-second lag. Run on JDK 21 against WireMock 3.3.1:

```java
rates : 200 {"USD":90.5}
broken: 500
slow  : 2005 ms, body=late
```

**Listing 2.** The service saw genuine HTTP responses: a JSON body, a 500, and a response that arrived after the delay — nothing was staged in-process.

## Why tests need it

Calling a real exchange-rate API from CI makes the test flaky: rate limits, downtime, changing data. WireMock removes the network gamble: responses are fixed, so assertions are stable, and the failure modes the happy path never shows — 500s, timeouts, malformed JSON, slow answers — are one stub each. Retry logic, circuit breakers and fallback branches get their own deterministic tests instead of waiting for the world to misbehave. The same idea exists in the Spring stack — [[How do you mock external HTTP APIs in Spring tests]] shows the Spring-side wiring, and [[What is the difference between hard and soft assertions]] helps when several response fields are checked at once.

> [!warning] WireMock mocks HTTP, not your business logic
> A stub returns what you told it regardless of what a real API would do, so a green test proves your code handles the response you assumed — not that the assumption matches the vendor's contract. Keep the stub shapes in sync with the real API (contract tests or recorded responses help), and do not stub everything: WireMock answers 404 for unmatched requests, which can silently turn into a green test asserting on an error branch you never meant to exercise. Also mind the two distinct roles — stubbing answers versus checking requests — covered in [[What is the difference between stubbing and verifying in WireMock]].

In JUnit 5 the server is managed by an extension (`@WireMockTest` or the WireMock JUnit Jupiter support) that starts and stops it per test — the lifecycle idea matches [[What are the @BeforeAll and @AfterAll annotations in JUnit]].

> [!tip] Interview answer
> **WireMock is an embeddable HTTP mock server. You register stubs — match on URL, method, headers, body — and it serves fixed responses over a real socket, so the code under test does genuine HTTP. It also records every request, so you can verify what was sent, and it can simulate failures, delays and stateful sequences. Tests become deterministic and independent of third-party APIs, which is exactly what CI needs.**

