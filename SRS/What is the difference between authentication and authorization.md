<!--
reps: 0
priority: 0
-->
#Security/Authentication #Security/Authorization #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**AuthN vs AuthZ in Spring Security?**

Authentication: establish identity (JWT/session/login). Authorization: Filter Security + @PreAuthorize. 401 unauthenticated, 403 authenticated but forbidden.
