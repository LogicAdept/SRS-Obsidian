<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# How do you test a Quarkus application?

> [!abstract] Short answer
> Testing has three layers. **`@QuarkusTest`** (from `quarkus-junit5`) boots the real application in the **test profile** inside the JVM before your tests and injects CDI beans normally; HTTP is asserted with REST Assured, with `@TestHTTPEndpoint` targeting a resource class. **`@QuarkusIntegrationTest`** runs the **actual build artifact** — JVM jar, native executable or container image — and talks to it over HTTP, with no mocking. Around both, **Dev Services** provision databases and brokers and **continuous testing** reruns affected tests as you edit.

## The @QuarkusTest layer

`@QuarkusTest` is not a Spring-style slice: the whole application starts (profile `test`, HTTP on 8081 by default), and tests combine plain CDI injection, `@InjectMock` for bean mocking and REST Assured for the HTTP boundary. Beans touched during startup are not automatically mocked — the mock replaces the bean in the container before requests, not the class loading path.

```java
import io.quarkus.test.junit.QuarkusTest;
import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.CoreMatchers.is;

@QuarkusTest
class GreetingResourceTest {

    @Test
    void testHelloEndpoint() {
        given()
          .when().get("/hello")
          .then()
             .statusCode(200)
             .body(is("Hello from Quarkus REST"));
    }

    @Test
    void testConfiguredEndpoint() {
        given()
          .when().get("/check/message")
          .then()
             .statusCode(200)
             .body(is("unset"));
    }
}
```

**Listing 1.** Executed in this batch (`mvnw test`, Quarkus 3.39.2, JDK 21): the app booted with "Profile test activated" on port 8081 and `Tests run: 2, Failures: 0, Errors: 0`. The shape mirrors the official getting-started test; the second test exercises `@ConfigProperty` default injection ([[How do you configure a Quarkus application]]).

## The integration layer and the loop

`@QuarkusIntegrationTest` launches the artifact the build produced — a fast jar, a native executable, or a container image built by a container-image extension — and tests it purely over HTTP; no CDI injection, no `@InjectMock`, because the process is the real one. Dev Services keep the layer honest: the same auto-provisioned database a developer used is what the test hit ([[What are Dev Services in Quarkus]]). Continuous testing closes the loop in dev mode: after `quarkus:dev`, affected tests run in the background as files change, with results surfaced in the Dev UI and console ([[How does Quarkus dev mode work]]).

```d2
direction: down
unit: "@QuarkusTest\nreal app in JVM, test profile,\n@InjectMock for beans" {
  width: 300
  height: 85
  style.fill: "#e8f5e9"
}
int: "@QuarkusIntegrationTest\njar / native / container artifact,\nHTTP only, no mocking" {
  width: 310
  height: 85
  style.fill: "#fff3e0"
}
svc: "Dev Services\ndatabases, brokers auto-started" {
  width: 290
  height: 70
  style.fill: "#e3f2fd"
}
cont: "Continuous testing\nbackground reruns in dev mode" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
unit -> svc
int -> svc
cont -> unit
```

**Fig. 1.** Fast feedback and artifact truth are separate tools: `@QuarkusTest` for the inner loop, `@QuarkusIntegrationTest` for the deployed shape, Dev Services underneath both.

> [!warning] Passing @QuarkusTest does not prove native behavior
> `@QuarkusTest` runs on the JVM with live CDI; reflection-driven shortcuts can work there and fail in a closed-world native executable. Only `@QuarkusIntegrationTest` against the native artifact tests what production runs. A second trap: `@QuarkusIntegrationTest` does not support mocking — tests built around `@InjectMock` must live in the `@QuarkusTest` layer or be redesigned around test doubles on the wire.

> [!tip] Interview answer
> I test in two layers. @QuarkusTest boots the real application under the test profile so I can mix CDI injection, @InjectMock and REST Assured against actual endpoints, with Dev Services supplying databases automatically. @QuarkusIntegrationTest then runs the built artifact — jar, native or container — over HTTP with no mocking, which is also the only way to validate native behavior. In dev mode continuous testing reruns affected tests in the background as I edit.
