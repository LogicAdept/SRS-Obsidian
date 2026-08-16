<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What is CMS (Concurrent Mark Sweep)?**

Источник: https://habr.com/ru/articles/967190/

Работает параллельно с приложением, уменьшая STW-паузы. Этапы: initial mark, concurrent mark, remark, sweep. Не компактизирует — возможна фрагментация. Устарел с Java 9, удалён в Java 14. Флаг: -XX:+UseConcMarkSweepGC.
