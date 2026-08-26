<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #Java/Spring/Framework/WebMvc #API/REST #SRS

# How do you write a Spring Boot RESTful web service?

> [!abstract] Short answer
> Add **`spring-boot-starter-webmvc`** (Boot **4**; Boot **3** used **`spring-boot-starter-web`**), a class with **`@SpringBootApplication`** and **`SpringApplication.run`**, and a **`@RestController`** whose methods return objects (Jackson writes JSON). Map with **`@GetMapping` / `@PostMapping` / `@PutMapping` / `@DeleteMapping`**. Bind the URL with **`@PathVariable`**, the query with **`@RequestParam`**, and JSON input with **`@RequestBody`**. You do **not** write `web.xml` or call `RestTemplate` to *serve* the API.

## Starter, auto-config, then a controller

Boot’s first-app tutorial: `@SpringBootApplication` is `@SpringBootConfiguration` + `@EnableAutoConfiguration` + `@ComponentScan`. The web starter pulls Tomcat + Spring MVC; auto-config sets up `DispatcherServlet` and JSON converters. `@RestController` is MVC (not Boot-specific): `@Controller` + `@ResponseBody`, so return values are the **body**, not view names.

Official REST guide: Jackson on the classpath → a returned POJO becomes JSON. Extra **`jackson-dataformat-xml`** is only if you declare **`produces` XML**. Path suffixes like `/employees.json` are **not** Framework 7 content negotiation (extension strategy was removed); use **`Accept`**.

```java
@SpringBootApplication
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}

@RestController
class EmployeeController {
    private final EmployeeRepository repository;

    EmployeeController(EmployeeRepository repository) {
        this.repository = repository;
    }

    @GetMapping("/employees")
    List<Employee> all() { return repository.findAll(); }

    @GetMapping("/employees/{id}")
    Employee one(@PathVariable Long id) { return repository.findById(id).orElseThrow(); }

    @PostMapping("/employees")
    @ResponseStatus(HttpStatus.CREATED)
    Employee create(@RequestBody Employee body) { return repository.save(body); }
}
```

**Listing 1.** Conceptual: Boot entry + REST controller (tutorial / REST guide shape). Stereotype: [[What is the difference between Spring RestController and Controller]]. JSON write: [[How do you return JSON from a Spring MVC controller]]. HTTP verbs: [[How do you map HTTP methods in Spring MVC]]. Errors: [[How do you implement exception handling in Spring Boot]].

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>4.1.1</version>
</parent>
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-webmvc</artifactId>
    </dependency>
</dependencies>
```

**Listing 2.** Conceptual Boot **4** POM from the official first-application tutorial. Pin the parent version you actually use. Run with `mvn spring-boot:run` (default **8080**).

```d2
direction: down
start: "@SpringBootApplication\nSpringApplication.run" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
mvc: "DispatcherServlet + Jackson" {
  width: 260
  height: 45
  style.fill: "#fff3e0"
}
api: "@RestController\n@GetMapping / @PostMapping" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}

start -> mvc
mvc -> api
```

**Fig. 1.** Auto-config wires MVC. Your job is the controller (and persistence), not servlet XML.

> [!warning] `@ResponseBody` on `@RestController` methods is redundant
> Type-level `@ResponseBody` already applies. Repeating it does not change JSON vs XML.

> [!warning] `/resource.json` is not version 7 negotiation
> Dump samples that append `.json` / `.xml` to the path assumed **favorPathExtension**. Framework **7** negotiates **`Accept`** by default. `produces` still restricts the mapping.

> [!warning] In-memory `Map` is not REST
> A static `HashMap` `@Repository` is a demo store. It is not idempotent HTTP, not transactional, and not exception translation for JPA.

> [!tip] Interview answer
> **`spring-boot-starter-webmvc` (or Boot 3 `starter-web`) + `@SpringBootApplication` + `@RestController`.** Return POJOs; Jackson writes JSON. `@GetMapping` / `@PostMapping` plus `@PathVariable` and `@RequestBody`. Boot starts Tomcat; you do not register `DispatcherServlet` yourself.
