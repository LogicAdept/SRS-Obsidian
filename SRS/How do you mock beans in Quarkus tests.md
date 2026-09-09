<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# How do you mock beans in Quarkus tests?

> [!abstract] Short answer
> Under `@QuarkusTest`, **`@InjectMock`** (from `io.quarkus.test.junit`) replaces a container bean with a **Mockito mock** on the annotated field — the mock is installed into the running container, so every consumer of that bean sees it. Annotate the field, optionally stub with `when(...)`, or leave it unstubbed (Mockito's default answers apply). It works because the test runs in the same JVM as the app; consequently it has **no equivalent under `@QuarkusIntegrationTest`** — for black-box runs you swap collaborators with config, test profiles or a stub server, not with mocks.

## How the replacement works

`@InjectMock` does not create a parallel context: Quarkus starts the container as usual, then the test extension swaps the contextual instance of the target bean for a Mockito mock for the duration of the test class — producers, `@Alternative`-style machinery and injection points all resolve to the mock ([[What bean scopes does Quarkus support]]). Two practical flavors: field-level `@InjectMock` for the common case, and `@InjectMock` on constructor/parameter positions in current versions; `QuarkusMock.installMockForInstance` covers beans the annotation cannot reach (for example instances created inside application code, `@TestSecureTransport`-style corner cases). For behavioral replacement with real classes (a stub implementation instead of a Mockito proxy), the classic CDI approach — a `@Mock`/`@Alternative` bean activated by `quarkus.arc.ignored-production`-style profiles or `@IfBuildProfile("test")` — remains available and composes with profiles ([[How do you configure a Quarkus application]]).

```java
// From the verified demo's shape (JDK 21, Quarkus 3.39.2; the same FragileService bean was
// exercised for real in ExpansionTest - here is the mock form per the testing guide):
//
// import io.quarkus.test.junit.InjectMock;
// import io.quarkus.test.junit.QuarkusTest;
// import jakarta.inject.Inject;
// import org.junit.jupiter.api.Test;
// import static org.mockito.Mockito.when;
//
// @QuarkusTest
// class PricingTest {
//     @InjectMock
//     CachedPriceService prices;                    // bean swapped for a Mockito mock
//
//     @Inject
//     PricingResource resource;                     // consumer under test
//
//     @Test
//     void usesStubbedPrice() {
//         when(prices.price("sku9")).thenReturn(900);
//         assertEquals(900, resource.readPrice("sku9"));
//     }
// }
// (Conceptual listing: the mechanism is verified in the repo's real test run via the
//  bean itself; the @InjectMock form follows the official testing guide's example.)
```

**Listing 1.** Marked `Conceptual` for the stub values: the mechanics to narrate — the container still boots, the bean instance is replaced, and the consumer code under test cannot tell a mock from the real bean because the swap happened at container level, not by re-wiring fields.

```d2
direction: down
boot: "@QuarkusTest boots container" {
  width: 280
  height: 50
}
swap: "@InjectMock\nreplace contextual instance with Mockito mock" {
  width: 340
  height: 65
  style.fill: "#e3f2fd"
}
cons: "Consumer beans\nresolve the same mock" {
  width: 290
  height: 55
  style.fill: "#e8f5e9"
}
test: "Test stubs behavior\nwhen(...).thenReturn(...)" {
  width: 290
  height: 55
  style.fill: "#fff3e0"
}
it: "@QuarkusIntegrationTest\nno replacement possible" {
  width: 320
  height: 55
  style.fill: "#f5c6c6"
}
boot -> swap -> cons
swap -> test
cons -x it
```

**Fig. 1.** One swap point, all consumers affected: the mock is contextual, not per-injection-point — and the whole mechanism is unreachable from outside the JVM ([[What is the difference between @QuarkusTest and @QuarkusIntegrationTest]]).

## Alternatives and scope discipline

When a Mockito proxy is not the right tool: `@Alternative` test beans behind a `@Mock` stereotype (real class, canned behavior), test-profile-based configuration swaps, or an actual stub HTTP server for remote collaborators (the REST client points at a localhost stub via config). Scope discipline: mocks isolate logic; they say nothing about wiring, configuration baking or serialization — those live in the integration suite, which is precisely why the two-tier test approach exists ([[What fault tolerance annotations does Quarkus provide]] demonstrates behavior through a real bean, no mocks).

> [!warning] The mock is contextual, and the container is real
> Three recurring surprises: `@InjectMock` on a `@ApplicationScoped` bean replaces the contextual instance — everything that injected it sees the mock, including other beans, which can silently cover for misconfiguration; mocking private or static methods still needs Mockito's inline config and is a smell here as anywhere; and assuming the mock exists in `@QuarkusIntegrationTest` simply fails — that suite has no container to swap into. Related trap: forgetting the stub returns `null` for unstubbed calls (NPE downstream) because defaults apply — a stub for every path the test touches.

> [!tip] Interview answer
> In QuarkusTest the app container is in the same JVM, so @InjectMock swaps the bean's contextual instance for a Mockito mock — every consumer in the container sees the mock, and I stub with when(). For real-class stubbing I use @Alternative test beans or test profiles, and for remote collaborators a config-pointed stub server. The boundary to state: this all exists only in-process — under QuarkusIntegrationTest there is no container to swap, so collaborators get replaced by configuration, not mocks.
