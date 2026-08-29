<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Embedded #Java/Spring/Boot/Build #SRS

# How do you switch the embedded server from Tomcat to Jetty?

> [!abstract] Short answer
> On the **servlet** stack, `spring-boot-starter-web` / **`spring-boot-starter-webmvc`** pulls **`spring-boot-starter-tomcat`**. **Exclude** that module and add **`spring-boot-starter-jetty`**. Leave both on the classpath and Boot still sees Tomcat. **WebFlux** defaults to **Reactor Netty**, not Tomcat — swap that starter instead if the app is reactive.

## Exclude Tomcat, add the Jetty starter

Boot ships a starter per HTTP server. Switching is a **dependency** change, not a `server.*` property.

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-webmvc</artifactId>
  <exclusions>
    <exclusion>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-tomcat</artifactId>
    </exclusion>
  </exclusions>
</dependency>
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-jetty</artifactId>
</dependency>
```

**Listing 1.** Current Boot how-to (MVC). Gradle: `exclude module: 'spring-boot-starter-tomcat'` on the web starter, then `implementation 'org.springframework.boot:spring-boot-starter-jetty'`.

For a **WAR**, the same swap applies, but Jetty must be **`provided`**. Gradle also needs **`providedRuntime 'org.springframework.boot:spring-boot-starter-jetty-runtime'`** ([[How do you deploy a Spring Boot application as a WAR]]).

Reactive apps: exclude **`spring-boot-starter-reactor-netty`** from **`spring-boot-starter-webflux`** and add `spring-boot-starter-jetty` (or Tomcat). Do not “exclude Tomcat” there — it was never the default ([[Which embedded containers are supported by Spring Boot]]).

Further Jetty-only knobs use `WebServerFactoryCustomizer` on the Jetty factory (HTTP/2 needs extra Jetty modules; SNI mapping differs from Tomcat).

```d2
direction: right
web: "starter-webmvc\n(default Tomcat)" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
ex: "exclude\nstarter-tomcat" {
  width: 180
  height: 70
  style.fill: "#ffebee"
}
jetty: "starter-jetty" {
  width: 160
  height: 70
  style.fill: "#e8f5e9"
}

web -> ex -> jetty
```

**Fig. 1.** One container starter wins. The exclude is mandatory; adding Jetty beside Tomcat is not a switch.

> [!warning] Two starters means you did not switch
> If `spring-boot-starter-tomcat` remains (another starter, BOM leftover, or a missed exclusion), the classpath still has Tomcat and you can get the **Tomcat** factory or a conflict. Check the effective POM/Gradle resolution, then the startup log (`Tomcat initialized` vs Jetty). `server.port` does not choose the engine.

> [!warning] WebFlux is not “Tomcat unless you switch”
> `starter-webflux` embeds **Netty**. Copy-pasting the MVC Tomcat exclusion does nothing useful there. WAR + Jetty also needs **`provided`** / **`jetty-runtime`** or the embedded server fights the external container.

> [!tip] Interview answer
> Default MVC embedded server is Tomcat via spring-boot-starter-tomcat. I exclude that from the web starter and add spring-boot-starter-jetty. If Tomcat stays on the classpath I have not switched. WebFlux starts Netty unless I swap reactor-netty for jetty, and a WAR needs Jetty marked provided.
