<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps do it in `@InitBinder` with `CustomDateEditor`:

```java
@InitBinder
protected void initBinder(WebDataBinder binder) {
    SimpleDateFormat dateFormat = new SimpleDateFormat("dd/MM/yyyy");
    binder.registerCustomEditor(Date.class, new CustomDateEditor(dateFormat, false));
}
```

Alternatively register a `Formatter` / `Converter` on `WebMvcConfigurer`.

> [!warning] Unverified traps from the dump
> - java.time types usually use @DateTimeFormat, not CustomDateEditor (which targets java.util.Date).
