<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

HTTP Basic sends username:password on every request in the Authorization header, Base64-encoded (not encrypted). Spring Security validates those credentials before the controller runs.

Dump recipe: require authentication on requests and enable httpBasic():

```java
http.authorizeRequests().anyRequest().authenticated().and().httpBasic();
```

Later dumps use a SecurityFilterChain bean and http.httpBasic(Customizer.withDefaults()).
> [!warning] Unverified traps from the dump
> - Base64 is encoding, not encryption. Without TLS the password is visible.
> - Dumps still show WebSecurityConfigurerAdapter; Boot 3 / Security 6 use SecurityFilterChain.
