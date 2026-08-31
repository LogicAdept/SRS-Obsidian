<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/SecurityContext #Java/Annotations #SRS

# What is the difference between AuthenticationPrincipal and SecurityContextHolder?

> [!abstract] Short answer
> **`SecurityContextHolder`** is the **static ThreadLocal API** for the full **`Authentication`** (principal **and** credentials, authorities, `isAuthenticated()`). **`@AuthenticationPrincipal`** is a **Spring MVC (and WebFlux) argument resolver**: it injects **`Authentication.getPrincipal()`** into a **controller parameter** so the web layer need not call the holder. A raw **`Principal`** argument is the servlet principal — typically **`getName()`** (username), **not** your `UserDetails` type. The annotation does **not** work on a `@Service` you call yourself and is **not** a substitute for propagating context to **`@Async`**.

## Two APIs, two layers

| | **`SecurityContextHolder`** | **`@AuthenticationPrincipal`** |
|--|--|--|
| What you get | **`SecurityContext` → `Authentication`** | **`getPrincipal()`** only |
| Where | Any code on **that thread** (filters, services, `@PreAuthorize`) | **Controller / `@RequestMapping` method args** (`AuthenticationPrincipalArgumentResolver`) |
| Coupling | Explicit Spring Security static API | Can be wrapped in your own meta-annotation (`@CurrentUser`) so MVC does not import Security types |
| Setup | Always there | Registered with **`@EnableWebSecurity`** (MVC `WebMvcConfigurer`) |

**`@CurrentSecurityContext`** is the sibling annotation that injects the **`SecurityContext`** (or a SpEL slice such as `authentication`) — still MVC, still not the static holder.

```java
Authentication auth = SecurityContextHolder.getContext().getAuthentication();
CustomUser user = (CustomUser) auth.getPrincipal();
```

**Listing 1.** Holder — full `Authentication`; you cast the principal. Works in a `@Service` on the request thread.

```java
@GetMapping("/messages/inbox")
ModelAndView inbox(@AuthenticationPrincipal CustomUser user) {
	// ...
}
```

**Listing 2.** MVC — same principal object, no `SecurityContextHolder` in the controller. SpEL: `@AuthenticationPrincipal(expression = "customUser")` when `UserDetails` wraps your type.

## `Principal` is not `@AuthenticationPrincipal`

A method parameter of type **`java.security.Principal`** is the servlet user (`request.getUserPrincipal()`). With Spring Security that object is usually the **`Authentication`**, but the type you programmed to only guarantees **`getName()`** (the username). It is **not** your `CustomUser`. **`@AuthenticationPrincipal CustomUser`** is the **principal**; **`Authentication`** on a controller argument (via `@CurrentSecurityContext(expression = "authentication")` or a cast) is the **token**.

Controllers: prefer the annotation (docs: **decouple the MVC layer**). Services and async workers: the annotation **never runs** — use the holder, pass the user in, or wrap the executor ([[How do you propagate SecurityContext to async threads]]).

```d2
direction: down
holder: "SecurityContextHolder.getContext()\nAuthentication (full token)" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
principal: "@AuthenticationPrincipal\nAuthentication.getPrincipal()" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}
name: "Principal method arg\ngetName() = username" {
  width: 320
  height: 70
  style.fill: "#fff3e0"
}

holder -> principal
holder -> name
```

**Fig. 1.** Same thread-local `Authentication`; three different views of it.

> [!warning] Wrong type and wrong thread
> **`@AuthenticationPrincipal`** on a parameter whose type does not match `getPrincipal()` yields **`null`** (or fails if **`errorOnInvalidType`**). Tests that plant Security’s **`User`** then break controllers that cast to **`YourUser`**. The resolver still reads **`SecurityContextHolder`** on the **request thread** — **`@Async`** without **`DelegatingSecurityContextExecutor`** sees an empty holder, annotation or not. See [[What is SecurityContextHolder]] and [[What is the purpose of WithMockUser in Spring Security tests]].

> [!tip] Interview answer
> SecurityContextHolder is the static ThreadLocal API for the full Authentication, usable anywhere on that thread. @AuthenticationPrincipal is MVC injection of Authentication.getPrincipal() so controllers stay off the holder. A Principal parameter is only the servlet principal (username via getName()), not your UserDetails. The annotation does not inject into services or @Async workers.
