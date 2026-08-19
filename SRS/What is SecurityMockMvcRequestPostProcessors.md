<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Spring/Framework/Testing #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump MockMvc testing: SecurityMockMvcRequestPostProcessors (csrf(), user(), httpBasic()) as request post-processors so a test POST carries a CSRF token or a fake user without @WithMockUser on the method.

Together with springSecurity() on MockMvc setup.
> [!warning] Unverified traps from the dump
> - Forgetting csrf() on MockMvc POST is a 403 even when the test user is correct.
