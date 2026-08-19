<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@CookieValue` binds an HTTP cookie to a handler parameter.

```java
@RequestMapping("/showCookie")
public String showCookie(@CookieValue("myCookie") String cookieValue) { ... }
```

> [!warning] Unverified traps from the dump
> - Missing cookies fail unless required=false or a defaultValue is set (same pattern as @RequestParam).
