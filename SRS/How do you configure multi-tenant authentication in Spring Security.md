<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump recipe: a custom Authentication that carries a tenant id (CustomAuthenticationToken extends UsernamePasswordAuthenticationToken) and a MultiTenantAuthenticationProvider whose authenticate() reads getTenant() and looks up users in that tenant’s store.

supports() must accept only that token type. Register the provider on AuthenticationManagerBuilder (old) or as a ProviderManager bean.
> [!warning] Unverified traps from the dump
> - A shared UserDetailsService with no tenant column will leak users across tenants.
