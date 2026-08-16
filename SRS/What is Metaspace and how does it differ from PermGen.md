<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What is Metaspace and how does it differ from PermGen?**

Источник: https://habr.com/ru/articles/967190/

Metaspace хранит метаданные классов: методы, константы, аннотации. Сами экземпляры объектов там не живут.
С Java 8 PermGen убрали: Metaspace лежит в нативной памяти, не в heap, и может расти без жёсткого лимита, если не задан -XX:MaxMetaspaceSize. Растёт по мере загрузки классов; лимиты: MaxMetaspaceSize, MetaspaceSize.
