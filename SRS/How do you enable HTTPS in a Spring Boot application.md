<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Embedded #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Configure the embedded server’s SSL in `application.properties` and put the keystore on the classpath (for example `src/main/resources/keystore.p12`):

```properties
server.port=8443
server.ssl.key-store=classpath:keystore.p12
server.ssl.key-store-password=password
server.ssl.key-store-type=PKCS12
```

> [!warning] Unverified traps from the dump
> - Password in properties is a secret — dumps show it inline; production uses env / a secret store.
> - HTTP on 8080 and HTTPS on 8443 together need extra connector config the dump does not show.
