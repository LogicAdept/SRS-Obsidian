<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**What changed in Spring Boot 3 / Framework 6?**

Java 17 baseline, javax.* → jakarta.* (Servlet, JPA, Validation). Spring Security 6: no WebSecurityConfigurerAdapter, SecurityFilterChain bean, lambda DSL. AOT/native image support, Observability (Micrometer Observation), ProblemDetail, RestClient. Hibernate 6. Breaking for any javax import and old security config.
