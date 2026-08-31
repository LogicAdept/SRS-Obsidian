<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Data #SRS

# What is SecurityEvaluationContextExtension?

> [!abstract] Short answer
> **A Spring Data `EvaluationContextExtension` that exposes the current `Authentication` as SpEL inside `@Query`.** Add `spring-security-data` and register the bean. Then `?#{ principal?.id }` (and the other common security expressions) bind from `SecurityContextHolder`. It is **not** `@PreAuthorize` / `@PostFilter` — the predicate runs **in the query**, which is what paging needs.

## Security root inside Spring Data SpEL

Package: `org.springframework.security.data.repository.query.SecurityEvaluationContextExtension` (since **4.0**). It implements Spring Data’s `EvaluationContextExtension`. Default constructor reads `Authentication` from `SecurityContextHolder` on each evaluation. A second constructor pins a fixed `Authentication` (tests). `getRootObject()` is a `SecurityExpressionRoot`, so `principal`, `authentication`, `hasRole`, `hasPermission`, … are the same names as method-security SpEL. Extension id: `security`.

Official 7.1: without filtering **in the query**, `@PostFilter` after a paged fetch does not scale. This bean is the documented way to put the user in JPQL/SQL SpEL.

`principal?.id` assumes you customized the principal to an object **with an `id` property**. Stock `UserDetails` has `username`, not `id`. Dump form `?#{principal.username}` is the `UserDetails` spelling. Safe navigation `?.` avoids a NPE when `principal` is null.

`hasPermission` in a query still hits this extension’s `PermissionEvaluator` (default `DenyAllPermissionEvaluator`) unless you `setPermissionEvaluator`. That is **not** auto-wired from `@EnableMethodSecurity`.

```java
@Bean
SecurityEvaluationContextExtension securityEvaluationContextExtension() {
    return new SecurityEvaluationContextExtension();
}
```

**Listing 1.** Conceptual Security **7.1** — also valid as an XML bean of this class. Need the `spring-security-data` module on the classpath.

```java
public interface MessageRepository extends PagingAndSortingRepository<Message, Long> {

    @Query("select m from Message m where m.to.id = ?#{ principal?.id }")
    Page<Message> findInbox(Pageable pageable);
}
```

**Listing 2.** Conceptual — `Authentication.getPrincipal().getId()` must exist. This is **not** `@PostFilter` on a service method.

```d2
direction: down
ctx: "SecurityContextHolder\nAuthentication" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
ext: "SecurityEvaluationContextExtension\nSecurityExpressionRoot" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
q: "@Query ?#{ principal?.id }" {
  width: 240
  height: 45
  style.fill: "#c8e6c9"
}

ctx -> ext
ext -> q
```

**Fig. 1.** Query-time SpEL, not a method interceptor. See [[Why is PostFilter a performance trap]], [[What is authentication in method-security SpEL]], [[What is PreFilter and PostFilter in Spring Security]], [[What is hasPermission in Spring Security method expressions]].

> [!warning] No bean, no security in `?#{}`
> Spring Data does not see `principal` until this extension is a bean. `@EnableMethodSecurity` does **not** register it. `principal.id` on a plain `User` / `UserDetails` fails — there is no `id` unless you put one on the principal. `@PostFilter` still loads the page then drops rows; this extension is the query-level alternative.

> [!tip] Interview answer
> `SecurityEvaluationContextExtension` is a Spring Data SpEL extension from `spring-security-data`. You register it as a bean so `@Query` can use `?#{ principal?.id }` and the usual security expressions from the `SecurityContext`. It is how you filter by the current user in the database instead of `@PostFilter` after the fact. It is not method security — `@EnableMethodSecurity` does not create this bean.
