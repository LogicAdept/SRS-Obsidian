<!--
reps: 0
priority: 0
-->
#API/REST #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Структура теста Rest Assured.**

given() — настройка запроса (headers, body, params). when() — HTTP-метод + URL. then() — проверки (statusCode, body). extract() — извлечение данных из ответа. RequestSpecification — переиспользование общей конфигурации (baseUri, auth, content-type).
