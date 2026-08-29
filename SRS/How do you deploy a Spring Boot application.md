<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Build #Java/Spring/Boot/Embedded #SRS

# How do you deploy a Spring Boot application?

> [!abstract] Short answer
> Package an **executable archive** (uber **JAR** or executable **WAR**) with the Spring Boot Maven/Gradle plugin’s **`repackage`** goal and run **`java -jar`**. That artifact already contains dependencies and, for web apps, an **embedded** server. To land on an **external servlet container**, produce a **deployable WAR** (`SpringBootServletInitializer`, `<packaging>war</packaging>`, embedded container **`provided`**). Cloud and Kubernetes typically run that same JAR (or a **container image** from a Dockerfile / Cloud Native Buildpacks) as a process.

## Three packaging shapes, one Boot app

Boot’s deployment how-to is explicit: you can ship to **cloud platforms** and to **virtual or real machines**. The archive type is the operations choice; Boot supports both **JAR** and **WAR** layouts.

**Executable JAR (default path).** `spring-boot-maven-plugin` **`repackage`** builds a JAR (or WAR) that holds all dependencies and is started with `java -jar`. On a VM or systemd unit, that is the whole deploy: `ExecStart=.../java -jar /var/myapp/myapp.jar`. Gradle’s Boot plugin does the same job.

```bash
java -jar myapp.jar
```

**Listing 1.** Run the uber JAR. Linux install docs treat this as the normal start command (systemd wraps it).

**Deployable WAR.** Servlet apps only — **WebFlux WAR deployment is not supported** (Netty, not the servlet API). Extend **`SpringBootServletInitializer`**, override **`configure`**, set Maven **`<packaging>war</packaging>`** (or Gradle `war`), and mark **`spring-boot-starter-tomcat`** as **`provided`** so the external Tomcat/Jetty/Undertow wins. With the Boot plugins, that still produces an **executable WAR** (`lib-provided`) you can also `java -jar`. Keep `main` and `configure` sharing the same `SpringApplicationBuilder` customizations if you support both launch styles ([[How do you deploy a Spring Boot application as a WAR]]).

**Container / cloud.** Executable JARs are what most PaaS “bring your own container” stacks expect. **Cloud Foundry** accepts a standalone JAR **or** a traditional WAR (`cf push … -p target/app.jar`). **Kubernetes** is auto-detected (`*_SERVICE_HOST` / `*_SERVICE_PORT`, overridable with `spring.main.cloud-platform`). Images: **Dockerfile** or **buildpacks** (`mvn spring-boot:build-image`). AWS ECS/Beanstalk, Heroku (`java -Dserver.port=$PORT -jar …`), and others are the same JAR or WAR in a process.

```d2
direction: right
build: "repackage\nuber JAR or WAR" {
  width: 180
  height: 70
  style.fill: "#e3f2fd"
}
jar: "java -jar\nembedded server" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}
war: "External servlet container\nSpringBootServletInitializer" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
cloud: "Image / buildpack / K8s\nsame archive as a process" {
  width: 220
  height: 80
  style.fill: "#f3e5f5"
}

build -> jar
build -> war
jar -> cloud
```

**Fig. 1.** One application, three runtimes: self-contained process, foreign servlet container, or that process inside an image ([[What is an executable JAR in Spring Boot]], [[Which embedded containers are supported by Spring Boot]]).

```xml
<packaging>war</packaging>
```

**Listing 2.** Maven switch to WAR. Pair with `provided` Tomcat and a `SpringBootServletInitializer` subclass — not with WebFlux.

> [!warning] Fat-JAR vs WAR is where it runs, not whether Boot is “correct”
> Both are first-class. JAR + embedded server is the usual cloud/VM path; WAR is for an **ops-mandated** servlet container. Mixing them without `provided` means **two** containers. WebFlux **cannot** be a WAR. `java -jar` on an executable WAR is still embedded; dropping the file into Tomcat is the external-server path.

> [!warning] The process must listen where the platform routes
> Heroku (and similar) assign **`$PORT`** — feed it with `server.port` / `-Dserver.port`. On Kubernetes, a **preStop** sleep plus a long enough **termination grace period** matters; Boot graceful shutdown alone does not stop the kube-proxy window. Do not enable forwarded-header support unless traffic comes from a **trusted** proxy (`server.forward-headers-strategy`).

> [!tip] Interview answer
> I ship an executable JAR from Boot’s repackage goal and run java -jar with the embedded server — that is the default VM, systemd, and most cloud deploys. If the shop requires an external Tomcat, I build a WAR with SpringBootServletInitializer, war packaging, and provided Tomcat; WebFlux cannot go that way. Kubernetes and Docker run the same JAR as a container image, via a Dockerfile or buildpacks, not a different application type.
