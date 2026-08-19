<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #Java/Annotations #API/REST #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Use @RestResource(exported = false) on a repository method to keep it off the REST API. Use @RepositoryRestResource(exported = false) to hide the entire repository.

Finder methods that stay exported are reached under /search/methodName.
> [!warning] Unverified traps from the dump
> - The Java method still exists for injection; only the HTTP export is removed.
> - collectionResourceRel and path still apply to repositories that remain exported.
