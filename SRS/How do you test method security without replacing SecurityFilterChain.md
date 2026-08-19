<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Framework/Testing #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: @WithMockUser (or @WithUserDetails) on the test method simulates a user so you do not hit a real provider. Use @AutoConfigureMockMvc / @SpringBootTest.

Do not put a permit-all SecurityFilterChain in @TestConfiguration — it overrides production and tests pass while prod returns 401. Prefer @ActiveProfiles("test") and profile-specific config.
> [!warning] Unverified traps from the dump
> - Tests that call the real OAuth2 server fail in CI without network. @WithMockUser avoids that.
