<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@MatrixVariable` binds matrix variables from a URI path segment (`/cars/ford;year=2020`).

```java
@GetMapping("/cars/{make}")
public String getCars(@PathVariable String make, @MatrixVariable int year) { ... }
```

> [!warning] Unverified traps from the dump
> - Matrix variables are disabled unless you enable them on the RequestMappingHandlerMapping (dumps often omit this).
