<!--
reps: 0
priority: 0
-->
#DataFormats/XML #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**JSON Schema validation — зачем?**

Проверяет структуру ответа (типы полей, обязательные поля, формат). body(matchesJsonSchemaInClasspath("schemas/user.json")). Защищает от непредвиденных изменений API-контракта. Генерация схемы: jsonschema.net или из Swagger/OpenAPI.
