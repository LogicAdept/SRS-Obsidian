<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #API/REST #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**How do you version a Spring REST API?**

URI (/v1/orders), header (Accept-version / custom), media type (application/vnd.x.v1+json). URI is simplest and most common in interviews. Don't break existing clients; deprecate with overlap. Pair with ProblemDetail error shape.
