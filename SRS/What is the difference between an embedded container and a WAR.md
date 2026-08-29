<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Embedded #Java/Spring/Boot/Build #SRS

# What is the difference between an embedded container and a WAR?

> [!abstract] Short answer
> An **embedded** container is a **library** Boot starts from `main` (`java -jar`, default **`server.port=8080`**). A **WAR** is a **servlet archive** (`WEB-INF/classes` + `WEB-INF/lib`) that an **external** Tomcat/Jetty/Undertow **process** deploys. Boot’s default is an **executable JAR** with `BOOT-INF/`. A **deployable WAR** needs `SpringBootServletInitializer`, `<packaging>war</packaging>`, and the embedded starter **`provided`**. **WebFlux cannot be a WAR.**

## Who owns the HTTP process?

Embedded (Tomcat, Jetty, Undertow on the servlet stack): Boot’s `SpringApplication` creates the `WebServer`. One OS process per app; reverse-proxy if you need many hostnames. That is the **usual** Boot packaging ([[What is an executable JAR in Spring Boot]], [[Which embedded containers are supported by Spring Boot]]).

Traditional WAR: the **container** is already running. It loads your app through servlet 3 `SpringBootServletInitializer.configure`. HTTP **connectors and ports** belong to the **server**, not to `server.port` in the WAR. One container can host **many** webapps (context paths). You do **not** install a second Tomcat just to run a second app ([[How do you deploy a Spring Boot application as a WAR]]).

```xml
<packaging>war</packaging>
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-tomcat</artifactId>
	<scope>provided</scope>
</dependency>
```

**Listing 1.** Mark the embedded engine **`provided`** (Gradle: `providedRuntime`, not `compileOnly`) so it does not clash with the external servlet API. Boot plugins then still put those jars in **`WEB-INF/lib-provided`**: the same WAR is **deployable** and **`java -jar`**-executable.

```java
@SpringBootApplication
public class MyApplication extends SpringBootServletInitializer {

	@Override
	protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
		return application.sources(MyApplication.class);
	}

	public static void main(String[] args) {
		SpringApplication.run(MyApplication.class, args);
	}
}
```

**Listing 2.** Skip `configure` and an external container never bootstraps Boot. Layout: JAR uses **`BOOT-INF/`**; WAR uses servlet **`WEB-INF/`** ([[What does a typical Java web application project structure look like]]).

```d2
direction: down
src: "Same @SpringBootApplication" {
  width: 260
  height: 45
  style.fill: "#e3f2fd"
}
jar: "executable JAR\nembedded server in-process" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
war: "WAR + provided container\nexternal servlet process" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}

src -> jar
src -> war
```

**Fig. 1.** Config is **not** “unzip the archive.” Both shapes still use Boot’s **Environment** (`./config`, env, CLI) ([[What is Spring Boot property source precedence]]). JSPs need **WAR** packaging on Tomcat/Jetty; they are **not** supported on an executable **JAR**.

> [!warning] WAR ≠ “easier production config”
> The dump’s “edit exploded properties inside the container” is not the Boot model. Externalize config. Do not treat a second HTTP port as “install another servlet container.”

> [!warning] WebFlux has no WAR path
> Official: WebFlux defaults to **Reactor Netty** and **does not** support WAR deployment. `server.port` is an **embedded** property; it does not retune an already-running Tomcat connector.

> [!tip] Interview answer
> Embedded means Tomcat or Jetty is a dependency and Boot starts it from main, usually as a fat JAR. A WAR is for an external servlet container: I extend SpringBootServletInitializer, package war, and mark the embedded starter provided. One Tomcat can host many WARs. WebFlux cannot ship as a WAR.
