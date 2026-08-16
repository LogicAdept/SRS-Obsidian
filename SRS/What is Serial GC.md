<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What is Serial GC?**

Источник: https://habr.com/ru/articles/967190/

Один поток на все фазы GC. Для однопоточных приложений и небольшого heap. Copying в Young Gen, mark-sweep-compact в Old Gen. Флаг: -XX:+UseSerialGC.
