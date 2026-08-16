<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Young / Old generation — как работает поколенческая сборка?**

Young: Eden + 2 Survivor. После нескольких переживаний minor GC — объект попадает в Old.

**How is the JVM heap structured?**

Источник: https://habr.com/ru/articles/967190/

Young Generation: Eden — новые объекты; Survivor Spaces S0/S1 — промежуточные зоны. Old Generation — объекты, пережившие несколько сборок в Young Gen.
