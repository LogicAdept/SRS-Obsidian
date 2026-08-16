<!--
reps: 0
priority: 0
-->
#Java/Concurrency #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What are Java thread lifecycle states?**

Источник: https://habr.com/ru/articles/966892/

NEW — создан, ещё не стартовал. RUNNABLE — выполняется или готов, ждёт CPU. BLOCKED — ждёт монитор для synchronized. WAITING — ждёт без таймаута. TIMED_WAITING — ждёт ограниченное время. TERMINATED — закончил.
