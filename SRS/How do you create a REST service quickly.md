<!--
reps: 0
priority: 0
-->
#API/REST #Java/Spring/Boot #Java/Spring/Framework/WebMvc #SRS

# How do you create a REST service quickly?

> [!abstract] Short answer
> Generate a Boot project (Initializr **Web** / **`spring-boot-starter-webmvc`** on Boot **4**) and put **`@SpringBootApplication`** plus **`@RestController`** on a class Spring can scan. **`SpringApplication.run`** starts auto-configured Tomcat and MVC. Map a path with **`@RequestMapping` / `@GetMapping`**; return a **`String`** or a POJO (**Jackson** writes JSON). Default listen port is **8080**. Boot **3** used **`spring-boot-starter-web`**; that artifact is **deprecated** on Boot **4** in favor of **`webmvc`**.

## Starter, then one scanned class

Boot’s web overview: most apps use **`spring-boot-starter-webmvc`** to get a servlet HTTP server running quickly. The first-app tutorial’s shortcut is Initializr with the **Web** starter; the long path is the same starter in the POM plus one Java type.

`@SpringBootApplication` is **`@SpringBootConfiguration` + `@EnableAutoConfiguration` + `@ComponentScan`**. With the webmvc starter on the classpath, auto-config “guesses” a web app: embedded **Tomcat** + **Spring MVC**. `@RestController` is Framework MVC (**4.0+**): **`@Controller` + `@ResponseBody`**, so the method return value is the **response body**, not a view name. `@RequestMapping` / composed mappings are MVC, not Boot-specific.

`scanBasePackages` on `@SpringBootApplication` is an alias for `@ComponentScan` only. Left empty, scanning starts at the **package of that class** and **subpackages**. It does **not** scan sibling packages, and it does **not** replace `@EntityScan` / Spring Data repository scanning.

```java
package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@SpringBootApplication
public class MyApplication {

    @RequestMapping("/")
    String home() {
        return "Hello World!";
    }

    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

**Listing 1.** Conceptual Boot **4.1** first-app shape: one class is both entry point and REST controller. Run with `mvn spring-boot:run` (or `gradle bootRun`). GET `/` on the default port **8080** yields the string body.

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webmvc</artifactId>
</dependency>
```

**Listing 2.** Conceptual Boot **4** starter. Parent **`spring-boot-starter-parent` 4.1.1** in the official tutorial pins versions; omit the version tag when that parent is in use. Boot **4** still lists **`spring-boot-starter-web`** but marks it deprecated toward **`webmvc`**.

```d2
direction: down
init: "Initializr Web\nor starter-webmvc" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
boot: "@SpringBootApplication\nSpringApplication.run" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
stack: "Tomcat :8080\nDispatcherServlet + Jackson" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
api: "@RestController\n@RequestMapping" {
  width: 240
  height: 50
  style.fill: "#f3e5f5"
}

init -> boot
boot -> stack
stack -> api
```

**Fig. 1.** The starter selects the stack. Your class must be a scanned bean; MVC mappings do the rest. CRUD repositories and HTTP verbs: [[How do you write a Spring Boot RESTful web service]]. Stereotype: [[What is the difference between Spring RestController and Controller]].

> [!warning] `@EnableWebMvc` turns Boot MVC auto-config off
> Boot servlet auto-config **replaces** `@EnableWebMvc`; the two **cannot** be used together. Extra MVC knobs go on a **`WebMvcConfigurer`** **without** `@EnableWebMvc`. Add `@EnableWebMvc` only if you want to own MVC configuration yourself. See [[What is the EnableWebMvc annotation]].

> [!warning] Controllers outside the scan root are invisible
> A main class in `com.example.app` does **not** pick up `@RestController` types in `com.example.web`. That is a silent **404**, not a startup error. Keep the application class in a parent package, or set **`scanBasePackages`**. Same bean-missing shape: [[Can a Spring controller be missing from the application context]].

> [!warning] Reactive Web is not this stack
> **`spring-boot-starter-webflux`** is the other Boot web starter. It does **not** give you servlet MVC + Tomcat. A `String` return from `@RestController` is the **body** (`Hello World!` in the tutorial), not a Thymeleaf view and not automatically a JSON object.

> [!tip] Interview answer
> **Initializr Web or `spring-boot-starter-webmvc`, one `@SpringBootApplication`, one `@RestController`.** Auto-config starts Tomcat on **8080**. Return a POJO for JSON. Do not add `@EnableWebMvc` unless you are replacing Boot’s MVC setup, and keep controllers under the scanned package.
