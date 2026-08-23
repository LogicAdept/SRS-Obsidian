<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Spring/Framework/WebMvc #SRS

# What is Open Session In View in Spring?

> [!abstract] Short answer
> **Open Session / EntityManager in View (OSIV)** keeps a Hibernate **`Session`** or JPA **`EntityManager`** bound to the thread for the **whole web request**, so lazy associations can still load during view or JSON rendering **after** the service `@Transactional` method has finished. Spring Boot enables the JPA form by default via **`OpenEntityManagerInViewInterceptor`** (`spring.jpa.open-in-view=true`).

## What it does

Spring Framework’s `OpenEntityManagerInViewInterceptor` binds an `EntityManager` for the entire request so lazy loading works in the view layer even though the original service transaction already completed. The older Hibernate name is **Open Session in View** (`OpenSessionInViewFilter` / interceptor); with JPA you hear **Open EntityManager in View** — same pattern.

```d2
direction: right
req: "HTTP request" {
  style.fill: "#e3f2fd"
}
svc: "Service @Transactional\n(commits)" {
  style.fill: "#fff3e0"
}
view: "Controller / Jackson / view\nlazy loads still possible" {
  style.fill: "#fce4ec"
}
em: "EM/Session open\nuntil request ends" {
  style.fill: "#e8f5e9"
}

req -> svc -> view
em -> svc
em -> view
```

**Fig. 1.** Persistence context outlives the service transaction for the rest of the request.

Boot (web apps): registers that interceptor unless you set:

```properties
spring.jpa.open-in-view=false
```

**Listing 1.** Disable OSIV (Spring Boot SQL / JPA reference).

## Why teams disable it

- **Hides missing fetch plans** — N+1 shows up as “it works in prod with OSIV” until someone turns it off and gets `LazyInitializationException`.
- **Holds a DB connection** across controller work and response writing, not only the transactional service call.
- Encourages returning **entities** to the web layer and letting serializers drive SQL.

Preferred style: fetch or project what you need **inside** `@Transactional`, map to a **DTO**, return that; leave OSIV off for APIs.

> [!warning] Default-on is not an endorsement for REST
> Boot documents the default for **lazy loading in web views**. For JSON APIs, treating OSIV as the fetch strategy is a common interview trap — disable it and fix loading explicitly.

> [!tip] Interview answer
> OSIV keeps the Session/EntityManager open for the whole request so lazies work in the view after the service transaction ends. Boot turns Open EntityManager in View on by default (`spring.jpa.open-in-view`). I disable it for APIs, load or project inside the transaction, and return DTOs so I do not depend on request-scoped lazy loads.

See [[Should you return JPA entities from a Spring controller]], [[What is the N plus 1 problem in Spring Data JPA]], and [[How does the Hibernate first-level cache work in Spring]].
