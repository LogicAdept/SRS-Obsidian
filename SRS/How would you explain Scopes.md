<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Scopes бина.**

singleton (default — один на контекст), prototype (новый при каждом запросе), request (один на HTTP-запрос), session, application, websocket. Важно: инжект prototype в singleton через Provider<T> или ObjectFactory<T>, иначе prototype-бин создастся один раз.

**Scopes бина.**

singleton (default — один на контекст), prototype (новый при каждом запросе), request, session, application, websocket.
