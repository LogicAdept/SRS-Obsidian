<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Framework/Testing #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: @WithMockUser builds a fake User with the given username/roles — no UserDetailsService. @WithUserDetails(username) loads the real UserDetails from the test context’s UserDetailsService.

Use WithMockUser for unit method-security tests; WithUserDetails when account flags or custom UserDetails matter.
> [!warning] Unverified traps from the dump
> - WithUserDetails fails if that username is not in the test UserDetailsService. WithMockUser never calls the service.
