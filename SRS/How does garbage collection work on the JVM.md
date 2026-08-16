<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Какие сборщики мусора ты знаешь?**

Serial — однопоточный, для маленьких приложений. Parallel — многопоточный для Young, был дефолтом до Java 9. G1 (Garbage First) — с Java 9 дефолт, делит heap на регионы, низкие паузы. ZGC и Shenandoah — для больших heap, паузы менее 10 мс. Generational ZGC — с Java 21, добавил поколения в ZGC.

**Какие бывают сборщики мусора?**

Serial, Parallel, CMS (deprecated с Java 9, удалён в Java 14), G1 (default с Java 9), ZGC, Shenandoah. Для low-latency выбирают ZGC/Shenandoah.

**Generational ZGC — что нового?**

ZGC с Java 21 стал generational (раздельная сборка Young/Old). Паузы <1ms даже на терабайтных heap. Предыдущий ZGC был non-generational (собирал весь heap). Generational ZGC — стандарт для high-load в 2026. G1 — для случаев, когда ZGC overkill (heap <4 GB).

**How does GC free memory?**

Источник: https://habr.com/ru/articles/967190/

GC автоматически освобождает память объектов, на которые больше нет ссылок. Один сборщик может использовать разные алгоритмы для разных областей:
Copying — Young Generation: живые объекты копируются, остальное — мусор.
Mark-Sweep-Compact — чаще Old Generation: Mark живых, Sweep мусора, Compact против фрагментации.
