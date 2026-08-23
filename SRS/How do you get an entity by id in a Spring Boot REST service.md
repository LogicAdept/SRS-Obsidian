<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #Java/Spring/Data #Java/Spring/Framework/WebMvc #SRS

# How do you get an entity by id in a Spring Boot REST service?

> [!abstract] Short answer
> Call **`repository.findById(id)`**, which returns **`Optional`**. In the controller (or service), map present → **200** with a body (prefer a **DTO**), empty → **404**. Do not use deprecated **`getOne`/`getById`** for “load or 404”; those are lazy **references** (`getReferenceById`).

## Repository + HTTP mapping

```java
public interface EmployeeRepository extends JpaRepository<Employee, Long> {}

@RestController
@RequestMapping("/api/employees")
class EmployeeController {
  private final EmployeeRepository employees;

  EmployeeController(EmployeeRepository employees) {
    this.employees = employees;
  }

  @GetMapping("/{id}")
  ResponseEntity<EmployeeResponse> get(@PathVariable Long id) {
    return employees.findById(id)
        .map(e -> new EmployeeResponse(e.getId(), e.getName()))
        .map(ResponseEntity::ok)
        .orElse(ResponseEntity.notFound().build());
  }
}

record EmployeeResponse(Long id, String name) {}
```

**Listing 1.** `CrudRepository.findById` → `Optional` → `ResponseEntity` (404 when empty). Mapping keeps the JSON contract off the raw entity.

`findById` loads the entity (or returns empty if missing). Path variable binds the id; Boot auto-configures JPA repositories when `spring-boot-starter-data-jpa` is on the classpath.

```d2
direction: right
http: "GET /api/…/{id}" {
  style.fill: "#e3f2fd"
}
find: "findById(id)\nOptional" {
  style.fill: "#fff3e0"
}
ok: "200 + DTO" {
  style.fill: "#e8f5e9"
}
nf: "404" {
  style.fill: "#fce4ec"
}

http -> find
find -> ok: "present"
find -> nf: "empty"
```

**Fig. 1.** Present vs missing id at the HTTP boundary.

## `findById` vs `getReferenceById`

| API | Behavior |
| --- | --- |
| **`findById`** | Optional; empty if no row — right for GET-by-id |
| **`getReferenceById`** | Lazy reference; may not hit DB until access; missing id often fails later with `EntityNotFoundException` — for associations/FK wiring, not REST lookup |

Deprecated `getOne` / `getById` are the old names for the reference API.

> [!warning] Returning the entity type
> Serializing the JPA entity can leak fields and trigger lazy loads. Prefer a DTO/record (or projection) for the response body.

> [!tip] Interview answer
> I use `findById`, map the `Optional` to `ResponseEntity.ok` or `notFound`, and return a DTO. I reserve `getReferenceById` for getting a proxy by id inside the persistence layer, not for REST “get or 404.”

See [[What is the difference between findById and getOne in Spring Data JPA]], [[Should you return JPA entities from a Spring controller]], and [[What is a CrudRepository]].
