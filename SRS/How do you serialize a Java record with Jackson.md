<!--
reps: 0
priority: 0
-->
#Java/Language/Records #DataFormats/JSON #SRS

# How do you serialize a Java record with Jackson?

> [!abstract] Short answer
> From **Jackson 2.12**, records work like POJOs with no extra annotations: `writeValueAsString` uses the component **accessors**; `readValue` uses the **canonical constructor**. JSON property names are the component names. Rename with `@JsonProperty` on the **record component**. This is Jackson JSON mapping, not `java.io.Serializable`.

## Jackson 2.12: accessors out, canonical constructor in

```d2
direction: down
json: "{\"name\":\"Alice\",\"age\":30}" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
ser: "write: name() / age()" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
de: "read: new User(name, age)" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
json -> ser: "serialize"
json -> de: "deserialize"
```

**Fig. 1.** Native record support (jackson-databind 2.12, JDK 14+ runtime) discovers components the same way [[How do you inspect a Java record with reflection]] does: header order, accessors, canonical constructor.

FasterXML’s 2.12 notes: reading and writing `java.lang.Record` “should work when running on Java 14 or later, using expected accessors, constructors, and annotation overrides.” The databind PR that landed it: components serialize automatically; deserialization calls the canonical constructor. Spring Boot **2.5.0** is the first Boot line that manages `jackson-databind` **2.12.3**; Boot **2.4.x** still ships **2.11.4**, so native records are not on that classpath. Boot 3.x includes 2.12+.

```java
record User(String name, int age) {}

ObjectMapper mapper = new ObjectMapper();
String json = mapper.writeValueAsString(new User("Alice", 30));
// {"name":"Alice","age":30}
User u = mapper.readValue(json, User.class);
```

**Listing 1.** No `@JsonCreator`, no getters with a `get` prefix. Accessors are `name()` / `age()` ([[What methods does the compiler generate for a Java record]]).

Single-component records bind as a **JSON object** (`{"value":"x"}`), not as a raw JSON string. Pre-2.12, a one-arg constructor was treated as delegating. To get that old string-binding behavior:

```java
public record MyValueRecord(String value) {
    @JsonCreator(mode = JsonCreator.Mode.DELEGATING)
    public MyValueRecord(String value) {
        this.value = value;
    }
}
```

**Listing 2.** Explicit `@JsonCreator(DELEGATING)` from the 2.12 compatibility note (jackson-databind#2980). Default for records is properties style.

## Renames and older Jackson

`@JsonProperty` targets fields, methods, and parameters. A record-component annotation is propagated to those sites ([[Where do annotations on Java record components apply]]), so put the name on the header:

```java
public record User(
        @JsonProperty("user_name") String name,
        int age) {}
```

**Listing 3.** JSON `{"user_name":"Alice","age":30}`. You do not need a second copy on a compact-constructor parameter.

Before 2.12 (or if you treat a record as a plain immutable class), Jackson has no implicit component names: register `ParameterNamesModule` and compile with `-parameters`, or put `@JsonCreator` on the canonical constructor and `@JsonProperty` on each parameter. That module is a Jackson Java 8 feature, not a substitute for 2.12’s record introspector.

Do not confuse this with [[How does Java serialization treat record classes]] (`Serializable` / canonical constructor on the byte stream).

> [!warning] Jackson JSON ≠ `java.io.Serializable`
> `ObjectMapper` does not use Java serialization. A record that implements `Serializable` still needs Jackson 2.12+ (or creator annotations) for JSON. Deserializing JSON always constructs a **new** record via the canonical constructor.

> [!warning] One-field records expect an object, not a scalar
> `record Wrapper(String value)` deserializes `{"value":"a"}`. A JSON string `"a"` is delegating style and needs `@JsonCreator(mode = DELEGATING)` on the canonical constructor.

> [!tip] Interview answer
> **Jackson 2.12 serializes records through accessors and deserializes through the canonical constructor, so a plain `record User(String name, int age)` needs no annotations.** Use `@JsonProperty` on the component when the JSON key differs. Spring Boot 2.5+ (not 2.4) is the first Boot line with Jackson 2.12 on the classpath.
