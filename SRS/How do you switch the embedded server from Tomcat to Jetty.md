<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Embedded #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Default with `spring-boot-starter-web` is Tomcat. To switch: exclude `spring-boot-starter-tomcat` from `starter-web` and add `spring-boot-starter-jetty` or `spring-boot-starter-undertow`.

> [!warning] Unverified traps from the dump
> - Leaving Tomcat on the classpath next to Jetty is how you get two servers or a surprise Tomcat.
