<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump FilterChainProxy sketch: when a SecurityFilterChain matches, FilterChainProxy does not register those filters with Tomcat. It wraps them in a VirtualFilterChain that runs the security filters then continues the servlet FilterChain toward DispatcherServlet.
> [!warning] Unverified traps from the dump
> - Debugging in FilterChainProxy is the dump starting point because VirtualFilterChain is what actually iterates getFilters().
