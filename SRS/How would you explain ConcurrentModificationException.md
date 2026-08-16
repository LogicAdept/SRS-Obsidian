<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**ConcurrentModificationException: причина и решение.**

Модификация коллекции во время итерации не через итератор. modCount-счётчик: при следующем next() проверяется. Решения: Iterator.remove(), CopyOnWriteArrayList, ConcurrentHashMap, removeIf() (Java 8+), stream + filter + collect в новый список.
