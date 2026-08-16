<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Stub vs Verify в WireMock.**

Stub: настроить фиксированный ответ — stubFor(get("/api/rates").willReturn(okJson(...))). Verify: проверить, что наш сервис сделал ожидаемый запрос — verify(getRequestedFor(urlEqualTo("/api/rates")).withHeader("X-Api-Key", equalTo("secret"))). Scenarios: стейт-машина — 1-й запрос → 500, 2-й → 200 (тест retry).
