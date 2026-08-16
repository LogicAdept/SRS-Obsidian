<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**MVC vs WebFlux vs virtual threads?**

MVC (Servlet, Tomcat): blocking, simple, default. WebFlux (Netty, reactive): many concurrent idle I/O connections, streaming; do not mix blocking JDBC on event loop. Java 21 virtual threads (spring.threads.virtual.enabled): keep MVC/blocking style with cheap threads — often better than rewriting to WebFlux. Interview: WebFlux is not 'faster CRUD'.
