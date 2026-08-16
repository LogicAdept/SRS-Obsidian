<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What are the JVM runtime data areas?**

Источник: https://habr.com/ru/articles/967190/

Heap — все объекты. Method Area (Metaspace) — метаинформация классов, constant pool. JVM Stack — на поток, фреймы вызовов. PC Register — указатель следующей команды потока. Native Method Stack — стек нативных вызовов.
