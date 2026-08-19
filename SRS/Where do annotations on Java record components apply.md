<!--
reps: 0
priority: 0
-->
#Java/Language/Records #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: an annotation on a header component is applied to the field, the constructor parameter, and the accessor.

```java
public record User(
    @JsonProperty("user_name") @NonNull String name,
    @Min(0) @Max(150) int age
) {}
```

For narrower placement, dumps mention meta-annotations `@Target({FIELD, METHOD, PARAMETER})`.

Bean Validation on record DTOs (`@NotBlank`, `@Email`, `@Min`) appears in Spring controller examples next to a compact constructor for extra checks.

> [!warning] Unverified traps from the dump
> - Whether a given annotation type actually lands on all three sites depends on its `@Target` — the dump’s “always all three” claim needs a check.
