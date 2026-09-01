<!--
reps: 0
priority: 0
-->
#Java/Collections/Map #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Расскажи про реализации Map.**

HashMap — основная, не потокобезопасна, без порядка, null-ключ можно. LinkedHashMap — порядок вставки или access-order (последнее нужно для LRU-кэша). TreeMap — отсортирована по ключу, через NavigableMap (firstKey, lastKey, floorKey). Hashtable — legacy, synchronized, null-ключи не разрешены, не используется.
