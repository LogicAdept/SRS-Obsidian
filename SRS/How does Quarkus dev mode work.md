<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# How does Quarkus dev mode work?

> [!abstract] Short answer
> `./mvnw quarkus:dev` (Gradle: `./gradlew quarkusDev`) boots the application in the **dev profile** with **live coding**: changed Java files are recompiled in the background and the running application is redeployed in place, so an edit-and-refresh cycle needs no manual restart. Dev mode bundles the developer loop: hot deployment with background compilation, the Dev UI, [[What are Dev Services in Quarkus|Dev Services]] for databases and brokers, optional continuous testing, and debug on port 5005 by default.

## The live-coding loop

The official flow: start dev mode once, then edit. The log line "Profile dev activated. Live Coding activated." marks the mode. Changing the returned string in the endpoint class and saving triggers background compilation; the next HTTP request executes the new code — no rebuild command, no restart. State that can be preserved is preserved across reloads; changes that augmentation cannot hot-swap (new extensions, build-time config, some structural changes) require a full restart of dev mode.

```java
// Getting-started edit cycle: keep quarkus:dev running, then
@Path("/hello")
public class GreetingResource {

    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public String hello() {
        return "Hola from Quarkus"; // was: "Hello from Quarkus REST"
    }
}
// Save -> refresh http://localhost:8080/hello -> the new body is already live.
```

**Listing 1.** The official live-coding example in condensed form: the only step between edit and effect is saving the file and refreshing the browser. [[What happens at build time in Quarkus]] explains why this is safe: the augmentation phase produced the wiring, so a hot swap of body code does not re-run discovery.

```d2
direction: right
edit: "Edit .java / resource" {
  width: 200
  height: 60
  style.fill: "#e3f2fd"
}
comp: "Background compile\n(deploy on change)" {
  width: 230
  height: 70
  style.fill: "#fff3e0"
}
dep: "Hot redeploy\nsame JVM process" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
req: "Next HTTP request\nruns new code" {
  width: 230
  height: 60
  style.fill: "#e8f5e9"
}
edit -> comp -> dep -> req -> edit: "next edit"
```

**Fig. 1.** Dev mode keeps the process alive and loops edit → compile → redeploy; only the request after redeploy sees the change.

## What else dev mode gives

- **Dev UI** at `/q/dev`: configuration editor, extension pages, readiness of Dev Services.
- **Debugging:** JVM debug on `5005` by default (`-DdebugHost` to expose it beyond localhost; `-Dsuspend` to wait for the debugger).
- **pom.xml awareness:** Quarkus detects `pom.xml` changes (new extensions, version bumps) and restarts the Maven process automatically.
- **Continuous testing:** changed tests run in the background as you edit; the loop is described with the testing story ([[How do you test a Quarkus application]]).
- **Container images:** for a dev-mode app running inside a container, the deployment directory needs write permissions for live reload — explicitly not a production setting.

> [!warning] Dev mode is not a miniature production
> It runs the **dev profile**: Dev Services may start containers, config comes from `%dev.` prefixes, and live reload is enabled — none of which holds for a packaged artifact. The common trap is configuring the app "because it works in dev" against auto-provisioned services, then shipping a jar that no longer finds them; the fix is configuring the service for prod (which also disables the Dev Service) ([[What are Dev Services in Quarkus]]).

> [!tip] Interview answer
> Dev mode is quarkus:dev: the app boots under the dev profile with live coding — background compilation hot-redeploys changes into the running process, and the next request executes them. Around that loop I get the Dev UI, debugging on 5005, automatic restart on pom changes, continuous testing and Dev Services. Build-time changes like new extensions still need a restart, and dev-mode conveniences such as auto-provisioned services are exactly that — dev-mode only.
