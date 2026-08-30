<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

ProviderManager walks a list of AuthenticationProvider. Dumps register several on AuthenticationManagerBuilder, for example in-memory and JDBC together, or a custom provider plus DaoAuthenticationProvider.

Each provider’s supports(Class) decides whether it tries the Authentication. First success wins; if none can decide, authentication fails (or the parent manager is tried).
> [!warning] Unverified traps from the dump
> - Order matters: a provider that always ‘supports’ username/password can shadow LDAP or JWT.
> - Returning null from authenticate means ‘I cannot decide’; throwing AuthenticationException means ‘credentials are wrong’.
