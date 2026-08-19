<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

@PostAuthorize runs a SpEL check after the method returns. returnObject is the result. Dump example: only the owner may see the loaded entity:

```
@PostAuthorize("returnObject.owner == authentication.name")
public Employee getEmployee(Long id) { ... }
```

It needs method security (@EnableMethodSecurity / prePostEnabled). The method still executes; denial happens after. @PreAuthorize runs before and can skip the call.
> [!warning] Unverified traps from the dump
> - Side effects already happened if you deny in @PostAuthorize. Use @PreAuthorize when you must not run the method.
