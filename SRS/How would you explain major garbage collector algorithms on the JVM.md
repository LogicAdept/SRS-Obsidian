<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**Which algorithms do modern GCs use per generation?**

Источник: https://habr.com/ru/articles/967190/

Copying — Young Generation. Mark-Sweep-Compact — чаще Old Generation (Mark → Sweep → Compact против фрагментации). G1 собирает регионы Garbage-First; ZGC/Shenandoah — почти полностью concurrent с короткими паузами.
