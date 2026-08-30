<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

rememberMe() issues a token so the browser can stay logged in after the session dies. Dump config:

```java
http.formLogin().permitAll()
    .and()
    .rememberMe().key("uniqueAndSecret");
```

Simple hash tokens use a shared key; persistent tokens store series/token in a database (PersistentTokenRepository) so a stolen cookie can be revoked.
> [!warning] Unverified traps from the dump
> - A guessable remember-me key lets attackers forge tokens.
> - Remember-me is a session-cookie feature; it does not replace JWT on a STATELESS API.
