<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# What is the Dev UI in Quarkus?

> [!abstract] Short answer
> The **Dev UI** is Quarkus' developer console that comes alive in dev mode at **`/q/dev-ui`**: each installed extension renders a **card** with its configuration, documentation and live tools — configuration editor with per-property docs, Dev Services status, Flyway migrations, testing view, build-time info, logs. It is extension-extensible (a card is a documented extension contribution), it exists only in dev/test mode, and it is Quarkus' flagship "developer joy" feature alongside live reload and continuous testing.

## What the cards actually give you

The landing page lists every extension in use as a card; cards open into pages backed by the running application — not static docs. Typical surfaces: the **configuration editor** (all `quarkus.*` properties with documentation and the build-time/runtime marker, editable in place), **Dev Services** (which containers were provisioned, ports, stop/start), **Flyway** (applied and pending migrations), **Hibernate** (persistence units), **REST client** endpoints, **messaging** channel state, and the **testing** view behind continuous testing. The build info card exposes augmentation detail useful when "why is this property build-time-fixed" debugging. Extension authors contribute their own pages — the card system is a documented extension API ([[What is a Quarkus extension]]), which is why third-party extensions (LangChain4j, Camel) appear with their own tooling in dev.

```java
// Dev UI is reachable only from the dev-mode process (JDK 21, Quarkus 3.39.2):
//
// $ ./mvnw quarkus:dev
// [INFO] --- quarkus-maven-plugin:3.39.2:dev ---
// 2026-09-09 ... INFO  [io.quarkus] (Quarkus Main Thread) Profile dev activated. Live Coding activated.
// 2026-09-09 ... INFO  [io.quarkus] ... Listening on: http://localhost:8080
// 2026-09-09 ... INFO  [io.quarkus] ...
// -- press 'd' here opens the browser at http://localhost:8080/q/dev-ui
//
// URL check from the same machine (verbatim behavior):
//   GET /q/dev-ui  -> 200 (dev mode)     GET /q/dev-ui -> 404 (packaged fast-jar run)
//
// Cards observed on the demo app (extensions present): Configuration, Dev Services,
// Continuous Testing and Testing view, smallrye-health endpoints, Flyway migrations,
// Reactive Messaging channels - each card linking into its live state.
```

**Listing 1.** The same artifact returned 200 in dev mode and 404 from the packaged run of this deck's demo — the console is a dev-mode feature by design, not a hidden prod endpoint to lock down ([[How does Quarkus dev mode work]] is the process it lives in).

```d2
direction: down
dev: "./mvnw quarkus:dev\nProfile dev activated" {
  width: 260
  height: 60
}
ui: "Dev UI at /q/dev-ui\ncard per installed extension" {
  width: 300
  height: 65
  style.fill: "#e3f2fd"
}
tools: "Live tools\nconfig editor, Dev Services, migrations,\ntesting view, build info, logs" {
  width: 360
  height: 80
  style.fill: "#e8f5e9"
}
ext: "Extension-contributed cards\ndocumented API for extension authors" {
  width: 340
  height: 65
  style.fill: "#fff3e0"
}
dev -> ui -> tools
ext -> ui: "adds cards"
```

**Fig. 1.** The console is the visible face of dev mode; extension cards are how each technology surfaces its own controls ([[What are Dev Services in Quarkus]] renders through the same mechanism).

## Where it fits in the workflow

Dev UI collapses the "read the guide → grep the config reference → restart to test" loop into in-browser iteration: change a dev-time property in the config editor and the running app reacts; watch Dev Services start the database you forgot to install; read migration state after editing a Flyway script. It complements rather than replaces tooling — CI uses the same properties and extensions programmatically ([[How do you test a Quarkus application]] — the continuous testing view drives the same engine the CI runs).

> [!warning] Dev UI is not a feature of your application
> It ships with the dev-mode tooling, not your artifact: `java -jar` of the fast-jar has no Dev UI, and planning "we'll leave it enabled in staging" is not a thing to plan. Two confusions to avoid in interviews: the path moved across versions (older guides mention `/q/dev`, current docs use `/q/dev-ui`) — a 404 on the old path in a modern app is version drift, not breakage; and Dev UI cards can run actions against the dev process (clear caches, restart Dev Services) — quoting it as "just a documentation page" undersells and slightly misdescribes it.

> [!tip] Interview answer
> The Dev UI is the dev-mode console at /q/dev-ui — a card per installed extension, each backed by the live process: a configuration editor with docs and build-time markers, Dev Services status, Flyway migration state, the continuous testing view, build info. Extension authors add their own cards through a documented API, so third-party techs show up with their own controls. It exists only in dev mode — the packaged artifact has no Dev UI — and it's the visible half of the developer-joy loop alongside live reload.
