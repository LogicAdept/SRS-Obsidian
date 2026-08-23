<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Spring/Framework/WebMvc #SRS

# Should you return JPA entities from a Spring controller?

> [!abstract] Short answer
> Prefer **not** for public JSON APIs. Return a **DTO / record / Spring Data projection** shaped for the contract. Returning entities couples the HTTP API to the persistence model and invites **lazy-load surprises** during serialization (mitigated — and often hidden — by Boot’s default **Open EntityManager in View**).

## Why entities in `@RestController` hurt

1. **API = schema** — every association and field becomes fair game for Jackson unless you fight with `@JsonIgnore` / mix-ins.
2. **Lazy loading** — serializers walk getters; uninitialized associations trigger loads or `LazyInitializationException` if the persistence context is closed.
3. **OSIV masks the problem** — Boot registers `OpenEntityManagerInViewInterceptor` by default (`spring.jpa.open-in-view=true`) so lazy loads can happen during view/JSON rendering **after** the service transaction ends. That keeps the connection open for the whole request and can amplify **N+1** queries.
4. **Security / over-fetch** — password hashes, internal flags, and large graphs leak more easily than a deliberate DTO.

```java
@GetMapping("/users/{id}")
UserResponse get(@PathVariable Long id) {
  return userService.findResponse(id); // map inside @Transactional service
}

public record UserResponse(Long id, String email, String displayName) {}
```

**Listing 1.** Controller returns an API type; mapping happens while the session is still open (or via a projection query).

## Better shapes

| Approach | When |
| --- | --- |
| **Manual map to DTO/record** in the service | Full control; clear API boundary |
| **Interface / class projections** | Spring Data loads only needed attributes |
| **`@Query` + constructor expression** | Explicit JPQL DTO construction |
| **JOIN FETCH / `@EntityGraph`** | Still entity-based — OK for internal use; still prefer DTO at the HTTP edge |

Spring Data Commons/JPA projections exist specifically to return **partial views** outside the entity hierarchy — a first-class alternative to shipping full aggregates to the web layer.

```d2
direction: right
ctrl: "@RestController" {
  style.fill: "#e3f2fd"
}
dto: "DTO / projection" {
  style.fill: "#e8f5e9"
}
svc: "@Transactional service" {
  style.fill: "#fff3e0"
}
em: "EntityManager\nentities stay here" {
  style.fill: "#f3e5f5"
}

ctrl -> dto
dto -> svc -> em
```

**Fig. 1.** Keep entities behind the service; expose only the API model.

> [!warning] OSIV is not an API design strategy
> Leaving `spring.jpa.open-in-view` on so controllers can return entities and “just work” trades correctness theater for longer DB sessions and accidental N+1. Prefer fetch what you need in the transaction, map, then serialize.

> [!tip] Interview answer
> I do not return JPA entities from REST controllers. I map to DTOs or use Spring Data projections so the API is stable, lazy loads stay inside the transaction, and I am not relying on Open Session/EntityManager in View to make Jackson succeed.

See [[What are Spring Data JPA projections]], [[What is Open Session In View in Spring]], [[What is the N plus 1 problem in Spring Data JPA]], and [[What is JOIN FETCH and EntityGraph in Spring Data JPA]].
