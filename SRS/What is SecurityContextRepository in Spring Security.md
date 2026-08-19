<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

SecurityContextRepository loads and saves SecurityContext across requests: loadContext, saveContext, containsContext.

Default for servlet apps is HTTP session (HttpSessionSecurityContextRepository). Stateless JWT dumps use a repository that does not persist (NullSecurityContextRepository / STATELESS) so the context is rebuilt each request from the token.

A custom repository is how you keep the context somewhere other than the servlet session.
> [!warning] Unverified traps from the dump
> - STATELESS without a repo that skips the session still surprises people who expect JSESSIONID.
> - Spring Security 6 also has SecurityContextHolderFilter vs the older SecurityContextPersistenceFilter naming in dumps.
