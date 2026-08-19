<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Add the Thymeleaf Spring Security dialect (dumps name thymeleaf-extras-springsecurity5) and the sec namespace. Templates can hide markup by expression:

```html
<div sec:authorize="hasRole('ROLE_USER')">Welcome, user!</div>
<div sec:authorize="isAuthenticated()">Welcome, authenticated user!</div>
```

The dialect reads the current SecurityContext; it does not replace URL or method security.
> [!warning] Unverified traps from the dump
> - The extras artifact version must match Thymeleaf / Spring Security (security5 vs security6 naming in dumps).
> - sec:authorize only affects rendering. You still need server-side authorization.
