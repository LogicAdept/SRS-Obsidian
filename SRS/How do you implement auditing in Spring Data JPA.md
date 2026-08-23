<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Annotations #SRS

# How do you implement auditing in Spring Data JPA?

> [!abstract] Short answer
> Enable auditing with `@EnableJpaAuditing`, register `AuditingEntityListener` on entities, annotate audit fields with `@CreatedDate` / `@LastModifiedDate` (and optionally `@CreatedBy` / `@LastModifiedBy`), and provide an `AuditorAware` bean when tracking the current user.

## Enable auditing and annotate fields

Spring Data JPA fills audit metadata on persist and update through `AuditingEntityListener`. Turn the feature on at configuration level, then mark fields on the entity.

```java
@Configuration
@EnableJpaAuditing
class JpaAuditingConfig {

  @Bean
  AuditorAware<String> auditorProvider() {
    return () -> Optional.ofNullable(SecurityContextHolder.getContext())
        .map(SecurityContext::getAuthentication)
        .filter(Authentication::isAuthenticated)
        .map(Authentication::getName);
  }
}
```

**Listing 1.** `@EnableJpaAuditing` registers auditing infrastructure; expose `AuditorAware` for `@CreatedBy` / `@LastModifiedBy` (Spring Data JPA auditing reference).

```java
@Entity
@EntityListeners(AuditingEntityListener.class)
class Article {

  @CreatedDate
  @Column(updatable = false)
  private Instant createdAt;

  @LastModifiedDate
  private Instant updatedAt;

  @CreatedBy
  @Column(updatable = false)
  private String createdBy;

  @LastModifiedBy
  private String modifiedBy;
}
```

**Listing 2.** Per-entity listener registration (alternative: global `AuditingEntityListener` entry in `orm.xml`).

Supported date types include `Instant`, other JDK date/time types, `long`/`Long`, and legacy `Date`/`Calendar`. Timestamps come from a `DateTimeProvider` (default `CurrentDateTimeProvider`). **Date-only auditing does not require `AuditorAware`.**

```d2
direction: right
save: "repository.save(entity)" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
listener: "AuditingEntityListener\nJPA lifecycle" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
fields: "@CreatedDate\n@LastModifiedDate\n@CreatedBy …" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
aware: "AuditorAware\n(current user)" {
  width: 200
  height: 70
  style.fill: "#f3e5f5"
}

save -> listener -> fields
aware -> fields: "@CreatedBy only"
```

**Fig. 1.** Listener runs on persist/update; user fields need a resolvable principal.

## `AuditorAware` and pitfalls

`@CreatedBy` / `@LastModifiedBy` stay empty unless Spring can resolve the current auditor via `AuditorAware<T>` (or `ReactiveAuditorAware` in reactive stacks). The generic `T` must match the field type. With multiple `AuditorAware` beans, set `@EnableJpaAuditing(auditorAwareRef = "…")`.

Auditing requires **`spring-aspects`** on the classpath. It populates fields on entity state transitions through the persistence provider — not when you mutate a detached object without saving. Mark creator columns `updatable = false` so later merges do not overwrite who created the row.

> [!warning] Listener + enable flag both required
> `@CreatedDate` alone does nothing without `@EnableJpaAuditing` and an registered `AuditingEntityListener`. `@CreatedBy` without `AuditorAware` (or outside an authenticated request) leaves nulls — that is expected, not a silent default user.

See [[What is Spring Data JPA]], [[Which Spring Data JPA annotations have you used]], and [[What is the Transactional annotation in Spring Data]].

> [!tip] Interview answer
> I add `@EnableJpaAuditing`, put `@EntityListeners(AuditingEntityListener.class)` on the entity, and use `@CreatedDate` / `@LastModifiedDate` for timestamps. For user tracking I add `@CreatedBy` / `@LastModifiedBy` plus an `AuditorAware` bean, usually reading Spring Security’s authentication. Date auditing alone does not need `AuditorAware`.
