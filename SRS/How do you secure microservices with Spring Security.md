<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/OAuth2 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: OAuth2 + JWT. Each service validates the token and reads the user. Legacy sample:

```
@EnableResourceServer
public class ResourceServerConfig extends ResourceServerConfigurerAdapter {
    public void configure(HttpSecurity http) {
        http.authorizeRequests()
            .antMatchers("/public/**").permitAll()
            .anyRequest().authenticated();
    }
}
```

Current dumps do oauth2ResourceServer().jwt() on a SecurityFilterChain instead.
> [!warning] Unverified traps from the dump
> - @EnableResourceServer / ResourceServerConfigurerAdapter are the old spring-security-oauth2 API.
