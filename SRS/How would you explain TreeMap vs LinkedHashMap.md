<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**TreeMap vs LinkedHashMap.**

TreeMap: красно-чёрное дерево, O(log n), ключи отсортированы (Comparable/Comparator). LinkedHashMap: HashMap + двусвязный список — порядок вставки. accessOrder=true — LRU-кэш. removeEldestEntry() для ограничения размера.

**TreeMap vs LinkedHashMap.**

TreeMap: red-black tree, O(log n), отсортирован. LinkedHashMap: порядок вставки / accessOrder=true для LRU.

**TreeMap vs LinkedHashMap.**

TreeMap: red-black tree, O(log n), ключи отсортированы. LinkedHashMap: HashMap + двусвязный список, порядок вставки. accessOrder=true → LRU-кэш.
