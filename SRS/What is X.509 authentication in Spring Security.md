<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: X.509 is certificate authentication. The usual story is the browser checking the *server* certificate on HTTPS against trusted CAs. Spring Security also has an X.509 module that can extract a client certificate and map it to a UserDetails user.

It is listed as a first-class mechanism next to form login and OAuth2.
> [!warning] Unverified traps from the dump
> - Dump text often describes server TLS, not mutual TLS client certs. Client X.509 needs the container to request a client certificate.
