<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump default order (~850): DefaultLogoutPageGeneratingFilter auto-generates a logout confirmation page when you use the default logout setup, sibling of DefaultLoginPageGeneratingFilter.
> [!warning] Unverified traps from the dump
> - A custom logoutSuccessUrl / SPA usually never hits this generated HTML page.
