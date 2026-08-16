<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Boot #Java/Concurrency #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**Virtual threads in Boot 3.2+?**

Java 21+, spring.threads.virtual.enabled=true — Tomcat/Jetty use virtual threads for requests. Keep blocking I/O; avoid pinning (synchronized around blocking in older JDKs). Not a substitute for measuring. Don't use huge platform thread pools 'just in case' on top.
