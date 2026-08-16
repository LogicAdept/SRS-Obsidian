<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**@ControllerAdvice vs @RestControllerAdvice?**

Both global exception handling / init binders. @RestControllerAdvice = @ControllerAdvice + @ResponseBody, so return values are serialized (JSON), not view names. Use RestControllerAdvice for APIs; ControllerAdvice if some handlers return views.
