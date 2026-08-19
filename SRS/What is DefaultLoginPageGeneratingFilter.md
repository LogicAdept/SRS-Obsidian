<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump request walkthrough: if the user is anonymous, filters such as AuthorizationFilter and DefaultLoginPageGeneratingFilter send them to the default login page.

That generated page is what you get from formLogin() without loginPage(...). A custom loginPage turns this filter off for that flow.
> [!warning] Unverified traps from the dump
> - REST clients hitting this filter get HTML, not 401, unless you replace the AuthenticationEntryPoint.
