<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Session fixation: attacker plants a session id, victim logs in, attacker reuses that id. Dumps migrate the session after login:

```java
http.sessionManagement().sessionFixation().migrateSession();
```

Other dump options: newSession() (fresh id, attributes dropped) or none() (do not change id — generally wrong for cookie sessions).
> [!warning] Unverified traps from the dump
> - Spring Security enables session-fixation protection by default; dumps that ‘add’ migrateSession are often restating the default.
> - STATELESS APIs have no servlet session to migrate.
