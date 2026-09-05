<!--
reps: 0
priority: 0
-->
#Java/JVM #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What is the JVM Execution Engine?**

Источник: https://habr.com/ru/articles/967190/

Interpreter — пошаговая интерпретация bytecode. JIT Compiler — компилирует горячие методы в машинный код. GC Interface — Execution Engine связан со сборщиком мусора: знает, когда объект больше не используется.
