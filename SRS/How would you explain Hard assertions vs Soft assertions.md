<!--
reps: 0
priority: 0
-->
#Java/Testing/JUnit #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Hard assertions vs Soft assertions.**

Hard (по умолчанию): при первом assertFalse тест падает, остальные проверки не выполняются. Soft (assertAll в JUnit 5, SoftAssertions в AssertJ): все проверки выполняются, ошибки собираются. Для AQA: Soft assertions для проверки нескольких полей ответа — увидеть ВСЕ ошибки за один запуск.
