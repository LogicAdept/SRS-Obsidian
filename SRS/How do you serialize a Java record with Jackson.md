<!--
reps: 0
priority: 0
-->
#Java/Language/Records #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: Jackson supports records natively since Jackson 2.12. It serializes with component accessors and deserializes through the canonical constructor. Simple cases need no extra annotations.

```java
record User(String name, int age) {}

ObjectMapper mapper = new ObjectMapper();
String json = mapper.writeValueAsString(new User("Alice", 30));
// {"name":"Alice","age":30}
User u = mapper.readValue(json, User.class);
```

When JSON keys differ, put `@JsonProperty` on the component (dumps also mention the compact-constructor parameter). Older Jackson: `jackson-module-parameter-names` plus the `-parameters` compiler flag, or `@JsonCreator` on the canonical constructor.

Spring Boot 2.4+ / Boot 3.x DTO migration examples in the same dumps assume Jackson record support is already on the classpath.

> [!warning] Unverified traps from the dump
> - This is JSON via Jackson, not `java.io.Serializable`.
> - There is no `#Jackson` leaf in the tag tree yet.
