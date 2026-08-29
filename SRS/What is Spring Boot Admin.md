<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Admin #SRS

# What is Spring Boot Admin?

> [!abstract] Short answer
> **Spring Boot Admin** is a **codecentric** (`de.codecentric`) **server + client** dashboard: a web UI that **registers** Spring Boot apps and **polls their Actuator** endpoints (health, metrics, logs, and other management data). It is **not** Spring Boot core and **not** a substitute for Grafana/Datadog-style observability. You run **`spring-boot-admin-starter-server`** with **`@EnableAdminServer`**, then register apps with the **Admin Client** (`spring.boot.admin.client.url`) or **Spring Cloud Discovery**.

## Server UI, clients’ Actuator

The **server** is the monitoring hub. The **client** (or the discovery registry) tells the server where each instance’s **management** / **health** URLs are. The server then **polls Actuator** and shows that in the dashboard. Hybrid registration is allowed (some apps client-register, others via Eureka/Kubernetes/…).

```xml
<dependency>
	<groupId>de.codecentric</groupId>
	<artifactId>spring-boot-admin-starter-server</artifactId>
</dependency>
```

```java
@SpringBootApplication
@EnableAdminServer
public class SpringBootAdminApplication {

	public static void main(String[] args) {
		SpringApplication.run(SpringBootAdminApplication.class, args);
	}
}
```

**Listing 1.** Official server: starter from **`de.codecentric`**, plus a web stack (`spring-boot-starter-webmvc` or **`webflux`**). `@EnableAdminServer` loads the Admin server configuration.

```properties
spring.boot.admin.client.url=${ADMIN_SERVER}
spring.boot.admin.client.auto-registration=true
```

**Listing 2.** Admin Client registration: HTTP **`POST /instances`**, then a periodic heartbeat (`period`, default **10s** in the docs). Discovery mode needs **no** Admin Client on the apps — the **server** is a discovery client instead.

The UI can also trigger **management** actions the instance exposes (log file download, cache clear, restart where those endpoints exist). That still **is** Actuator; Admin is the **console** ([[What is the difference between Spring Boot Actuator and Spring Boot Admin]]).

```d2
direction: right
apps: "Boot apps\nActuator endpoints" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
reg: "Client POST /instances\nor Cloud Discovery" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
ui: "Admin Server UI\npolls health / metrics" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}

apps -> reg -> ui
ui -> apps: poll
```

**Fig. 1.** Centralized **application-centric** view. Official docs: use it **alongside** full observability stacks, not **instead** of them ([[Which Actuator endpoints are exposed over HTTP by default]]).

> [!warning] Admin is not Actuator, and it is not Boot core
> Interview “Boot Admin” sometimes means **`/actuator/health`**. Actuator is the **library on the app**; Admin is a **separate server** (`de.codecentric`) that **reads** those endpoints. Without registration (or discovery) the UI is empty. SBA is **not** designed to replace Grafana / Datadog / Instana (no long history, distributed tracing, or that class of alerting).

> [!warning] The dashboard is only as open as the Actuator you exposed
> The server must **reach** each instance’s health/management URLs. `include=*` plus **`show-details=always`** on a **public** app leaks env, loggers, heapdump-class data. Lock **client** Actuator ([[How do you expose Spring Boot Actuator endpoints safely]]) **and** the Admin UI ([[How do you secure a Spring Boot Admin server]]). Client `user.name` / `user.password` metadata is how the server authenticates **to the app**, not how you log into the UI.

> [!tip] Interview answer
> Spring Boot Admin is a codecentric UI server that registers Boot apps and polls their Actuator endpoints for health, metrics, and logs. I enable it with spring-boot-admin-starter-server and @EnableAdminServer, then either the Admin Client posts to /instances or the server uses Spring Cloud Discovery. It is not part of Spring Boot itself, and it is not a replacement for a full observability platform.
