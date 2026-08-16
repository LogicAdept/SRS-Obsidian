<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**Front controller recap?**

Single servlet entry: HandlerMapping → interceptor → controller → converters. Boot registers it via auto-config (no web.xml).
