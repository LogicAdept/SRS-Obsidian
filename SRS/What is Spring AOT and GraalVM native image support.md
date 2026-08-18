<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**AOT vs native image?**

AOT: Spring processes bean definitions at build time (hints for reflection/proxies). Native image (GraalVM): closed-world binary, fast startup, low RSS, worse warmup/peak and harder reflection. AOT is not automatically 'faster JVM app'. Use native for CLI/serverless/scale-to-zero; JVM for long-lived high throughput unless measured otherwise.
