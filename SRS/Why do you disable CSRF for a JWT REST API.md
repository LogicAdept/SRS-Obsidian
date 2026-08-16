<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Security #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**CSRF vs CORS vs JWT?**

CSRF: browser cookie auth + cross-site form/POST. JWT in Authorization header is not sent automatically by foreign sites → CSRF often disabled; still use CSRF for cookie-session apps. CORS: which origins may call your API from a browser; configure in Security (CorsFilter), not only @CrossOrigin. POST 403 after Boot 3: often CSRF still on.
