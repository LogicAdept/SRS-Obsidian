<!--
reps: 0
priority: 0
-->
#Java/Testing/WireMock #SRS

# What is the difference between stubbing and verifying in WireMock

> [!abstract] Short answer
> **Stubbing configures what WireMock answers when a request matches a pattern; verifying checks afterwards which requests actually arrived.** Stubbing happens before the action (`stubFor(get(...).willReturn(...))`), verifying after it (`verify(getRequestedFor(...))`) — both use the same request-matching builder, but they answer different questions: "what should I return?" versus "was I called, and how often, with what?"

## Stub first, act, verify last

Both directions use one request-matching DSL: `urlEqualTo`, `matching`, `withHeader(..., equalTo(...))`. On the stub side the pattern selects the canned response; on the verify side it filters the request journal — an in-memory log of everything the server received since the last reset.

```d2
direction: right
s: "stubFor(\nget(\"/api/rates\")\n.withHeader(...)\nwillReturn(okJson))" {
  width: 300
  height: 130
  style.fill: "#fff3e0"
}
act: "Service under test\nsends real HTTP requests" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
j: "Request journal\n(every received request)" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
v: "verify(1, getRequestedFor(\nurlEqualTo(\"/api/rates\")\n.withHeader(...)))" {
  width: 310
  height: 130
  style.fill: "#e8f5e9"
}
s -> act: "matched -> stub answer"
act -> j
j -> v
```

**Fig. 1.** Stubbing points forward (pattern → response); verification points backward (pattern → journal entries).

```java
stubFor(get(urlEqualTo("/api/rates"))
        .withHeader("X-Api-Key", equalTo("secret"))
        .willReturn(okJson("{\"USD\":90.5}")));

HttpRequest req = HttpRequest.newBuilder(URI.create(wm.baseUrl() + "/api/rates"))
        .header("X-Api-Key", "secret").build();
HttpResponse<String> r = client.send(req, HttpResponse.BodyHandlers.ofString());
System.out.println("stub answered: " + r.statusCode() + " " + r.body());

verify(1, getRequestedFor(urlEqualTo("/api/rates"))
        .withHeader("X-Api-Key", equalTo("secret")));
System.out.println("verify passed: 1 request with X-Api-Key=secret");
```

**Listing 1.** Verified on JDK 21 with WireMock 3.3.1:

```java
stub answered: 200 {"USD":90.5}
verify passed: 1 request with X-Api-Key=secret
```

**Listing 2.** The count mode (`1`) and the header predicate are the same idea as Mockito's `times` and argument matchers.

## What failing verification shows

A failed verification throws `VerificationException` and prints the pattern plus how many journal entries matched — the "nobody called me the way I expected" message. This is the check for contracts like "the client sent the API key" or "the webhook was delivered exactly once", which pure response stubbing cannot prove.

```java
try {
    verify(3, getRequestedFor(urlEqualTo("/api/rates")));
} catch (Throwable e) {
    System.out.println(e.getClass().getSimpleName());
    System.out.println(e.getMessage().trim().lines().limit(4).toList());
}
// VerificationException
// [Expected exactly 3 requests matching the following pattern but received 1:,
//  {
//    "url" : "/api/rates",
//    "method" : "GET]
```

**Listing 3.** Same server, one request in the journal, three expected: the mismatch message names the counts.

> [!warning] Verifying is not re-stubbing and stubbing is not a check
> Two classic confusions. First: `stubFor(...)` never asserts anything — if the client calls a different URL, the stub just stays unused and the test can pass on a 404 you misread as success; only `verify` turns "expected a call" into a checked claim. Second: verification patterns must match how the request really arrived — an extra header in the pattern (`withHeader("X-Api-Key", ...)`) makes verify fail even when the stub answered fine, because the journal entry lacks that header. Count modes accept exact numbers and comparison operators (`lessThan`, `greaterThan`); default `verify(pattern)` means "at least once". Stateful retry scenarios are built from stubbing, not verification — see how sequences work with scenarios in [[How would you explain WireMock]] and the Mockito analogue in [[How would you explain verify]].

> [!tip] Interview answer
> **Stubbing teaches WireMock what to answer: pattern in, fixed response out, registered before the test action. Verifying checks the journal after: how many matching requests arrived and with what headers or body. Both share the same matching DSL, but stubbing shapes the world and verifying asserts on it. In interviews: stubbing is arrange, the HTTP call is act, verify is assert.**

