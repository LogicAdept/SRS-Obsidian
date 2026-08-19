<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: put `@EnableAspectJAutoProxy` on a `@Configuration` class (XML equivalent: `<aop:aspectj-autoproxy/>`).

```java
@Configuration
@EnableAspectJAutoProxy
public class AppConfig {}
```

Aspect classes still need to be Spring beans (`@Component` + scan, or `@Bean`). Boot: if `spring-boot-starter-aop` is on the classpath, auto-config enables AOP.

> [!warning] Unverified traps from the dump
> - @EnableAspectJAutoProxy needs aspectjweaver on the classpath (dump/API claim).
> - It applies to the local ApplicationContext only; a second web context may need its own declaration.
