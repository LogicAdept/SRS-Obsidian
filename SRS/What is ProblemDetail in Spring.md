<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #API/REST #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**What is ProblemDetail (RFC 7807)?**

Boot 3 / Framework 6 standard error body: type, title, status, detail, instance. @ControllerAdvice can return ProblemDetail or ErrorResponse. Replaces ad-hoc {error, message} JSON. Interviewers ask why it matters for API clients.
