<!--
reps: 0
priority: 0
-->
#Java/JVM #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что такое Minor GC и Major GC?**

Minor GC — собирает Young Generation. Быстро (миллисекунды), Stop-The-World, но коротко. Major GC — собирает Old Generation, медленнее. Full GC — весь heap + Metaspace. Тревожное событие, если случается часто.

**What are Stop-the-world, Minor GC, and Full GC?**

Источник: https://habr.com/ru/articles/967190/

Stop-the-world — на части фаз GC все потоки приложения останавливаются. Minor GC — Young Generation. Major/Full GC — Old Generation, может включать очистку Metaspace.
