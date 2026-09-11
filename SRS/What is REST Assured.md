<!--
reps: 0
priority: 0
-->
#API/REST #Java/Testing #SRS

# What is REST Assured

> [!abstract] Short answer
> REST Assured is a Java library for testing HTTP APIs with a fluent, BDD-style DSL: given (request spec — headers, auth, body), when (method and URI), then (validation with Hamcrest matchers on status, headers, and body via JSON paths). It puts API assertions inside normal JUnit tests with static imports, so a REST call reads like a sentence.

## The DSL and what it verifies

The canonical shape: given().header(...).body(...).when().post("/orders").then().statusCode(201).body("id", notNullValue()). Static imports from io.restassured.RestAssured keep it readable; the body matchers use Groovy GPath (jsonPath/xmlPath) to navigate nested JSON without model classes — fast for contract checks that would need a DTO per response otherwise. RequestSpecBuilder and ResponseSpecBuilder extract reusable specs (auth header, base URL, common assertions); request logging (log().all()) and filters capture traffic for debugging or custom auth flows. It handles form params, multipart, cookies, and OAuth signatures, making it the workhorse for integration-level API tests in JVM projects ([[How do you test the service layer in Spring]] for where these tests slot; [[How do you write a MockMvc test]] for the controller layer without a socket; [[What is TestRestTemplate]] as the Boot-native alternative).

```java
import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

given()
    .baseUri("http://localhost:8080")
    .header("Authorization", "Bearer " + token)
    .contentType("application/json")
    .body("{"item":"book"}")
.when()
    .post("/api/orders")
.then()
    .statusCode(201)
    .header("Location", containsString("/api/orders/"))
    .body("id", notNullValue());
```

**Listing 1.** The given/when/then DSL: request spec, call, and Hamcrest assertions on status, headers, and body — a JUnit test method around this is a complete API contract test (conceptual, per rest-assured README).

## Position in the testing pyramid

REST Assured tests run over the wire against a real (or containerized) server, so they live at the integration level: slower than MockMvc (which calls controllers in-process without a socket) but closer to reality — real serialization, filters, and headers ([[How do you test the service layer in Spring]] for unit-level; [[How would you explain Testcontainers]] spins the dependencies these tests need — the common pairing is Testcontainers for the database and REST Assured for the HTTP assertions; [[What is TestRestTemplate]] covers the same level with a simpler assertion story). Typical stack: JUnit 5 + Spring Boot test slices or a standalone server, Testcontainers for infrastructure, REST Assured for the API contract. Its DSL keeps API tests declarative enough that non-specialists review them — the trade over plain HttpClient assertions is a Groovy-flavored dependency and stack traces that need practice ([[What are the key principles of good API design]] — a testable API is itself a design deliverable).

```d2
junit: JUnit 5 test
given: given(...) request spec
headers, auth, body
when: when(...) HTTP call
then: then(...) Hamcrest assertions
status, headers, GPath body
tc: Testcontainers backend
(real dependencies, real wire)
junit -> given -> when -> then
when -> tc
```

**Fig. 1.** The DSL mirrors the test anatomy — spec, call, assertions — executed against a real, containerized server.

> [!warning] REST Assured is a client, not a mocking framework
> It sends real HTTP; it cannot fake your backend. Tests that "use REST Assured" against WireMock are testing the mock, not the service — wire the library to a real (containerized) application instance, or the green build means nothing.

> [!tip] Interview answer
> REST Assured is the JVM standard DSL for API integration tests: given/when/then with Hamcrest matchers and GPath navigation — statusCode(201), body("id", notNullValue()) — inside plain JUnit. I extract reusable request specs for auth and base URL, run it against a Testcontainers-backed server, and it covers the real wire: serialization, filters, headers. MockMvc stays for fast controller-slice tests; REST Assured is the contract level.
