<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Embedded #Java/Spring/Boot/Build #SRS

# How do you deploy a Spring Boot application as a WAR?

> [!abstract] Short answer
> Three documented steps: **(1)** extend **`SpringBootServletInitializer`** and override **`configure`**, **(2)** set packaging to **`war`**, **(3)** mark the embedded container **`provided`** so the external Tomcat/Jetty/Undertow owns the servlet API. The usual Boot default is still an **executable JAR**; a WAR is for a **servlet container** you do not embed. **WebFlux cannot be a WAR.** With the Boot plugins, a `provided` container still yields an **executable WAR** you can `java -jar`.

## The three steps

Traditional deployment uses Spring Framework servlet 3.0 support: the container calls your initializer, which builds a `SpringApplication`.

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

**Listing 1.** Initializer for the external container; `main` for `java -jar` on the same artifact. If you customize the builder (banner, sources), share that logic between `configure` and `main`.

```xml
<packaging>war</packaging>
```

**Listing 2.** Maven (`spring-boot-starter-parent` already configures the war plugin). Gradle: `apply plugin: 'war'`.

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-tomcat</artifactId>
  <scope>provided</scope>
</dependency>
```

**Listing 3.** Embedded server must not fight the host. Gradle: `providedRuntime` for `spring-boot-starter-tomcat-runtime` — **not** `compileOnly` (tests lose the web classpath). Boot’s packager then puts those libs in **`lib-provided`**, so the WAR is both **deployable** and **`java -jar`**-executable.

```d2
direction: right
init: "SpringBootServletInitializer\nconfigure()" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
pack: "packaging war\nembedded provided" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
host: "External servlet container\nServlet 3.0 bootstrap" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

init -> pack -> host
```

**Fig. 1.** Without the initializer, the host has no Boot entry point. Without `provided`, you pack **two** containers ([[Which embedded containers are supported by Spring Boot]], [[How do you deploy a Spring Boot application]]).

WebLogic additionally needs the class to **`implements WebApplicationInitializer`** even if the superclass already does.

> [!warning] Skip the initializer and the context never bootstraps
> A WAR can deploy “successfully” while Spring never starts if there is no **`SpringBootServletInitializer`**. That class is the **first** step in the official recipe — it is what the servlet container invokes. `main` alone is only for `java -jar`. **WebFlux** apps (Reactor Netty, no servlet API contract) **cannot** use this path at all.

> [!warning] `provided` is not optional if the server is external
> Leaving Tomcat as a compile/runtime dependency packages the embedded server **inside** the WAR. Use **`provided`** / **`providedRuntime`**, not Gradle **`compileOnly`**. Executable JAR remains the simpler default when you are not mandated onto an external container ([[What is an executable JAR in Spring Boot]]).

> [!tip] Interview answer
> For a WAR I extend SpringBootServletInitializer and override configure, set packaging to war, and mark the embedded Tomcat starter provided so the external server wins. That is servlet-only — WebFlux cannot be deployed as a WAR. The same artifact can still be java -jar if Boot packaged provided libs under lib-provided; otherwise the default production shape is an executable JAR.
