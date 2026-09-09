<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# How does the Quarkus REST client work?

> [!abstract] Short answer
> You declare an **interface** annotated with `@RegisterRestClient` whose methods carry Jakarta REST annotations (`@GET`, `@Path`, `@QueryParam`, ...); Quarkus **generates the implementation at build time** (MicroProfile REST Client, backed by the reactive HTTP stack), so the interface is injectable with `@Inject @RestClient`. Base URL, timeouts and per-key overrides are configuration: `quarkus.rest-client.<configKey>.*` or `quarkus.rest-client."fully.qualified.InterfaceName".*`. It is reactive under the hood — methods may also return `Uni` — and it participates in native builds without extra metadata.

## Declaration, injection, configuration

The build-time generation is the Quarkus-specific part: where plain MicroProfile implementations build clients dynamically at runtime, Quarkus reads the interface during augmentation, records the client machinery, and the container wires an instance into your injection points ([[What happens at build time in Quarkus]]). `configKey` selects which `quarkus.rest-client.<key>.*` stanza applies — `url`, `connect-timeout`, `read-timeout`, scope, proxy settings — keeping environments swappable without code changes; the fallback key is the fully qualified interface name. Response bodies map through JSON-B or Jackson depending on the installed `quarkus-rest-client-jackson`/`-jsonb` extension. Error handling supports `ResponseExceptionMapper`s — a 4xx/5xx becomes a typed exception your service can translate.

```java
// src/main/java/org/acme/check/res/EchoClient.java (JDK 21, Quarkus 3.39.2, mvn test: 6/6 green)
package org.acme.check.res;

import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.QueryParam;
import org.eclipse.microprofile.rest.client.inject.RegisterRestClient;

@RegisterRestClient(baseUri = "http://localhost:8081")
public interface EchoClient {
    @GET
    @Path("/echo")
    String echo(@QueryParam("q") String q);
}
// Injected into a resource:
//   @Inject @RestClient EchoClient echo;
//   @GET @Path("/echo") public String echo(@QueryParam("q") String q) { return echo.echo(q); }
// Test request (verbatim): GET /demo/echo?q=ping -> 200 body "echo:ping"
// The client called the app's own endpoint over HTTP; no implementation class was ever written.
```

**Listing 1.** The whole client is one interface: generated implementation, injected proxy, real HTTP call verified in the test run ([[How do you test a Quarkus application]]).

```d2
direction: down
itf: "Interface\n@RegisterRestClient + Jakarta REST annotations" {
  width: 360
  height: 65
}
aug: "Augmentation\ngenerates implementation,\nbinds config key" {
  width: 300
  height: 65
  style.fill: "#fff3e0"
}
inj: "@Inject @RestClient\nCDI injection point" {
  width: 250
  height: 55
  style.fill: "#e8f5e9"
}
cfg: "quarkus.rest-client.<key>.url\ntimeouts, proxy, scope" {
  width: 300
  height: 60
  style.fill: "#e3f2fd"
}
http: "Reactive HTTP client\non Vert.x/Netty stack" {
  width: 290
  height: 55
}
itf -> aug -> inj
cfg -> aug: "resolved per config key"
inj -> http
```

**Fig. 1.** Configuration feeds the generated implementation, not the interface; swapping environments is a property change ([[How do you configure a Quarkus application]]).

## The follow-up questions

Reactive: the same interface can declare `Uni<String> echo(...)` — the call is then non-blocking and composes with Mutiny pipelines ([[What is Mutiny in Quarkus]]). Multipart, headers via `@ClientHeaderParam`, request filters and TLS registry options are all documented extensions of the interface model. Testing without a real target: point the config key at a stub server (or Dev Service) — the interface never changes.

> [!warning] "The REST client calls REST" — say what happens on failure too
> Default behavior on a non-2xx response: the built-in mapper throws a `WebApplicationException`-family error unless you register a `ResponseExceptionMapper` — code that assumes retries or graceful degradation gets neither. Two further traps: timeouts default generously and must be set per client for real SLAs (`connect-timeout`/`read-timeout`), and forgetting the `@RestClient` qualifier produces a confusing "no bean found" — the generated implementation is qualified, plain `@Inject EchoClient` does not select it.

> [!tip] Interview answer
> The Quarkus REST client is MicroProfile's typed client: I write an interface with Jakarta REST annotations and @RegisterRestClient, Quarkus generates the implementation at build time on its reactive stack, and I inject it with @RestClient. Base URL and timeouts come from quarkus.rest-client.<configKey> config, methods can return Uni for non-blocking composition, errors map through ResponseExceptionMappers. It's declarative — no client code to write — and native-image safe because everything is resolved during augmentation.
