<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Annotations #Java/Spring/Framework/Testing #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps pair @WithMockUser with @WithUserDetails. @WithUserDetails looks the user up through the real UserDetailsService (full UserDetails, custom fields). @WithMockUser synthesizes a user and skips the service.

Use on a @WebMvcTest / @SpringBootTest method with MockMvc.
> [!warning] Unverified traps from the dump
> - @WithUserDetails fails if that username is not in the test UserDetailsService. @WithMockUser never hits the database.
