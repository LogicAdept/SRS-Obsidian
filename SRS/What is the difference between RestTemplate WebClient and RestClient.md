<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**RestTemplate vs WebClient vs RestClient?**

RestTemplate: blocking, maintenance mode, still in many codebases. WebClient: reactive, also usable blocking via .block() (discouraged on event loop). RestClient (Boot 3.2 / Framework 6.1): modern blocking fluent API, successor to RestTemplate. For MVC+virtual threads prefer RestClient; for reactive stacks WebClient.
