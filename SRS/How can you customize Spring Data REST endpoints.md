<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #API/REST #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps list:

- Hide methods with @RestResource(exported = false).
- Hide a whole repository with @RepositoryRestResource(exported = false).
- Add a normal @RestController on the same base path to override or extend behavior.
- Use event handlers (AbstractRepositoryEventListener) to validate or change data before save or delete through the REST API.
> [!warning] Unverified traps from the dump
> - Export false is not the same as Spring Security; it only removes the HTTP resource.
> - Generated CRUD is still there unless you hide or override it.
