<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Где передавать данные: body / path / query / headers?**

Path: идентификатор ресурса (/users/123). Query: фильтрация, пагинация (?page=2&sort=name). Body: данные для создания/обновления (POST/PUT/PATCH). Headers: метаданные (Authorization, Content-Type, Accept). НЕ в URL: пароли, токены, персональные данные.
