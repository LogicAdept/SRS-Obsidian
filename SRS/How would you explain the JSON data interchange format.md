<!--
reps: 0
priority: 0
-->
#DataFormats/JSON #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Content-Type: json vs form-urlencoded vs multipart.**

application/json: JSON в body (REST API). application/x-www-form-urlencoded: пары key=value (формы логина). multipart/form-data: для загрузки файлов (binary + metadata). Для AQA: в Rest Assured — contentType(JSON) для API, contentType("multipart/form-data") для file upload.
