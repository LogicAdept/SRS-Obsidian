<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps wire ldapAuthentication() on AuthenticationManagerBuilder: context URL, user search base/filter, group search base/filter.

```java
auth.ldapAuthentication()
    .contextSource().url("ldap://localhost:8389/dc=springframework,dc=org")
    .and()
    .userSearchBase("ou=people")
    .userSearchFilter("(uid={0})")
    .groupSearchBase("ou=groups")
    .groupSearchFilter("member={0}");
```

Spring maps LDAP groups to GrantedAuthority. There is also an Active Directory-specific provider in some dumps.
> [!warning] Unverified traps from the dump
> - AuthenticationManagerBuilder / WebSecurityConfigurerAdapter is the old API; later apps expose an AuthenticationManager / LdapBindAuthenticationManagerFactory bean.
