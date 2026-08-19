<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/OAuth2 #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Legacy dump annotation @EnableResourceServer plus ResourceServerConfigurerAdapter makes the app an OAuth2 resource server (validate access tokens, authorizeRequests on /public vs authenticated).

Spring Security 5.2+ / Boot 3 dumps use http.oauth2ResourceServer(oauth2 -> oauth2.jwt()) and issuer-uri instead.
> [!warning] Unverified traps from the dump
> - Do not mix @EnableResourceServer with the new oauth2ResourceServer DSL in one app without knowing which filter chain wins.
