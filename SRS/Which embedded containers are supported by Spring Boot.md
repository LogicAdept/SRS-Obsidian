<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Embedded #SRS

# Which embedded containers are supported by Spring Boot?

> [!abstract] Short answer
> For **servlet** applications, Spring Boot supports embedded **Tomcat**, **Jetty**, and **Undertow** (Servlet 6.0). **`spring-boot-starter-web`** pulls in **Tomcat by default** via **`spring-boot-starter-tomcat`**. Swap to Jetty or Undertow by **excluding Tomcat** and adding **`spring-boot-starter-jetty`** or **`spring-boot-starter-undertow`**.

## Servlet stack (Spring MVC)

Spring Boot's servlet reference and system requirements list three embedded servlet containers:

| Container | Typical starter | Notes |
|---|---|---|
| **Tomcat 10.1+** | **`spring-boot-starter-tomcat`** (transitive from **`spring-boot-starter-web`**) | **Default** embedded server |
| **Jetty 12** | **`spring-boot-starter-jetty`** | Exclude Tomcat from `starter-web` first |
| **Undertow 2.3** | **`spring-boot-starter-undertow`** | Exclude Tomcat; **no JSP support** on Undertow |

Boot auto-configures a **`ServletWebServerFactory`** bean — **`TomcatServletWebServerFactory`**, **`JettyServletWebServerFactory`**, or **`UndertowServletWebServerFactory`** — and starts HTTP on **port 8080** by default.

```xml
<!-- Jetty instead of Tomcat -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-web</artifactId>
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

**Listing 1.** Same swap pattern applies for **`spring-boot-starter-undertow`**.

```d2
direction: right
app: "Spring Boot app\n(main method)" {
  width: 180
  height: 60
  style.fill: "#e8f5e9"
}
factory: "ServletWebServerFactory\n(auto-configured)" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
srv: "Tomcat (default)\nJetty · Undertow" {
  width: 200
  height: 60
  style.fill: "#fff3e0"
}

app -> factory -> srv
```

**Fig. 1.** One factory bean per app; starter choice picks the embedded engine.

## Not the same as WebFlux

**`spring-boot-starter-webflux`** uses **Reactor Netty** by default (not Tomcat). Jetty and Undertow also have **reactive** factory variants, but the servlet-container list above applies to **Spring MVC / servlet** apps. See [[Which common Spring Boot starters do you know]].

Server-specific tuning uses **`server.tomcat.*`**, **`server.jetty.*`**, and **`server.undertow.*`** properties, or a **`WebServerFactoryCustomizer`**.

> [!warning] JSP limitations with embedded jars
> Spring Boot docs warn that **JSPs have limitations** in executable **jar** packaging. **Undertow does not support JSPs** at all. Tomcat/Jetty JSP support is mainly realistic with **war** packaging — not a typical Boot default.

> [!tip] Interview answer
> Servlet Spring Boot supports embedded Tomcat, Jetty, and Undertow. starter-web includes Tomcat by default. To switch, exclude spring-boot-starter-tomcat and add starter-jetty or starter-undertow. WebFlux defaults to Netty, not these servlet engines.
