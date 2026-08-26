<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Java/Annotations #SRS

# What is the JsonTest annotation?

> [!abstract] Short answer
> **`@JsonTest`** (module **`spring-boot-test-autoconfigure`**, package **`org.springframework.boot.test.autoconfigure.json`**, since **1.4**) is Boot’s **JSON slice**. It enables **JSON-mapper auto-config only** and scans **`@JacksonComponent`** plus Jackson **`JacksonModule`** beans (Jackson **3** **`JsonMapper`**). Deprecated Jackson **2** path: **`ObjectMapper`**, **`@JsonComponent`**, Jackson **`Module`**. Also **Gson** / **Jsonb** when those libraries are on the classpath. Autowire **`JacksonTester<T>`** (or Gson/Jsonb/Basic testers). **No MVC, no MockMvc, no database.**

## Mapper + testers, nothing else

AssertJ helpers sit on **JSONAssert** and **JsonPath**: **`json.write(dto).isEqualToJson("expected.json")`** (file next to the test), **`hasJsonPathStringValue`**, **`json.parse(content)`**. Tune tester beans with **`@AutoConfigureJsonTesters`**. Without the slice, call **`JacksonTester.initFields(this, mapper)`** in **`@BeforeEach`**. Two **`@…Test`** annotations on one class are **unsupported** — do not stack this with **`@WebMvcTest`**. Family: [[What are Spring Boot test slices]]. MVC slice: [[What is the WebMvcTest annotation]]. JSONAssert: [[What is JSONAssert]]. Full app: [[What is SpringBootTest]].

```java
@JsonTest
class MyJsonTests {

    @Autowired JacksonTester<VehicleDetails> json;

    @Test
    void serialize() throws Exception {
        VehicleDetails details = new VehicleDetails("Honda", "Civic");
        assertThat(this.json.write(details)).isEqualToJson("expected.json");
        assertThat(this.json.write(details)).extractingJsonPathStringValue("@.make").isEqualTo("Honda");
    }

    @Test
    void deserialize() throws Exception {
        String content = "{\"make\":\"Ford\",\"model\":\"Focus\"}";
        assertThat(this.json.parse(content)).isEqualTo(new VehicleDetails("Ford", "Focus"));
    }
}
```

**Listing 1.** Conceptual Boot **4.1**. Helper type: **`org.springframework.boot.test.json.JacksonTester`**.

```java
@JsonTest
@AutoConfigureJsonTesters
class TunedJsonTests { }
```

**Listing 2.** Conceptual: extra control over tester registration (`enabled` defaults **true**).

```d2
direction: down
ann: "@JsonTest" {
  width: 180
  height: 35
  style.fill: "#e3f2fd"
}
keep: "JsonMapper / Gson / Jsonb\n@JacksonComponent" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
drop: "MockMvc / DataSource / @Service" {
  width: 280
  height: 40
  style.fill: "#ffebee"
}
tester: "JacksonTester.write / parse" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}

ann -> keep -> tester
ann -> drop
```

**Fig. 1.** DTO JSON only. Controller mapping is **`@WebMvcTest`**. Persistence is **`@DataJpaTest`**.

> [!warning] Not a web test
> **No** `MockMvc`, **no** listen port, **no** `@RestController` invocation. A passing `@JsonTest` does not prove your endpoint returns that JSON.

> [!warning] `@JsonComponent` is the Jackson 2 name
> Boot **4** prefers **`@JacksonComponent`** and **`JsonMapper`**. Custom serializers that are only `@Component` **are not scanned**.

> [!warning] Number JSON-path + `isEqualTo`
> AssertJ helpers may not like **`isEqualTo`** on a JSON number. Use **`satisfies`** (Boot documents an offset example around `0.15`).

> [!tip] Interview answer
> **`@JsonTest` is the JSON slice: mapper plus `JacksonTester`, no web and no DB.** `write` / `parse` and `isEqualToJson`. For a controller, that is `@WebMvcTest`.
