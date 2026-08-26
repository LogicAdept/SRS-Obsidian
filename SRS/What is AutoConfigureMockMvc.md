<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Java/Spring/Framework/WebMvc #Testing/Mocking #Java/Annotations #SRS

# What is AutoConfigureMockMvc?

> [!abstract] Short answer
> **`@AutoConfigureMockMvc`** (Boot **4**: `org.springframework.boot.webmvc.test.autoconfigure`) **enables MockMvc** (and **`MockMvcTester`** if AssertJ is on the classpath) on a test that is **not** already a web slice. Pair it with **`@SpringBootTest`**: full auto-config **plus** in-process MVC, **no** listen port. **`@WebMvcTest` already auto-configures MockMvc**; hang **`@AutoConfigureMockMvc`** on the slice only to **tune** attributes (`addFilters`, `print`, `printOnlyOnFailure`). It does **not** make `@SpringBootTest` fast.

## Register MockMvc on a full context

Boot: *You can also auto-configure MockMvc … in a non-`@WebMvcTest` (such as `@SpringBootTest`) by annotating it with `@AutoConfigureMockMvc`.* Default **`webEnvironment` is still `MOCK`**. For a real port use **`RANDOM_PORT`** and **`RestTestClient`**, not this.

Attributes (javadoc):

| Attribute | Default | Meaning |
| --- | --- | --- |
| **`addFilters`** | **`true`** | Register **`Filter`** beans from the context on MockMvc (including **Security**) |
| **`printOnlyOnFailure`** | **`true`** | Print `MvcResult` only when the assertion fails |
| **`print`** | **`DEFAULT`** | How that dump is written |

**`addFilters = false`** skips **every** filter, not a surgical “secure=false.” Official Security tests use **`@WithMockUser`**, not filter removal. Driver: [[What is MockMvc]]. How to assert: [[How do you write a MockMvc test]]. Slice: [[What is the WebMvcTest annotation]]. Full context: [[What is SpringBootTest]]. Security: [[How do you test Spring Security in MockMvc tests]].

```java
@SpringBootTest
@AutoConfigureMockMvc
class MyMockMvcTests {

    @Test
    void testWithMockMvc(@Autowired MockMvc mvc) throws Exception {
        mvc.perform(get("/")).andExpect(status().isOk());
    }
}
```

**Listing 1.** Conceptual Boot **4.1**. Whole application context; MockMvc is **opt-in**.

```java
@WebMvcTest(UserController.class)
@AutoConfigureMockMvc(addFilters = false)
class FiltersOffSliceTests { }
```

**Listing 2.** Conceptual: **tune** the slice. **`addFilters = false`** drops Security filters — tests go green while production still **401**. Prefer **`@WithMockUser`**.

```d2
direction: down
boot: "@SpringBootTest\nfull SpringApplication" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
ann: "@AutoConfigureMockMvc" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
mvc: "MockMvc / MockMvcTester" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}

boot -> ann -> mvc
```

**Fig. 1.** The slice **`@WebMvcTest`** already does the right-hand side **without** a full Boot refresh.

> [!warning] This is not a slice
> Full auto-config still runs (JPA, Security, messaging, …). MockMvc only avoids **Tomcat**. For MVC-only speed use **`@WebMvcTest`**.

> [!warning] `@SpringBootTest` alone has no `MockMvc` bean
> Autowire fails until this annotation (or `@WebMvcTest`). **`RANDOM_PORT`** still does not inject MockMvc — that is a **live HTTP** client.

> [!warning] `addFilters = false` is not `secure = false`
> There is **no `secure` on `@WebMvcTest`**. Turning filters off **skips CSRF and the filter chain**. That is not how Boot’s Security how-to tests a protected URL.

> [!tip] Interview answer
> **`@AutoConfigureMockMvc` on `@SpringBootTest` gives you MockMvc against the full Boot context, no real port.** `@WebMvcTest` already includes it. `addFilters` defaults **true**. Do not use it to pretend a slice is cheap.
