<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Admin #Java/Spring/Boot/Actuator #SRS

# What is the difference between Spring Boot Actuator and Spring Boot Admin?

> [!abstract] Short answer
> **Actuator** is a **Spring Boot module** (`spring-boot-actuator`, starter `spring-boot-starter-actuator`): **in-process** production endpoints (`/actuator/health`, metrics, loggers, …) over **HTTP or JMX**. You curl, scrape, or probe them. **Spring Boot Admin** is a **codecentric** (`de.codecentric`) **server + client UI**, **not** Boot core: it **registers** Boot apps and **polls their Actuator** URLs. Admin does not replace Actuator; without Actuator (and exposure) the dashboard has nothing to show.

## Library on the app vs dashboard in another process

Actuator lives **inside** each application. Endpoints are how you **monitor and interact** with that process. Default HTTP (and current JMX) exposure is **`health` only** ([[Which Actuator endpoints are exposed over HTTP by default]]; [[What is the difference between enabling and exposing an Actuator endpoint]]).

```xml
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

**Listing 1.** Official Actuator enablement: Boot’s **`spring-boot-actuator`** module via the starter ([[How do you monitor an application with Spring Boot Actuator]]).

Admin is a **separate** web app: `spring-boot-admin-starter-server` + **`@EnableAdminServer`**. Apps register with the **Admin Client** (`spring.boot.admin.client.url` → `POST /instances`) or the server uses **Spring Cloud Discovery**. The server then **HTTP-polls** each instance’s management/health URLs and draws the UI ([[What is Spring Boot Admin]]).

```xml
<dependency>
	<groupId>de.codecentric</groupId>
	<artifactId>spring-boot-admin-starter-server</artifactId>
</dependency>
```

**Listing 2.** Admin **server** coordinates; group **`de.codecentric`**, not `org.springframework.boot`. Clients still need Actuator on the classpath.

```d2
direction: right
act: "Actuator\nin each Boot app" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
http: "/actuator/health\n/metrics /loggers …" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
ui: "Admin Server UI\npolls those URLs" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}

act -> http
ui -> http: poll
```

**Fig. 1.** Actuator **is** the data plane. Admin is a **console** that reads it — plus optional write actions the instance already exposed (loggers, caches, restart).

| | **Actuator** | **Spring Boot Admin** |
|---|---|---|
| **Who ships it** | Spring Boot | codecentric |
| **Where it runs** | Inside the app | Separate server (+ optional client) |
| **What you get** | HTTP/JMX endpoints | Browser UI over many instances |
| **Typical dep** | `spring-boot-starter-actuator` | `spring-boot-admin-starter-server` |

> [!warning] “Boot Admin” in an interview often means `/actuator/health`
> Actuator is the **library**. Admin is the **dashboard**. Saying “we use Admin” when the app only has the Actuator starter is the usual mix-up. SBA is **not** Grafana/Datadog-class observability (no long history or distributed tracing as its job).

> [!warning] Admin without exposed Actuator is an empty UI
> The server must **reach** each instance’s health/management URLs. If `health` is the only HTTP-exposed endpoint, the UI is thin. `include=*` plus open `show-details` on a public app leaks env/loggers/heapdump-class data. Lock **client** Actuator ([[How do you expose Spring Boot Actuator endpoints safely]]) **and** the Admin UI ([[How do you secure a Spring Boot Admin server]]). Client metadata `user.name` / `user.password` is how the **server authenticates to the app**, not the UI login.

> [!tip] Interview answer
> Actuator is Spring Boot’s in-process production endpoints — health, metrics, loggers — over HTTP or JMX via spring-boot-starter-actuator. Spring Boot Admin is a codecentric UI server that registers apps and polls those Actuator URLs; it is not part of Boot and it does not replace Actuator. If the client does not expose Actuator, Admin has nothing to display.
