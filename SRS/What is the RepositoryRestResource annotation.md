<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #Java/Annotations #API/REST #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

@RepositoryRestResource customizes how Spring Data REST exports a repository: collectionResourceRel and path set the JSON rel and URL path (dump: people).

exported = false on the annotation hides the whole repository. On a method, @RestResource(exported = false) hides that method.
> [!warning] Unverified traps from the dump
> - Hiding the repository is exported = false on @RepositoryRestResource, not on @RestController.
> - Custom @RestController mappings on the same path are the dump's way to override generated endpoints.
