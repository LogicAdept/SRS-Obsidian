<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# What are Dev Services in Quarkus?

> [!abstract] Short answer
> Dev Services **automatically provision unconfigured services** — PostgreSQL, Kafka, Keycloak and friends — in **dev and test mode**: include the extension, do not configure the service, and Quarkus starts a container (usually through Testcontainers) and wires the generated connection settings into the configuration. Explicitly configure the service and the Dev Service disables itself. Production mode never starts them.

## The trigger logic

The decision is per extension and per property: presence of a supporting extension plus absence of your own configuration starts a container; your database URL or broker address flips the behavior back to "use what is configured". Connection details discovered at startup are injected as runtime configuration, so the application code reads them like any other property — nothing Quarkus-specific leaks into the code ([[How do you configure a Quarkus application]]).

```d2
direction: down
ext: "Extension present\n(e.g. quarkus-jdbc-postgresql)" {
  width: 290
  height: 75
  style.fill: "#e3f2fd"
}
cfg: "Service configured?\n(url / credentials set)" {
  width: 260
  height: 75
  style.fill: "#fff3e0"
}
skip: "Dev Service skipped\nyour config is used" {
  width: 250
  height: 70
  style.fill: "#ffebee"
}
docker: "Container runtime available?" {
  width: 270
  height: 60
  style.fill: "#fff3e0"
}
fail: "No provisioning\nconfigure services manually" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
start: "Testcontainers starts service\nconfig injected at runtime" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
ext -> cfg
cfg: yes -> skip
cfg: no -> docker
docker: yes -> start
docker: no -> fail
```

**Fig. 1.** Dev Services only act where the configuration is silent. This is why "it works in dev" can break in prod if the service was never actually configured ([[How does Quarkus dev mode work]]).

## Behavior details worth remembering

- **Modes:** active in dev mode and in tests ([[How do you test a Quarkus application]]); `@QuarkusIntegrationTest` also works out of the box with containers launched via Dev Services.
- **Timeout:** default startup timeout is **60s**, raised via `quarkus.devservices.timeout`.
- **Sharing:** containers are shared across restarts via label-based service discovery — a matching running container is reused instead of starting a second one; relational databases additionally support Testcontainers "reusable instances" (`testcontainers.reuse.enable=true`), which stops containers from being stopped aggressively between runs.
- **Prerequisite:** a container environment (Docker or Podman). Without one, provisioning fails and services must be configured normally — the mechanism builds on [[How would you explain Testcontainers]] semantics.

> [!warning] Magic config is still configuration you must own
> The auto-generated URL and credentials exist only while the Dev Service runs; relying on them outside dev/test (or committing code that implicitly assumes a local container) is the classic failure. Also, because a Dev Service starts **when the service is unconfigured**, a partially set property can both disable the Dev Service and leave the app missing values — set the full configuration or none of it.

> [!tip] Interview answer
> Dev Services auto-provision unconfigured dependencies in dev and test mode: with the extension on the classpath and no service configuration, Quarkus starts a Testcontainers-based container and wires its connection settings into config; configuring the service disables it automatically. It needs Docker or Podman, defaults to a 60-second startup timeout, reuses containers across restarts via label discovery, and never runs in production. It removes the "no database locally" excuse while keeping explicit config the escape hatch.
