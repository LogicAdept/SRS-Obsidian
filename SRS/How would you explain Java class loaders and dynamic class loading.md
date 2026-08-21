<!--
reps: 0
priority: 0
-->
#Java/JVM/ClassLoaders #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**Why do custom ClassLoaders exist?**

Источник: https://habr.com/ru/articles/967190/

Custom ClassLoaders нужны для плагинов, модульных систем (OSGi, Spring Boot) и горячей перезагрузки кода. Delegation model: сначала родитель, потом сам.
