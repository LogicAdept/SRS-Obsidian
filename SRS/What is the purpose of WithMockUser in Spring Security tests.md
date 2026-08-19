<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Annotations #Java/Spring/Framework/Testing #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

@WithMockUser puts a fake authenticated user on the SecurityContext for a test so MockMvc (or a method-security test) does not need a real login.

```java
@Test
@WithMockUser(username = "user", roles = {"USER"})
void testUserEndpoint() throws Exception {
    mockMvc.perform(get("/user")).andExpect(status().isOk());
}
```

Dumps also mention @WithUserDetails when you need the real UserDetailsService lookup.
> [!warning] Unverified traps from the dump
> - roles = {"USER"} becomes ROLE_USER. authorities = {"USER"} does not add the prefix.
> - @WithMockUser does not run your AuthenticationProvider; it skips credential checks.
