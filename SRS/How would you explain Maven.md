<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Жизненный цикл Maven.**

validate → compile → test → package → verify → install → deploy. mvn test: прогоняет unit-тесты (Surefire plugin). mvn verify: прогоняет интеграционные (Failsafe plugin). Scope: compile (по умолчанию), test (только для тестов), provided (контейнер предоставит), runtime.

**Расскажи жизненный цикл Maven.**

validate → compile → test → package → verify → install → deploy. validate — проверка проекта. compile — компиляция. test — юнит-тесты. package — упаковка в jar/war. verify — интеграционные тесты. install — в локальный репозиторий ~/.m2. deploy — в удалённый репозиторий (Nexus, Artifactory).
