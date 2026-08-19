<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

SecurityEvaluationContextExtension (spring-security-data) exposes the current Authentication to SpEL in Spring Data queries (and similar evaluation contexts).

Register it as an EvaluationContextExtension bean, then in a repository:

```
@Query("select u from User u where u.username = ?#{principal.username}")
User findCurrentUser();
```

That binds principal.username from the SecurityContext into the query.
> [!warning] Unverified traps from the dump
> - Without this extension, ?#{principal.username} in a repository query does not see Spring Security.
