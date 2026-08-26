<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS

# Is WebClient thread-safe?

> [!abstract] Short answer
> **Share one built `WebClient`.** After **`build()`**, Spring documents the instance as **immutable**; concurrent `get()` / `post()` on that field is the intended use (Boot keeps it on the service). **`WebClient.Builder` is mutable and stateful** — do not treat the builder as a concurrent singleton you keep mutating. Spring’s explicit “safe for multiple threads” sentence is on **`RestClient`**, not on `WebClient`.

## Immutable client, mutable builder

Spring *WebClient Configuration*: **once built, a `WebClient` is immutable**. Changes go through **`mutate()`**, which copies settings onto a **new** builder and **`build()`s a second client**. The original keeps its filters.

```java
WebClient client1 = WebClient.builder()
        .filter(filterA).filter(filterB).build();

WebClient client2 = client1.mutate()
        .filter(filterC).filter(filterD).build();
// client1: A, B — client2: A, B, C, D
```

**Listing 1.** Conceptual Framework sample — `mutate()` does not edit `client1`.

Javadoc: **`WebClient.Builder` is a mutable builder**. Boot *Calling REST Services*: inject the auto-configured **prototype** `WebClient.Builder`, **`build()` once**, keep the **`WebClient`**. The builder is **stateful**: later `baseUrl(...)` on the **same** builder instance affects **later** `build()` calls. For two different clients from one builder, **`builder.clone()`**.

Boot’s `WebClient.Builder` bean is **`@Scope("prototype")`**: each injection point gets a **cloned** builder so one component’s `baseUrl` does not leak into another’s injection.

```java
@Service
public class MyService {

    private final WebClient webClient;

    public MyService(WebClient.Builder builder) {
        this.webClient = builder.baseUrl("https://example.org").build();
    }

    public Mono<Details> someRestCall(String name) {
        return this.webClient.get()
                .uri("/{name}/details", name)
                .retrieve()
                .bodyToMono(Details.class);
    }
}
```

**Listing 2.** Conceptual Boot pattern — one immutable client field, many overlapping `Mono`s. Client overview: [[What is WebClient]]. Wiring: [[How do you call an external API from a WebFlux application]].

```d2
direction: down
b: "WebClient.Builder\nmutable, prototype in Boot" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
c: "WebClient\nimmutable after build()" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
req: "Concurrent get/post\nReactor, shared Netty pool" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}

b -> c: "build() once"
c -> req
```

**Fig. 1.** Concurrency lives in **Reactor + the HTTP connector pool**, not in mutating the client object. Default Netty `HttpClient` shares **`HttpResources`** (loops + pool) across clients.

`.block()` on a `Mono` from `WebClient` is still a **blocking wait** — safe regarding *client* sharing, unsafe on the **event loop** — [[What happens if you call block on a WebFlux event loop]].

> [!warning] “Thread-safe because immutable” is dump shorthand
> Framework text is **immutable after `build()`**. **`RestClient`** is the client whose docs say **used safely by multiple threads**. Do not paste that sentence onto `WebClient` in an interview unless you also say what Spring actually wrote.

> [!warning] Do not share a long-lived mutating `Builder`
> `filters(list -> …)` sees a **live** list. Two threads calling `baseUrl` / `filter` on one builder race. Build **once** (or `clone()`), then share the **`WebClient`**.

> [!warning] `WebClient.create()` skips Boot’s builder
> No shared codecs / connector auto-config. Fine for samples; in Boot prefer the injected **`WebClient.Builder`**.

> [!tip] Interview answer
> **Yes — reuse one built `WebClient`; it is immutable.** Concurrent requests are normal. The **builder** is mutable: inject Boot’s prototype builder, `build()` in the constructor, keep the client. `mutate()` makes a **new** client. Spring’s “multiple threads” guarantee is documented for **`RestClient`**.
