<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #Java/Spring/Security/FilterChain #SRS

# What is permitAll in a method-security expression?

> [!abstract] Short answer
> **`permitAll` is a SpEL root field/method that always allows the invocation.** `@PreAuthorize("permitAll")` does **not** load `Authentication` and does **not** run a role check. Same *name* as HTTP `.permitAll()`, **different stack**: method AOP vs `AuthorizationFilter`. JSR-250 **`@PermitAll`** is a third thing and needs `jsr250Enabled`.

## Always true, no user lookup

On `SecurityExpressionRoot` / `MethodSecurityExpressionRoot`, `permitAll` is a `final boolean` **and** `permitAll()` returns **`true`**. The 7.1 reference: the method requires **no authorization** to be invoked; `Authentication` is **never** retrieved from the session (same note as `denyAll`). Official list uses the field name; `@PreAuthorize("permitAll()")` is the same always-true method.

Typical use: a **class-level** default you tighten on sensitive methods, or a test fixture that must stay callable. Class-level `@PreAuthorize` applies to every method; a method-level `@PreAuthorize` **overrides** the class (7.1: methods declaring the annotation override the class-level annotation). No method annotation means the class rule stands — `@PreAuthorize("permitAll")` on the type leaves those methods **open**.

HTTP `authorizeHttpRequests(...).permitAll()` does **not** run when another bean calls the service. JSR-250 **`@PermitAll`** is `jakarta.annotation.security.PermitAll`; it needs `@EnableMethodSecurity(jsr250Enabled = true)` and is not SpEL.

```java
@Service
@PreAuthorize("permitAll")
public class CatalogService {

    public Item findPublic(long id) {
        return load(id);
    }

    @PreAuthorize("hasRole('ADMIN')")
    public void withdraw(Item item) {
        remove(item);
    }
}
```

**Listing 1.** Conceptual Security **7.1** — class default allows; `withdraw` overrides to `ROLE_ADMIN`. Drop the method annotation and `withdraw` is public too.

```java
http.authorizeHttpRequests((authorize) -> authorize
        .requestMatchers("/catalog/**").permitAll()
        .anyRequest().authenticated());
```

**Listing 2.** Conceptual — HTTP matcher. This does **not** protect `CatalogService` when a scheduler or another bean calls it.

```d2
direction: right
http: "authorizeHttpRequests\n.permitAll()" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
aop: "@PreAuthorize(\"permitAll\")\nmethod interceptor" {
  width: 260
  height: 50
  style.fill: "#c8e6c9"
}
jsr: "JSR-250 @PermitAll\njsr250Enabled" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
```

**Fig. 1.** Three different permits. See [[What is denyAll in a method-security expression]], [[What is jsr250Enabled in method security]], [[What is PreAuthorize]], [[Can method security run without a SecurityFilterChain]].

> [!warning] Class-level `permitAll` is a wide-open default
> Method annotations override the class; they do **not** combine. Forgetting `@PreAuthorize` on a mutating method leaves the class-level `permitAll`. `permitAll` is not “disable method security” — the interceptor still runs and returns grant without reading the session. HTTP `.permitAll()` on a URL is unrelated.

> [!tip] Interview answer
> `permitAll` in `@PreAuthorize` is SpEL that always grants and does not look up `Authentication`. People mix it up with HTTP `.permitAll()` and with JSR-250 `@PermitAll`, which needs `jsr250Enabled`. A class-level `permitAll` is a default; the method annotation replaces it, so a missing method rule stays open.
