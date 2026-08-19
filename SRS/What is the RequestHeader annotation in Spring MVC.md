<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@RequestHeader` binds an HTTP header to a handler parameter.

```java
@RequestMapping("/showHeader")
public String showHeader(@RequestHeader("User-Agent") String userAgent) { ... }
```

> [!warning] Unverified traps from the dump
> - A Map or HttpHeaders parameter can receive all headers.
