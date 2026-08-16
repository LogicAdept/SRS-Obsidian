<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Можно ли null-ключ в HashMap?**

Да, один null-ключ, кладётся в bucket 0. В ConcurrentHashMap нельзя ни ключ, ни значение.

**Можно ли null в HashMap?**

HashMap — да, ОДИН null-ключ (лежит в table[0]), null-значений сколько угодно. TreeMap — null-ключ нельзя (бросит NPE при сравнении). Hashtable — null нельзя ни в ключе, ни в значении (NPE).
