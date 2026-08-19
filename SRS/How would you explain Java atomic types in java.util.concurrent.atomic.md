<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Atomics #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**How do Java atomics work?**

Источник: https://habr.com/ru/articles/966892/

java.util.concurrent.atomic: атомарность и видимость без блокировок, через CAS — обновить только если значение не изменилось между чтением и записью.
