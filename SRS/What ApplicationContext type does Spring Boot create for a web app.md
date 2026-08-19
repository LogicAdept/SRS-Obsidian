<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Embedded #Java/Spring/Core/IoC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Depends on application type. MVC dumps: `AnnotationConfigServletWebServerApplicationContext` (starts the embedded servlet container). WebFlux: `AnnotationConfigReactiveWebServerApplicationContext`. Non-web: plain `AnnotationConfigApplicationContext` (no server).

Boot picks the type by inspecting the classpath.

> [!warning] Unverified traps from the dump
> - A leftover `starter-web` on the classpath is why a 'batch' app still starts Tomcat.
