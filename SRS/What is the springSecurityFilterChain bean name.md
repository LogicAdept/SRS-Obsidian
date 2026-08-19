<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The FilterChainProxy that intercepts requests is registered under the bean name springSecurityFilterChain. DelegatingFilterProxy in the servlet container looks up exactly that name and delegates into Spring.

That name is the dump’s certification-style fill-in. Individual SecurityFilterChain beans sit behind this one proxy.
> [!warning] Unverified traps from the dump
> - Renaming the DelegatingFilterProxy filter-name away from springSecurityFilterChain breaks the lookup unless you set targetBeanName.
