<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS

# Why do you use Hibernate Validator in Spring?

> [!abstract] Short answer
> **Spring integrates Jakarta Bean Validation through a JSR-style engine on the classpath** — in Boot, typically **`spring-boot-starter-validation` → Hibernate Validator.** Despite the name, **Hibernate Validator is not Hibernate ORM**; it is the **reference implementation of Jakarta Validation**, used to enforce **`@NotNull`**, **`@Size`**, **`@Email`**, and custom constraints on **beans, method parameters, and return values** — including **`@RequestBody`** / **`@ModelAttribute`** in MVC.

## Not the database layer

**Hibernate Validator** shares a project name with **Hibernate ORM** but is a **standalone validation engine**. The Jakarta Validation specification states the API is **not tied to web or persistence** — it applies to server-side services, DTOs, and configuration objects alike.

Spring Boot's validation chapter assumes a **Bean Validation implementation** (such as **Hibernate Validator**) on the classpath and wires it into:

- **Controller binding** — **`@Valid`** on **`@RequestBody`** / form objects → **`MethodArgumentNotValidException`** / **`BindingResult`**
- **Method validation** — **`@Validated`** on a class + constraint annotations on method parameters (requires a proxy)
- **`@ConfigurationProperties`** — **`@Validated`** + constraints for fail-fast config

```java
public record CreateUserRequest(
    @NotBlank String username,
    @Email String email
) {}

@PostMapping("/users")
public ResponseEntity<?> create(@Valid @RequestBody CreateUserRequest req) {
    return ResponseEntity.ok(userService.register(req));
}
```

**Listing 1.** Constraints live on the model; Hibernate Validator executes them when Spring triggers validation.

## Why Hibernate Validator specifically

| Reason | Detail |
|---|---|
| **Reference implementation** | Official docs: **Hibernate Validator is the reference implementation of Jakarta Validation** (today **HV 9.x** / **Jakarta Validation 3.x** — not the older Bean Validation 1.1 / HV 5.x pairing from legacy dumps) |
| **Default in Spring Boot** | **`spring-boot-starter-validation`** pulls in **Hibernate Validator** — no extra engine choice for most apps |
| **Portable API** | Application code uses **`jakarta.validation`** annotations; only the **engine** is Hibernate-specific |
| **Rich constraint set** | Standard **`@NotNull` / `@Size`** plus Hibernate extensions (`@Email`, `@URL`, …) |

You *could* plug another Jakarta Validation provider, but **Spring's ecosystem docs and starters assume Hibernate Validator**.

```d2
direction: right
api: "jakarta.validation\nannotations on DTOs" {
  width: 200
  height: 60
  style.fill: "#e8f5e9"
}
spring: "Spring MVC / Boot\n@Valid · @Validated" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
hv: "Hibernate Validator\n(reference impl)" {
  width: 200
  height: 60
  style.fill: "#fff3e0"
}

api -> spring -> hv: "validate at\nbind / invoke"
```

**Fig. 1.** Spring triggers validation; Hibernate Validator is the engine behind `@Valid`.

> [!warning] Do not conflate with Hibernate ORM
> **`@NotNull` on an `@Entity`** is validated by **Hibernate Validator**; **persisting** the entity is **JPA/Hibernate ORM** — separate stacks. Controller-only validation leaves **service / scheduler** entry points unchecked unless you also use **`@Validated`** on those beans. See [[How does Bean Validation work in Spring Boot]] and [[What is BindingResult in Spring MVC]].

> [!tip] Interview answer
> We use Hibernate Validator because Spring Boot's validation starter ships it as the Jakarta Validation reference implementation — not because of the database. It runs constraint annotations on request bodies, forms, and @Validated service methods. The API is jakarta.validation; the engine happens to be Hibernate Validator.
