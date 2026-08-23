<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #SRS

# What technologies does Spring Data build upon?

> [!abstract] Short answer
> Spring Data sits on **Spring Framework** (IoC, configuration, transactions, AOP-style proxies) and on each module’s **underlying data-access technology** — for example **Jakarta Persistence (JPA)** / a provider, the **MongoDB** or **Redis** drivers, **JDBC/R2DBC**, Cassandra, and so on. Commons supplies the shared repository model; store modules keep the traits of that backend.

## Two layers underneath

**1. Spring Framework**  
Commons’ own preface: it applies **core Spring concepts** to data-access across relational and non-relational stores. Repository beans are Spring-managed proxies; you get familiar DI, `@Enable*Repositories`, and integration with Spring’s transaction model where the store supports it. Current Commons docs require a modern Spring Framework line (e.g. 6.x for recent trains).

**2. The store / driver stack**  
spring.io describes the mission as a consistent Spring programming model **while retaining the special traits of the underlying data store**. Examples:

| Module | Builds on |
| --- | --- |
| Spring Data JPA | JPA API + provider (often Hibernate in Boot) |
| Spring Data MongoDB | MongoDB Java / Reactive Streams drivers |
| Spring Data Redis | Redis + Spring Data Redis connection factories |
| Spring Data JDBC / R2DBC | JDBC or R2DBC |
| Spring Data REST | Your Spring Data repositories + Spring MVC/Web |

```d2
direction: down
app: "Your repositories\n& domain model" {
  style.fill: "#e3f2fd"
}
sd: "Spring Data module\n(JPA / Mongo / …)" {
  style.fill: "#fff3e0"
}
sf: "Spring Framework\nDI · tx · proxies" {
  style.fill: "#e8f5e9"
}
store: "Store API / driver\nJPA · Mongo · Redis · JDBC…" {
  style.fill: "#f3e5f5"
}

app -> sd
sd -> sf
sd -> store
```

**Fig. 1.** Application code talks Spring Data; that layer uses Spring and the concrete store technology.

## What that means in practice

Spring Data does **not** replace JPA, MongoDB, or Redis. It **orchestrates** them: derived queries become JPQL or Mongo queries; `save` goes through `EntityManager` or the document template; Redis modules still speak Redis commands under templates/repositories.

> [!warning] You still need the store skills
> Knowing Spring Data repositories is not enough when indexes, transactions, mapping quirks, or driver options matter — those come from the underlying technology the module wraps.

> [!tip] Interview answer
> Spring Data builds on Spring Framework for beans, configuration, and transactions, and on each store’s native stack — JPA/Hibernate, MongoDB drivers, Redis, JDBC, and so on. Commons is the shared repository abstraction; modules keep store-specific behavior.

See [[What is the Spring Data umbrella project]], [[What is Spring Data Commons]], [[Why do you need Spring Data]], and [[What is the difference between Spring Data JPA and using Hibernate directly]].
