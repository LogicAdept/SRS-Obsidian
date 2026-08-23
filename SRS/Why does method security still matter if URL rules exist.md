<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #SRS

# Why does method security still matter if URL rules exist?

> [!abstract] Short answer
> **`authorizeHttpRequests` / filter-chain rules guard the HTTP boundary only.** **`@PreAuthorize` and related method-security annotations protect the service method itself**, no matter who calls it — MVC controller, scheduled job, message listener, or test — and can use **parameters and return values** in the decision.

## Two layers, different scope

| Layer | What it protects | Typical config |
|---|---|---|
| **Web / request** | Incoming HTTP URLs and verbs | `SecurityFilterChain`, `authorizeHttpRequests` |
| **Method** | Spring-managed bean methods | `@EnableMethodSecurity`, `@PreAuthorize`, … |

Spring Security’s method-authorization docs list **enforcing security at the service layer** as a core use case, alongside fine-grained rules where **method arguments and return values** matter (for example **`@PostAuthorize("returnObject.owner == authentication.name")`**).

URL rules stop anonymous callers from hitting **`GET /admin`**. They do **not** stop an authenticated user from invoking **`adminService.deleteUser(id)`** through another entry point if that service method is reachable without a method check.

```d2
direction: right
http: "HTTP filter chain\nauthorizeHttpRequests" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
svc: "@Service method\n@PreAuthorize" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}
other: "Scheduler / listener\n(no HTTP)" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}

http -> svc: "controller may call"
other -> svc: "still checked\nby method security"
```

**Fig. 1.** Method security follows the business method, not only the web adapter.

```java
@Service
public class AccountService {

    @PreAuthorize("hasAuthority('account:read')")
    @PostAuthorize("returnObject.owner == authentication.name")
    public Account readAccount(String id) {
        return repository.findById(id);
    }
}
```

**Listing 1.** Method security can inspect identity and the returned object — logic that URL patterns alone cannot express.

## Defense in depth, not either/or

Method security is **not a substitute** for web-layer rules. Public endpoints still need **`SecurityFilterChain`** configuration (authentication, CSRF, headers). Method annotations add **defense in depth** so internal calls cannot bypass business authorization just because no HTTP matcher applied.

> [!warning] Non-HTTP callers must handle denial
> When a secured method runs **outside an HTTP request**, Spring Security may throw **`AccessDeniedException`** without an **`ExceptionTranslationFilter`** to translate it into 403. Callers (jobs, messaging, tests) need explicit handling. See [[What is EnableMethodSecurity]] and [[At what levels can Spring Security enforce access control]].

> [!tip] Interview answer
> URL rules only secure the web perimeter. Method security secures the service method for every caller and supports SpEL on parameters and return values. Use both: filter chain for HTTP, @PreAuthorize for business operations.
