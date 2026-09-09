<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# What is the difference between build-time and runtime configuration in Quarkus?

> [!abstract] Short answer
> Quarkus splits its `quarkus.*` properties into two classes. **Build-time-fixed** properties are consumed during augmentation, baked into the artifact, and become **read-only** at runtime — changing them requires a rebuild (or re-augmentation); the configuration reference marks them with a lock icon. **Runtime** properties are read at startup and can vary per environment without rebuilding — the official example is the database URL, username and password, which are only known on the target machine.

## Why the split exists

Build-time values let extensions commit to optimizations: what the augmentation phase bakes in cannot change later, which is exactly what keeps boot fast and native builds possible ([[What happens at build time in Quarkus]]). At build time Quarkus also **records** the available configuration into the binary so startup fails fast on missing required values — system properties, environment variables, `.env` and build-system sources are excluded from that recording precisely because they belong to the deployment machine.

```d2
direction: down
build: "Augmentation phase\nreads build-time properties" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
freeze: "Baked into artifact\nlock icon in config docs" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
run: "Runtime startup\nreads runtime properties + excluded sources" {
  width: 330
  height: 80
  style.fill: "#e8f5e9"
}
same: "Same artifact serves many environments\nonly runtime values differ" {
  width: 330
  height: 70
  style.fill: "#e8f5e9"
}
build -> freeze
run -> same
```

**Fig. 1.** Build-time values travel inside the artifact; runtime values are supplied by the environment at boot. This is the platform-level version of the source-merge story in [[How do you configure a Quarkus application]].

## Profiles connect the two worlds

The default runtime profile equals the profile used for the build; build with `-Dquarkus.profile=prod-aws` and the runner later boots with profile `prod-aws` unless overridden by `quarkus.profile`. Running a different profile than the one baked in is supported but officially warned against: build-time decisions were made against the build profile's values.

```java
// Build once:
//   ./mvnw package -Dquarkus.profile=prod-aws
// Run the same artifact per environment, varying only runtime values:
//   DATABASE_URL=... DATABASE_USERNAME=... ./target/my-app-1.0-runner
```

**Listing 1.** The official pattern: the build profile (`prod-aws`) is recorded into the artifact; per-machine differences arrive as runtime configuration (env vars here), never as edits to build-time properties.

For genuinely different build-time settings after the artifact exists, **re-augmentation** rebuilds the augmentation output against a new configuration instead of recompiling everything.

> [!warning] The classic production trap
> Setting a build-time property via env var or `-D` at boot does **not** reconfigure the application — the value is recorded in the artifact, read-only at runtime, and the override is silently irrelevant to Quarkus' behavior (the docs: such properties are "available at runtime but as read-only"). If a knob seems dead at boot, check whether it is lock-marked; the fix is a rebuild or re-augmentation, not more env vars. And never put application-specific keys under `quarkus.*` — that namespace is the platform's ([[What is the difference between Quarkus and Spring Boot]]).

> [!tip] Interview answer
> Build-time configuration is consumed during augmentation and frozen into the artifact — it is read-only at runtime, and changing it means a rebuild or re-augmentation. Runtime configuration, like database URL and credentials, is read at boot and can differ per environment. Quarkus records available config into the binary to fail fast on missing values, the runtime profile defaults to the build profile, and mixing a different runtime profile with baked build-time decisions is explicitly warned against.
