<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump (non-Boot war): subclass AbstractSecurityWebApplicationInitializer so the container registers DelegatingFilterProxy / springSecurityFilterChain without web.xml.

```
public class SpringSecurityInitializer extends AbstractSecurityWebApplicationInitializer {}
```

Boot’s embedded container and SecurityFilterAutoConfiguration usually make this class unnecessary.
> [!warning] Unverified traps from the dump
> - An empty initializer still needs a SecurityFilterChain / @EnableWebSecurity config class on the classpath.
