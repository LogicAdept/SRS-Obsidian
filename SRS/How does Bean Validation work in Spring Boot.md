<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Spring/Boot/AutoConfiguration #Java/Annotations #SRS

# How does Bean Validation work in Spring Boot?

> [!abstract] Short answer
> Put **`spring-boot-starter-validation`** (Hibernate Validator) on the classpath. In MVC, **`@Valid` / `@Validated`** on a **`@RequestBody`**, **`@ModelAttribute`**, or **`@RequestPart`** command object runs Jakarta Bean Validation after binding. Failures become **`MethodArgumentNotValidException`** (**HTTP 400**) unless a **`BindingResult`** sits immediately after that parameter. Constraints **on method parameters or the return type** use **method validation** and raise **`HandlerMethodValidationException`** (also 400). On **services**, annotate the **class** with Spring’s **`@Validated`** so **`MethodValidationPostProcessor`** wraps a proxy.

## Two MVC paths, plus a service proxy

Boot auto-enables Bean Validation 1.1 **method** validation when a JSR-303 provider is present. `LocalValidatorFactoryBean` is both `jakarta.validation.Validator` and Spring’s `Validator`; it adapts `ConstraintViolation`s to `FieldError`s.

**Argument validation** (one object): `@Valid` or `@Validated` on a command object that is not a `Map`/`Collection`, with **no** `Errors`/`BindingResult` next to it, and **no** method-level `@Constraint`s that would take over. Exception: **`MethodArgumentNotValidException`** (a `BindException` / `ErrorResponse`).

**Method validation** (the whole signature): `@Min`, `@NotBlank`, and other **`@Constraint`** annotations on parameters or the return value **supersede** per-argument validation, because they already cover nested `@Valid`. Exception: **`HandlerMethodValidationException`**. `@Valid` **alone is not a constraint** — adding `@NotNull` next to it **does** switch to method validation. Framework **6.1+** does this inside MVC **without** an AOP proxy; a **class-level `@Validated` on the controller** forces the older AOP path — **remove it** to use the built-in support.

**Service / other beans:** class-level `@Validated` is the **pointcut** for `MethodValidationPostProcessor`. Default exception there is **`ConstraintViolationException`**, not the MVC 400 types (unless you `setAdaptConstraintViolations(true)` for `MethodValidationException`). Groups: `@Validated({Create.class})` as Spring’s group-aware `@Valid`.

```java
public class PersonForm {
    @NotNull @Size(max = 64) private String name;
    @Min(0) private int age;
}

@PostMapping("/persons")
public ResponseEntity<Void> create(@Valid @RequestBody PersonForm form) {
    return ResponseEntity.created(/* … */).build();
}

@Service
@Validated
public class PersonService {
    public void add(@Valid PersonForm form, @Max(2) int degrees) { /* … */ }
}
```

**Listing 1.** Conceptual: MVC argument validation vs Boot **service** method validation (Spring Framework 7 / Boot validation chapter). Form errors in-method: [[What is BindingResult in Spring MVC]]. Custom 400 bodies: [[What does the ExceptionHandler annotation do]], [[What is ProblemDetail in Spring]].

```d2
direction: down
mvc: "@Valid @RequestBody\ncommand object" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
arg: "MethodArgumentNotValidException\nHTTP 400" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
sig: "@NotBlank / @Min on params" {
  width: 260
  height: 45
  style.fill: "#e3f2fd"
}
hmv: "HandlerMethodValidationException\nHTTP 400" {
  width: 300
  height: 55
  style.fill: "#fff3e0"
}
svc: "@Validated service + AOP proxy" {
  width: 280
  height: 45
  style.fill: "#e8f5e9"
}
cve: "ConstraintViolationException" {
  width: 260
  height: 40
  style.fill: "#fce4ec"
}

mvc -> arg
sig -> hmv
svc -> cve
```

**Fig. 1.** MVC uses two exception types depending on the signature. Services use a validation interceptor unless you call the target through the Spring proxy.

> [!warning] Starter is not on `spring-boot-starter-web`
> **`spring-boot-starter-validation`** supplies Hibernate Validator. Without a provider, `@Valid` is a no-op and invalid bodies still return 200.

> [!warning] `BindingResult` swallows the 400
> Declare `Errors`/`BindingResult` **immediately after** the validated parameter and the method **runs** with errors on that object. Constraints on **other** parameters still raise `HandlerMethodValidationException`.

> [!warning] Self-invocation skips the service interceptor
> Method validation on `@Validated` beans is an **AOP proxy**. `this.add(form)` inside the same class does not validate. Same family as [[What happens when a Spring bean calls its own Async method]].

> [!warning] Controller `@Validated` hides 6.1 MVC method validation
> Class-level `@Validated` on a `@Controller` routes method validation through AOP. Remove it if you want Framework’s built-in `HandlerMethodValidationException` path.

> [!tip] Interview answer
> Boot needs **`spring-boot-starter-validation`**. Controllers: `@Valid` on the body/form object → `MethodArgumentNotValidException` / 400, or `BindingResult` to handle it yourself. Constraints on parameters → `HandlerMethodValidationException`. Services: **`@Validated` on the class** plus a Spring proxy, not `@Valid` alone.
