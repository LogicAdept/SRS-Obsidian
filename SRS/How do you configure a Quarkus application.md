<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# How do you configure a Quarkus application?

> [!abstract] Short answer
> Configuration lives in `application.properties` (or YAML via the config-yaml extension) and is injected with **MicroProfile Config** APIs: `@ConfigProperty` for single values, `@ConfigMapping` interfaces for grouped values. All sources merge by **ordinal** — system properties over environment variables over `.env` over `config/application.properties` over the classpath file — and **profiles** (`%dev`, `%test`, `%prod`) vary values per environment in the same file. The `quarkus.*` namespace belongs to the platform and extensions, never to your application keys.

## Sources and their order

SmallRye Config (the MicroProfile Config implementation) aggregates sources by descending ordinal; lookup stops at the first source that has the property, so a higher source overrides per property, not per file:

| Ordinal | Source |
|---------|--------|
| 400 | System properties (`-Dkey=value`) |
| 300 | Environment variables (relaxed mapping: `QUARKUS_HTTP_PORT` → `quarkus.http.port`) |
| 295 | `.env` file in the working directory |
| 260 | `$PWD/config/application.properties` |
| 250 | `application.properties` on the classpath |
| 100 | `META-INF/microprofile-config.properties` |

```java
import jakarta.inject.Inject;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import org.eclipse.microprofile.config.inject.ConfigProperty;

@Path("/check")
public class ConfiguredResource {

    @Inject
    @ConfigProperty(name = "check.message", defaultValue = "unset")
    String message;

    @GET
    @Path("/message")
    public String message() {
        return message;
    }
}
```

**Listing 1.** Field injection of a config value (compiled on Quarkus 3.39.2, JDK 21). Without `defaultValue` an absent value fails the build's deploy-time validation instead of breaking at first use — a deliberate build-time check.

## Profiles and grouped mappings

Profile prefixes select values per environment: `quarkus.http.port=9090` plus `%dev.quarkus.http.port=8181` yields 8181 only under dev. The three default profiles activate automatically — **dev** in `quarkus:dev`, **test** under tests, **prod** otherwise — and custom profiles are just names you activate (`%prod-aws`). In `.env` files the syntax uses underscores: `_DEV_QUARKUS_HTTP_PORT=8181`. For structured groups, bind an interface with `@ConfigMapping(prefix = "...")` instead of reading dozens of loose keys.

```d2
direction: down
sys: "System props (400)" {
  width: 220
  height: 55
  style.fill: "#ffebee"
}
env: "Env vars (300) + .env (295)" {
  width: 250
  height: 55
  style.fill: "#ffebee"
}
files: "config/application.properties (260)\nclasspath application.properties (250)\nmicroprofile-config.properties (100)" {
  width: 340
  height: 90
  style.fill: "#e3f2fd"
}
res: "Merged view + profile prefix (%dev, %test, %prod)" {
  width: 330
  height: 80
  style.fill: "#fff3e0"
}
inj: "@ConfigProperty / @ConfigMapping" {
  width: 280
  height: 60
  style.fill: "#e8f5e9"
}
sys -> res
env -> res
files -> res
res -> inj
```

**Fig. 1.** Every arrow is a possible override target; the merge is per property. This same machinery configures Quarkus itself — compare the platform-side split in [[What is the difference between build-time and runtime configuration in Quarkus]] and the Spring equivalent [[What is Spring Boot property source precedence]].

> [!warning] Namespaces and traps
> `quarkus.*` is reserved for platform and extension properties; putting application values there invites collisions with real platform knobs. Environment variables are checked **after** system properties but **before** files — a stray `CHECK_MESSAGE` env var silently beats your `application.properties`. And YAML support needs the smallrye-config-yaml extension; a `application.yaml` without it is just an unread file ([[What is a Quarkus extension]]).

> [!tip] Interview answer
> I put values in application.properties, inject them with @ConfigProperty or group them via @ConfigMapping, and rely on MicroProfile Config source ordering — system properties, then env vars, then .env, then the config folder, then the classpath file. Profiles like %dev and %prod vary the same keys per environment and activate automatically. The quarkus.* prefix is reserved for the platform, and build-time properties are a separate story because they freeze into the artifact.
